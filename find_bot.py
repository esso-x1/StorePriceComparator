import urllib.request
import re

candidates = [
    'insightXpro_bot', 'insightx_bot', 'insightxprobot', 'insight_x_pro_bot', 
    'insightX_bot', 'InsightXProBot', 'insightxstore_bot', 'insightx_pro_bot',
    'insightxbot', 'insight_xbot'
]
for c in candidates:
    url = f'https://t.me/{c}'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req, timeout=3).read().decode('utf-8', errors='ignore')
        title_m = re.search(r'property="og:title"\s+content="([^"]+)"', html)
        desc_m = re.search(r'property="og:description"\s+content="([^"]+)"', html)
        title = title_m.group(1) if title_m else 'None'
        desc = desc_m.group(1) if desc_m else 'None'
        if 'Telegram: Contact' not in title and title != 'None':
            print(f"MATCH: @{c} -> Title: {title} | Desc: {desc[:60]}")
        else:
            print(f"NOT FOUND: @{c}")
    except Exception as e:
        print(f"Error {c}: {e}")
