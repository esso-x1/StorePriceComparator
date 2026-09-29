import urllib.request
import re

bots = [
    'insightXpro_bot',
    'digital_assetbot',
    'boompayshop_bot',
    'p_a_store_bot',
    'Veriyferbot',
    'GeminiPixel1_bot',
    'QuickDigiBot',
    'aishopmopsbot',
    'Digitalsocials_bot'
]

for b in bots:
    url = f'https://t.me/{b}'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req, timeout=5).read().decode('utf-8', errors='ignore')
        title_m = re.search(r'property="og:title"\s+content="([^"]+)"', html)
        desc_m = re.search(r'property="og:description"\s+content="([^"]+)"', html)
        
        # also search for any web app or links
        links = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', html)
        external_links = [l for l in links if 'telegram' not in l and 't.me' not in l and 'w3.org' not in l]

        title = title_m.group(1) if title_m else 'None'
        desc = desc_m.group(1) if desc_m else 'None'
        print(f"=== @{b} ===")
        print(f"Title: {title}")
        print(f"Desc: {desc}")
        if external_links:
            print(f"External Links: {external_links}")
        print("-" * 40)
    except Exception as e:
        print(f"=== @{b} === Error: {e}")
