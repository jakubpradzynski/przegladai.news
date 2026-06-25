import sys
import datetime
import re

def get_next_friday():
    today = datetime.date.today()
    days_ahead = 4 - today.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    return today + datetime.timedelta(days_ahead)

def create_slug(title, issue_num):
    # Remove "Wydanie #XX: " prefix
    clean_title = re.sub(rf'^Wydanie #{issue_num}:\s*', '', title)
    # Lowercase and replace spaces with hyphens
    slug = clean_title.lower()
    # Replace polish characters
    pl_chars = {'ą':'a', 'ć':'c', 'ę':'e', 'ł':'l', 'ń':'n', 'ó':'o', 'ś':'s', 'ź':'z', 'ż':'z'}
    for pl, eng in pl_chars.items():
        slug = slug.replace(pl, eng)
    # Remove special characters
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    # Replace multiple spaces/hyphens with single hyphen
    slug = re.sub(r'[\s-]+', '-', slug).strip('-')
    return f"wydanie-{issue_num}-{slug}"

def update_constants(issue_num, title, slug, next_friday):
    with open('constants.ts', 'r', encoding='utf-8') as f:
        content = f.read()

    # Zapewnienie, że tytuł zawsze będzie miał prefix Wydanie #X:
    full_title = title if title.startswith(f"Wydanie #{issue_num}:") else f"Wydanie #{issue_num}: {title}"

    new_post = f"""  {{
    id: '{issue_num}',
    slug: '{slug}',
    title: '{full_title}',
    date: '{next_friday.strftime('%d-%m-%Y')}',
    htmlUrl: '/issues/{issue_num}.html'
  }},
"""
    # Insert new post at the top of BLOG_POSTS array
    content = content.replace('export const BLOG_POSTS: BlogPost[] = [\n', f'export const BLOG_POSTS: BlogPost[] = [\n{new_post}')
    
    with open('constants.ts', 'w', encoding='utf-8') as f:
        f.write(content)

def update_llms(issue_num, title, slug, next_friday):
    with open('public/llms.txt', 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    
    # Szukamy ostatniego wydania, aby dodać nowe dokładnie po nim (bez podwójnych \n)
    last_issue_index = -1
    for i in range(len(lines) - 1, -1, -1):
        if lines[i].startswith('- **Wydanie #'):
            last_issue_index = i
            break
            
    if last_issue_index != -1:
        # Clean title without "Wydanie #XX: "
        clean_title = re.sub(rf'^Wydanie #{issue_num}:\s*', '', title)
        date_str = next_friday.strftime('%d-%m-%Y')
        # Zwróć uwagę, by nie dodawać znaku nowej linii na końcu!
        new_entry = f'- **Wydanie #{issue_num}**: "{clean_title}" ({date_str}) - https://przegladai.news/{slug}'
        
        lines.insert(last_issue_index + 1, new_entry)
        
        with open('public/llms.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))

def update_sitemap(slug, next_friday):
    with open('public/sitemap.xml', 'r', encoding='utf-8') as f:
        content = f.read()

    new_url = f"""  <url>
    <loc>https://przegladai.news/{slug}</loc>
    <lastmod>{next_friday.strftime('%Y-%m-%d')}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
"""
    content = content.replace('</urlset>', f'{new_url}</urlset>')
    
    with open('public/sitemap.xml', 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    if len(sys.argv) < 3:
        print('Usage: python3 update_configs.py <issue_num> "<title>"')
        sys.exit(1)

    issue_num = sys.argv[1]
    title = sys.argv[2]
    
    next_friday = get_next_friday()
    slug = create_slug(title, issue_num)

    update_constants(issue_num, title, slug, next_friday)
    print(f"Zaktualizowano constants.ts")
    
    update_llms(issue_num, title, slug, next_friday)
    print(f"Zaktualizowano public/llms.txt")
    
    update_sitemap(slug, next_friday)
    print(f"Zaktualizowano public/sitemap.xml")

if __name__ == "__main__":
    main()