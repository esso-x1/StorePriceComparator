import urllib.request
import re

for u in ['https://t.me/insightXpro_bot?start=_tgr_tE2QuLZkYzU8', 'https://t.me/p_a_store_bot?start=_tgr_TRWKnPpiNDFk']:
    req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        html = urllib.request.urlopen(req, timeout=5).read().decode('utf-8', errors='ignore')
        print(f"=== {u} ===")
        links = re.findall(r'https?://[^\s"\'<>]+', html)
        ext = [l for l in links if 'telegram.org' not in l and 't.me' not in l]
        print("External links:", ext)
        # Check any text mentioning web app or app
        meta = re.findall(r'property="og:[^"]+"\s+content="([^"]+)"', html)
        print("Meta:", meta)
    except Exception as e:
        print(f"Error {u}: {e}")
