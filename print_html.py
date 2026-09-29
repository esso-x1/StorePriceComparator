import requests
r = requests.get('https://boompay.shop', timeout=8)
print("FULL HTML OF BOOMPAY:")
print(r.text)
