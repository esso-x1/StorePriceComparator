import requests
import re

r = requests.get('https://boompay.shop', timeout=8)
print("=== HTML PREVIEW ===")
print(r.text[:1500])

scripts = re.findall(r'src="([^"]+)"', r.text)
print("=== SCRIPTS ===")
for s in scripts:
    print("Script:", s)
    if s.endswith('.js'):
        full_url = s if s.startswith('http') else 'https://boompay.shop' + s
        try:
            js_code = requests.get(full_url, timeout=5).text
            # Look for API endpoints in JS code
            endpoints = re.findall(r'https?://[^\s\'"<>]+|/api/[^\s\'"<>]+', js_code)
            unique_eps = list(set([e for e in endpoints if 'react' not in e and 'google' not in e]))
            print(f"  Found endpoints in {s}:", unique_eps[:10])
        except Exception as e:
            print(f"  Error fetching JS: {e}")
