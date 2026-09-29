import requests
import re

js = requests.get('https://boompay.shop/assets/index-QFWwP6Si.js', timeout=8).text

# Find occurrences of "products" or items
for m in re.finditer(r'products\s*[:=]\s*(\[.*?\])', js):
    content = m.group(1)[:500]
    print("Found products array:", content)

# Check for price and name objects
objects = re.findall(r'\{[^{}]*name[^{}]*price[^{}]*\}', js)
print("Found name/price objects:", len(objects))
for obj in objects[:5]:
    print(" ->", obj)
