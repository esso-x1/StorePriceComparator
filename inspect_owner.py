import requests
import re

for chunk in ['OwnerApp-Bz8ehWyW.js', 'mini-i18n-B4Y-77qG.js']:
    url = f'https://digital-socials-shop.pages.dev/assets/{chunk}'
    t = requests.get(url, timeout=8).text
    print(f"=== {chunk} (Length: {len(t)}) ===")
    if 'supabase' in t.lower():
        print("  SUPABASE FOUND in", chunk)
        for m in re.finditer(r'.{0,100}supabase.{0,200}', t, re.IGNORECASE):
            print("   ->", m.group(0))
    if 'evpnejwdftnhunlqgrof' in t:
        print("  evpnejwdftnhunlqgrof FOUND in", chunk)
        idx = t.find('evpnejwdftnhunlqgrof')
        print("   ->", t[max(0, idx-50):min(len(t), idx+250)])
