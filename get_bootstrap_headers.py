import requests

url = 'https://digital-socials-shop.pages.dev/assets/mini-i18n-B4Y-77qG.js'
t = requests.get(url, timeout=8).text

idx = t.find('/api/bootstrap')
print("Code around /api/bootstrap:")
print(t[max(0, idx-500):min(len(t), idx+1000)])
