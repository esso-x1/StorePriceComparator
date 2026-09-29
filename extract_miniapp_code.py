import requests

url = 'https://digital-socials-shop.pages.dev/assets/mini-i18n-B4Y-77qG.js'
t = requests.get(url, timeout=8).text

idx = t.find('https://evpnejwdftnhunlqgrof.supabase.co/functions/v1/mini-app')
print("Surrounding code around mini-app endpoint:")
print(t[max(0, idx-200):min(len(t), idx+1500)])
