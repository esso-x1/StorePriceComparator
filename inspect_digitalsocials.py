import requests
import re

# 1. Fetch root HTML
root_html = requests.get('https://digital-socials-shop.pages.dev/', timeout=10).text
print("=== ROOT HTML ===")
print(root_html[:1500])

# 2. Fetch main JS
main_js = requests.get('https://digital-socials-shop.pages.dev/assets/main-DZX2OZ_Y.js', timeout=10).text
print("\n=== MAIN JS LENGTH ===", len(main_js))

# Look for all https in main_js
main_urls = set(re.findall(r'https?://[a-zA-Z0-9_\-\./]+', main_js))
print("URLs in main JS:", [u for u in main_urls if 'w3.org' not in u and 'react' not in u])

# 3. Check for keywords like products, categories, price, firebase, supabase, render
for kw in ["products", "categories", "price", "supabase", "firebase", "render", "api", "fetch"]:
    print(f"Keyword '{kw}': root={root_html.count(kw)}, main_js={main_js.count(kw)}")
