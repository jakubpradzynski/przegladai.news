"""Czyszczenie, normalizacja i rozwijanie URL-i.

Zestaw parametrow do usuniecia jest nadzbiorem tego z dawnego prepare_skeleton.py.
"""
import re
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

TRACKING_PARAMS = [
    # oryginalna lista z dawnego prepare_skeleton.py
    'utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content',
    '_bhlid', 'lid', 'r', 'triedRedirect', 'IR', 'isFreemail', 'mod', 'module',
    'pgtype', 'post_id', 'publication_id', 'reflink', 's',
    # dodatki spotykane w newsletterach
    'utm_id', 'utm_name', 'utm_brand', 'utm_social', 'utm_social-type',
    'mc_cid', 'mc_eid', 'ck_subscriber_id', 'gclid', 'fbclid', 'igshid',
    'ref', 'referrer', 'source', 'sourceid', 'tpcc', 'cmp', 'at_medium',
    'at_campaign', 'email_token', 'subscriber_id', 'user_id', 'hss_channel',
    '_hsenc', '_hsmi', 'mkt_tok', 'trk', 'trkCampaign', 'li_fat_id',
    'guccounter', 'guce_referrer', 'guce_referrer_sig', 'sh',
]

URL_PATTERN = re.compile(r'https?://[^\s<>"\'\]\)]+')

# Hosty posrednikow: newslettery owijaja KAZDY link artykulu w tracker.
# Takich linkow nie wolno odrzucac po domenie - trzeba je rozwinac przez resolve_redirect().
REDIRECT_HOST_PREFIXES = (
    'link.', 'links.', 'click.', 'clicks.', 'trk.', 'track.', 'tracking.',
    'email.', 'mail.', 'e.', 'em.', 'go.', 'r.', 'u.', 't.', 'url.', 'ss.',
)

REDIRECT_HOST_SUFFIXES = (
    'beehiiv.com', 'list-manage.com', 'sendgrid.net', 'mailgun.org',
    'convertkit-mail.com', 'convertkit-mail2.com', 'customeriomail.com',
    'pstmrk.it', 'mailanyone.net', 'sparkpostmail.com', 'rsgnl.co',
    'mailchimp.com', 'hubspotlinks.com', 'salesforce.com', 'exct.net',
    'tldrnewsletter.com', 'mailerlite.com', 'ecomail.eu', 'freshmail.com',
)

REDIRECT_PATH_MARKERS = (
    '/ss/c/', '/redirect/', '/redirect?', '/click?', '/c/e/', '/wf/click',
    '/track/click', '/api/mailings/click', '/CL0/', '/ls/click',
)

REDIRECT_EXACT_HOSTS = (
    't.co', 'bit.ly', 'buff.ly', 'lnkd.in', 'ow.ly', 'tinyurl.com',
    'dub.sh', 'shorturl.at', 'rb.gy',
)


def clean_url(url):
    """Usuwa parametry sledzace i normalizuje URL. Nigdy nie rzuca wyjatkiem."""
    try:
        url = url.strip().rstrip('.,;)]}\'"')
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            return url

        query_params = parse_qs(parsed.query, keep_blank_values=True)
        for param in TRACKING_PARAMS:
            query_params.pop(param, None)

        # www. i koncowy slash zostaja - to link, ktory trafi do wydania.
        # Porownania robimy przez dedup_key(), ktory je ignoruje.
        netloc = parsed.netloc.lower()
        path = parsed.path

        # fragmenty w newsletterach to prawie zawsze kotwice sledzace
        # albo fragmenty tekstowe (#:~:text=...) doklejane przez czytniki
        fragment = parsed.fragment or ''
        if fragment.startswith('utm') or fragment.startswith(':~:'):
            fragment = ''

        return urlunparse((
            parsed.scheme, netloc, path, parsed.params,
            urlencode(query_params, doseq=True), fragment,
        ))
    except Exception:
        return url


def looks_like_redirect(url):
    """Czy link jest opakowany w tracker/skracacz i wymaga rozwiniecia."""
    try:
        parsed = urlparse(url)
    except Exception:
        return False

    host = parsed.netloc.lower()
    if host.startswith('www.'):
        host = host[4:]
    path = parsed.path or ''

    if host in REDIRECT_EXACT_HOSTS:
        return True
    if any(host.endswith(suffix) for suffix in REDIRECT_HOST_SUFFIXES):
        return True
    if any(marker in path for marker in REDIRECT_PATH_MARKERS):
        return True
    # subdomena typu link.* / click.* / email.* przy dowolnej domenie
    if any(host.startswith(prefix) for prefix in REDIRECT_HOST_PREFIXES) and '.' in host[host.index('.') + 1:]:
        return True
    return False


def extract_urls(text):
    """Wyciaga wszystkie URL-e z dowolnego tekstu."""
    return [clean_url(m) for m in URL_PATTERN.findall(text or '')]


META_REFRESH_RE = re.compile(
    r'<meta[^>]+http-equiv=["\']?refresh["\']?[^>]*content=["\']?[^"\'>]*?url\s*=\s*([^"\'>\s]+)',
    re.IGNORECASE)
JS_REDIRECT_RE = re.compile(
    r'(?:window\.)?location(?:\.href)?\s*=\s*["\'](https?://[^"\']+)["\']', re.IGNORECASE)

UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36')
HEADERS = {'User-Agent': UA, 'Accept-Language': 'pl,en;q=0.8'}


def _from_body(text):
    """Substack i czesc bramek nie robi przekierowania HTTP, tylko meta refresh."""
    if not text:
        return None
    head = text[:8000]
    match = META_REFRESH_RE.search(head) or JS_REDIRECT_RE.search(head)
    if not match:
        return None
    target = match.group(1).strip().strip('\'"')
    target = target.replace('&#38;', '&').replace('&amp;', '&')
    return target if target.startswith('http') else None


def resolve_redirect(url, timeout=12, session=None, max_hops=3):
    """Rozwija lancuch przekierowan do docelowego URL-a.

    Najpierw HEAD (tanie), potem GET. Gdy serwer odpowiada 200, ale strona jest
    tylko bramka z `meta refresh` (tak robi Substack), idziemy za nia dalej.
    """
    import requests

    sess = session or requests
    current = url

    for _ in range(max_hops):
        try:
            resp = sess.head(current, allow_redirects=True, timeout=timeout, headers=HEADERS)
            if resp.status_code >= 400 or resp.url == current:
                resp = sess.get(current, allow_redirects=True, timeout=timeout,
                                headers=HEADERS)
                nxt = _from_body(resp.text)
            else:
                nxt = None

            landed = resp.url
            if nxt and nxt != landed:
                current = nxt
                continue
            if landed != current:
                current = landed
                if not looks_like_redirect(current):
                    break
                continue
            break
        except Exception:
            break

    return clean_url(current)


def dedup_key(url):
    """Klucz deduplikacji - ignoruje schemat, www i koncowy slash."""
    cleaned = clean_url(url)
    parsed = urlparse(cleaned)
    host = parsed.netloc.lower()
    if host.startswith('www.'):
        host = host[4:]
    return (host, parsed.path.rstrip('/').lower(), parsed.query)


def normalize_anchor(text):
    """Klucz deduplikacji po tekscie kotwicy - ten sam artykul z trzech newsletterow."""
    if not text:
        return ''
    text = re.sub(r'\s+', ' ', text).strip().lower()
    text = re.sub(r'[^\w\sąćęłńóśźż]', '', text, flags=re.UNICODE)
    return text
