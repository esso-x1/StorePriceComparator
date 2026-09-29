import requests

url = 'https://digital-socials-shop.pages.dev/assets/mini-i18n-B4Y-77qG.js'
t = requests.get(url, timeout=8).text

idx = t.find('function Cn()')
print("Code before function Cn():")
print(t[max(0, idx-1000):idx])
