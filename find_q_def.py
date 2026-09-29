import requests
import re

url = 'https://digital-socials-shop.pages.dev/assets/mini-i18n-B4Y-77qG.js'
t = requests.get(url, timeout=8).text

for m in re.finditer(r'(?:async\s+function|function|const|let|var)\s+Q\s*[:=]', t):
    print("Q defined at:", m.start())
    print(t[m.start():m.start()+600])
