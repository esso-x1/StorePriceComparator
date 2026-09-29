import urllib.request
import re

url = 'https://t.me/QuickDigiBot'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    html = urllib.request.urlopen(req, timeout=5).read().decode('utf-8', errors='ignore')
    print('=== @QuickDigiBot ===')
    title_m = re.search(r'property="og:title"\s+content="([^"]+)"', html)
    desc_m = re.search(r'property="og:description"\s+content="([^"]+)"', html)
    print('Title:', title_m.group(1) if title_m else 'None')
    print('Desc:', desc_m.group(1) if desc_m else 'None')
    
    # check for links
    links = re.findall(r'href="([^"]+)"', html)
    ext = [l for l in links if 'telegram.org' not in l and 't.me' not in l]
    print('External links:', ext)
except Exception as e:
    print('Error:', e)
