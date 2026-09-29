import requests
import re

js = requests.get('https://boompay.shop/assets/index-QFWwP6Si.js', timeout=8).text
print("JS length:", len(js))

# Look for fetch or axios or endpoints
endpoints = re.findall(r'(/api/[a-zA-Z0-9_\-\./]+)', js)
print("Endpoints found:", set(endpoints))

# Look for domains or base URLs
domains = re.findall(r'https?://[a-zA-Z0-9_\-\.]+', js)
print("Domains found:", set(domains))

# Look for headers
headers_matches = re.findall(r'([a-zA-Z\-]+api[a-zA-Z\-]+)', js, re.IGNORECASE)
print("Headers matches:", set(headers_matches))

# Look for any hardcoded product lists or items
if "products" in js:
    print("Keyword 'products' is present in JS")
