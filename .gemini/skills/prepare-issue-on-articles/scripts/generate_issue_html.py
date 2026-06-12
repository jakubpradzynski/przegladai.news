import sys
import csv
import re

def main():
    if len(sys.argv) < 5:
        print("Usage: python generate_issue_html.py <prev_issue_file> <new_issue_file> \"<title>\" \"<intro_text>\"")
        sys.exit(1)
        
    prev_file = sys.argv[1]
    new_file = sys.argv[2]
    new_title = sys.argv[3]
    intro_text = sys.argv[4]
    
    with open('final_prepared_data.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        articles = list(reader)
        
    if not articles:
        print("Brak artykułów w final_prepared_data.csv")
        sys.exit(1)

    with open(f"public/issues/{prev_file}.html", 'r', encoding='utf-8') as f:
        html = f.read()

    # Wstrzyknięcie stylu dla tagu paywall, jeśli nie istnieje
    if ".tag-paywall" not in html:
        css_paywall = """
        .tag-paywall {
            background-color: #f5f5f5;
            color: #616161;
        }"""
        html = html.replace('.tag-pl {', css_paywall.strip() + '\n\n        .tag-pl {')

    # Top 3 (opcjonalnie)
    top3_html = ""
    for i in range(min(3, len(articles))):
        top3_html += f'''<li style="margin-bottom: 10px; font-size: 15px; line-height: 1.5; color: #444;">{articles[i]["Tytuł"]}</li>\n                                                        '''

    ul_pattern = re.compile(r'(<h3[^>]*>Top 3[^<]*informacje</h3>\s*<ul[^>]*>)(.*?)(</ul>)', re.IGNORECASE | re.DOTALL)
    html = ul_pattern.sub(r'\g<1>\n                                                        ' + top3_html.strip() + r'\n                                                    \g<3>', html)

    # Title update
    title_pattern = re.compile(r'(<title>)(.*?)(</title>)', re.IGNORECASE | re.DOTALL)
    html = title_pattern.sub(r'\g<1>' + new_title + r' - PrzeglądAI\n    \g<3>', html)

    # Intro text update
    intro_pattern = re.compile(r'(<strong>Cześć!</strong>\s*<br><br>\s*)(.*?)(\s*<br><br>\s*Zapraszam do lektury!)', re.IGNORECASE | re.DOTALL)
    html = intro_pattern.sub(r'\g<1>' + intro_text + r'\g<3>', html)

    # Articles
    articles_html = ""
    for i, a in enumerate(articles):
        tags = [t.strip() for t in a["Tagi"].split(",") if t.strip()]
        tags_html = ""
        for t in tags:
            tag_class = "news-tag"
            if "nowości" in t.lower(): tag_class += " tag-news"
            elif "bliżej" in t.lower(): tag_class += " tag-tech"
            elif "polska" in t.lower(): tag_class += " tag-pl"
            elif "paywall" in t.lower(): tag_class += " tag-paywall"
            tags_html += f'<span class="{tag_class}">{t}</span>\n                                        '
            
        if a.get("Czas"):
            tags_html += f'<span class="news-tag">{a["Czas"]}</span>\n                                        '

        border_top = ' border-top: 1px solid #eeeeee;' if i == 0 else ''
        
        articles_html += f'''                            <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                <tr>
                                    <td style="padding-top: 20px; padding-bottom: 20px; border-bottom: 1px solid #eeeeee;{border_top}">
                                        <a href="{a["Link"]}" class="news-title">
                                            {a["Tytuł"]}
                                        </a>
                                        <div class="news-desc">
                                            {a["Opis"]}
                                        </div>
                                        {tags_html.strip()}
                                    </td>
                                </tr>
                            </table>\n'''

    # Wymiana kontenera z artykułami przy użyciu bardziej elastycznego wyrażenia regularnego
    pattern = re.compile(
        r'(<td class="mobile-padding" style="padding: 10px 30px 30px 30px;">\s*).*?(</td>\s*</tr>\s*</table>\s*<table[^>]*style="background-color: #f9f9f9; border-top: 1px solid #eeeeee;">)', 
        re.DOTALL | re.IGNORECASE
    )
    
    html = pattern.sub(r'\1\n' + articles_html + r'                        \2', html)
    
    with open(f"public/issues/{new_file}.html", 'w', encoding='utf-8') as f:
        f.write(html)
        
    print(f"Wygenerowano public/issues/{new_file}.html")

if __name__ == "__main__":
    main()