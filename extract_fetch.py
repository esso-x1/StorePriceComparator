import requests
import re

js = requests.get('https://boompay.shop/assets/index-QFWwP6Si.js', timeout=8).text

for m in re.finditer(r'fetch\((.*?)\)', js):
    print("Fetch call:", m.group(0)[:200])

for m in re.finditer(r'([a-zA-Z0-9_\-\.]*onrender\.com[a-zA-Z0-9_\-\./]*)', js):
    print("Render URL found:", m.group(0))
