import sys
import re
import os
import csv
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

def clean_url(url):
    try:
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            return url
        
        query_params = parse_qs(parsed.query, keep_blank_values=True)
        
        params_to_remove = [
            'utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content',
            '_bhlid', 'lid', 'r', 'triedRedirect', 'IR', 'isFreemail', 'mod', 'module',
            'pgtype', 'post_id', 'publication_id', 'reflink', 's'
        ]
        
        for param in params_to_remove:
            query_params.pop(param, None)
            
        new_query = urlencode(query_params, doseq=True)
        
        new_url = urlunparse((
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            parsed.params,
            new_query,
            parsed.fragment
        ))
        
        return new_url
    except Exception:
        return url

def main():
    if len(sys.argv) < 3:
        print("Usage: python prepare_skeleton.py <input_file> <output_file>")
        sys.exit(1)
        
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        # Match URLs using same pattern as clear_links.py
        url_pattern = re.compile(r'https?://[^\s<>"\'\]\)]+')
        
        unique_urls = set()
        for line in lines:
            matches = url_pattern.findall(line)
            for match in matches:
                cleaned = clean_url(match)
                unique_urls.add(cleaned)
        
        with open(output_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            writer.writerow(['Link', 'Tytuł', 'Opis', 'Tagi', 'Czas'])
            for url in sorted(list(unique_urls)):
                writer.writerow([url, '', '', '', ''])
                
        print(f"Success: Skeleton CSV saved as {output_file} with {len(unique_urls)} unique links.")
    except Exception as e:
        print(f"Error processing file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
