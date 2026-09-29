import requests
import re

url = 'https://digital-socials-shop.pages.dev/assets/mini-i18n-B4Y-77qG.js'
t = requests.get(url, timeout=8).text

endpoints = re.findall(r'[\'\"`](/api/[a-zA-Z0-9_\-\./]+)[\'\"`]', t)
print("API endpoints found in mini-i18n:")
for ep in set(endpoints):
    print(" ->", ep)
