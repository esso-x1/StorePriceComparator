import requests
import json

headers = {'x-api-key': 'rk_live_UtCaFiQCiztkP7pZBc-hHs04RJJKSxoJ9DKNlncCrEo'}
r = requests.get('https://digital-assets-api.pe-supplykh.com/api/v1/products', headers=headers)
data = r.json()
products = data.get('data', [])
print(f"Total product groups: {len(products)}")
for p in products:
    print(f"\nGroup: {p.get('name')}")
    for v in p.get('variations', []):
        print(f"   - {v.get('name')} | Price: {v.get('price')} USD | ID: {v.get('id')}")
