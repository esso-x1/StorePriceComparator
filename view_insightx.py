import requests
import json

key = "isk_live_ZubASNjKdXI-UvjdoGJ6Gnt_YAcqBHoZ"
url = "https://api.insightxpro.store/api/v1/products"
headers = {"x-api-key": key}

r = requests.get(url, headers=headers, timeout=8)
data = r.json()
products = data.get("products", [])
print(f"Total products in InsightX: {len(products)}")
for p in products[:10]:
    print(f" - ID: {p.get('id')} | Name: {p.get('name')} | Price: {p.get('price_usdt') or p.get('price')} | Stock: {p.get('stock') or p.get('in_stock')}")
    # print keys
print("Product keys:", list(products[0].keys()) if products else [])
