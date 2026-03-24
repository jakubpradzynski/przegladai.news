import sys
import re
import os
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

def clean_url(match):
    url = match.group(0)
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
    except Exception as e:
        return url

def main():
    if len(sys.argv) < 2:
        print("Usage: python clear_links.py <input_file>")
        sys.exit(1)
        
    input_file = sys.argv[1]
    
    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)

    dirname = os.path.dirname(input_file)
    basename = os.path.basename(input_file)
    output_file = os.path.join(dirname, f"cleaned_{basename}")
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Match URLs stopping at space, quotes, or markdown brackets
        # Using [^\s<>"'\])]+ which means match any character EXCEPT those in the set
        url_pattern = re.compile(r'https?://[^\s<>"\'\]\)]+')
        cleaned_content = url_pattern.sub(clean_url, content)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(cleaned_content)
            
        print(f"Success: Processed file saved as {output_file}")
    except Exception as e:
        print(f"Error processing file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
