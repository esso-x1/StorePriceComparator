import requests
import json

key = "isk_live_ZubASNjKdXI-UvjdoGJ6Gnt_YAcqBHoZ"
base = "https://api.insightxpro.store"

paths = ["", "/docs", "/api/docs", "/api/v1/products", "/api/products", "/products", "/api/v1/balance", "/balance"]
for p in paths:
    url = base + p
    headers = {
        "x-api-key": key,
        "X-API-Key": key,
        "Authorization": f"Bearer {key}",
        "Accept": "application/json"
    }
    try:
        r = requests.get(url, headers=headers, timeout=8)
        print(f"GET {p or '/'} -> Status: {r.status_code} ({len(r.text)} bytes)")
        if r.status_code == 200:
            print("  SUCCESS:", r.text[:300])
        elif r.status_code in [400, 401, 403, 404]:
            print(f"  Status {r.status_code}:", r.text[:200])
    except Exception as e:
        print(f"GET {p or '/'} -> Error: {e}")
