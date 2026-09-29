import requests
import json

tests = [
    {
        "name": "digital_assetbot",
        "base_url": "https://digital-assets-api.pe-supplykh.com",
        "key": "rk_live_UtCaFiQCiztkP7pZBc-hHs04RJJKSxoJ9DKNlncCrEo"
    },
    {
        "name": "boompayshop_bot",
        "base_url": "https://api.boompay.shop",
        "key": "bp_UMXpMbigljksmoBt1esML45IW3u16NXZj63ypm-4AKI"
    },
    {
        "name": "Veriyferbot (duskyr)",
        "base_url": "https://duskyr.com/api/v1",
        "key": "dsk_live_j5xLScD0vuH53xvIJOGhnqruibi3woYY0Ru-7fsL7nY"
    }
]

for t in tests:
    name = t["name"]
    base_url = t["base_url"].rstrip("/")
    key = t["key"]
    print(f"\n==========================================")
    print(f"Testing {name} -> {base_url}")
    print(f"==========================================")
    
    # 1. First test root / docs / openapi
    for path in ["/docs", "/openapi.json", "/api/v1/products", "/products", "/api/products", "/balance", "/api/v1/balance"]:
        url = base_url + path
        # Try both x-api-key and Authorization
        headers = {
            "x-api-key": key,
            "Authorization": f"Bearer {key}",
            "Accept": "application/json"
        }
        try:
            r = requests.get(url, headers=headers, timeout=8)
            print(f"GET {path} -> {r.status_code} ({len(r.text)} bytes)")
            if r.status_code == 200:
                try:
                    j = r.json()
                    preview = json.dumps(j)[:300]
                    print(f"  [SUCCESS JSON]: {preview}...")
                except Exception:
                    print(f"  [SUCCESS HTML/TEXT]: {r.text[:200]}...")
            elif r.status_code in [400, 401, 403, 404]:
                print(f"  [Status {r.status_code}]: {r.text[:150]}")
        except Exception as e:
            print(f"GET {path} -> FAILED: {e}")
