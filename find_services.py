import requests
import re

js = requests.get('https://boompay.shop/assets/index-QFWwP6Si.js', timeout=8).text

for word in ["supabase", "firebase", "backend", "render", "vercel", "api.", "fetch(", "axios"]:
    count = js.count(word)
    print(f"Word '{word}': {count} occurrences")

# Find strings starting with https
urls = re.findall(r'["\'](https://[^"\']+)["\']', js)
print("All https URLs in JS:", set(urls))
