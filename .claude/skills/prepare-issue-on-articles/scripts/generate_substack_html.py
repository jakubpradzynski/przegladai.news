import sys
import re
import os
from bs4 import BeautifulSoup

TAG_TEXT_COLORS = {
    'polska': '#d9381e',
    'nowości i ogłoszenia': '#1a73e8',
    'bliżej technologii': '#e6a100',
    'za paywallem': '#707070',
}

def get_tag_html(tag_text):
    lower_tag = tag_text.lower().strip()
    color = TAG_TEXT_COLORS.get(lower_tag, '#707070')
    return f'<span style="color: {color}; font-weight: bold; font-size: 11px; margin-right: 8px;">[{tag_text.strip()}]</span>'

def clean_text(text):
    if not text:
        return ''
    cleaned = text.replace('\xa0', ' ').replace('&nbsp;', ' ')
    return re.sub(r'\s+', ' ', cleaned).strip()

def extract_welcome(soup):
    for cell in soup.find_all('td'):
        cell_text = cell.get_text()
        if 'Cześć!' not in cell_text and 'Witaj w pierwszym wydaniu' not in cell_text:
            continue
        cell_html = cell.decode_contents()
        text_with_newlines = (
            cell_html.replace('<br>', '\n').replace('<br/>', '\n')
            .replace('<br />', '\n').replace('</p>', '\n\n')
        )
        text_clean = BeautifulSoup(text_with_newlines, 'html.parser').get_text()
        start_idx = max(text_clean.find('Cześć!'), text_clean.find('Witaj w pierwszym wydaniu'))
        if start_idx == -1:
            continue
        sub = text_clean[start_idx:]
        end_idx = sub.find('Zapraszam do lektury!')
        if end_idx != -1:
            return sub[:end_idx + len('Zapraszam do lektury!')].strip()
        return sub.split('Bonus dla czytelników!')[0].split('Top 3')[0].strip()
    return 'Cześć!\n\nZapraszam do lektury najnowszego wydania newslettera.'

def rebuild_welcome(raw_text):
    paragraphs = [p.strip() for p in raw_text.split('\n') if p.strip()]
    result = []
    if not paragraphs:
        return raw_text
    result.append(paragraphs[0])
    middle = paragraphs[1:-1] if len(paragraphs) > 2 else paragraphs[1:]
    if middle:
        result.append(' '.join(middle))
    if len(paragraphs) > 2 and paragraphs[-1].startswith('Zapraszam'):
        result.append(paragraphs[-1])
    return '\n\n'.join(result)

def main():
    if len(sys.argv) < 6:
        print('Usage: python generate_substack_html.py <issue_num> "<seo_title>" "<seo_description>" "<slug>" "<publish_date>"')
        sys.exit(1)

    issue_num = int(sys.argv[1])
    seo_title = sys.argv[2]
    seo_description = sys.argv[3]
    slug = sys.argv[4]
    publish_date = sys.argv[5]

    input_path = f'public/issues/{issue_num}.html'
    output_dir = 'public/substack_posts_html'
    os.makedirs(output_dir, exist_ok=True)

    with open(input_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    welcome_text = rebuild_welcome(extract_welcome(soup))

    # Extract articles (modern layout only — news-title / news-desc / news-tag classes)
    articles = []
    for title_el in soup.find_all(class_=re.compile(r'news-title')):
        url = title_el.get('href', '')
        title = clean_text(title_el.get_text())
        desc = ''
        tags = []
        container = title_el.find_parent('td') or title_el.parent
        if container:
            desc_el = container.find(class_=re.compile(r'news-desc'))
            if desc_el:
                desc = clean_text(desc_el.get_text())
            for tag_el in container.find_all(class_=re.compile(r'news-tag')):
                tags.append(clean_text(tag_el.get_text()))
        if title and url:
            articles.append({'title': title, 'url': url, 'desc': desc, 'tags': tags})

    # Deduplicate by URL
    seen_urls = set()
    unique_articles = []
    for art in articles:
        if art['url'] not in seen_urls:
            seen_urls.add(art['url'])
            unique_articles.append(art)

    # Build output HTML
    parts = []
    parts.append(f'<h1>{seo_title}</h1>')

    for p_text in welcome_text.split('\n\n'):
        p_clean = p_text.replace('\n', '<br>').strip()
        if p_clean:
            parts.append(f'<p>{p_clean}</p>')

    parts.append('<hr>')

    for art in unique_articles:
        parts.append(f'<h3><a href="{art["url"]}">{art["title"]}</a></h3>')
        if art['desc']:
            parts.append(f'<p>{art["desc"]}</p>')
        if art['tags']:
            tags_html = ' '.join(get_tag_html(t) for t in art['tags'])
            parts.append(f'<p>{tags_html}</p>')
        parts.append('<hr>')

    # Metadata block — visible in browser, separated from content
    parts.append(
        '<div style="margin-top: 48px; padding: 20px 24px; background-color: #f5f5f5;'
        ' border: 1px solid #ddd; border-radius: 6px; font-size: 13px; line-height: 1.7;">'
        '<p style="margin: 0 0 12px 0; font-size: 15px; font-weight: bold;">📋 Metadane Substack</p>'
        f'<p><strong>Tytuł SEO:</strong> {seo_title}</p>'
        f'<p><strong>Opis SEO</strong> ({len(seo_description)} znaków)<strong>:</strong> {seo_description}</p>'
        f'<p><strong>URL posta:</strong> {slug}</p>'
        f'<p><strong>Data publikacji:</strong> {publish_date}</p>'
        '</div>'
    )

    output_path = f'{output_dir}/issue_{issue_num}_substack.html'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(parts))

    print(f'Wygenerowano {output_path}')

if __name__ == '__main__':
    main()
