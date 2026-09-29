import requests
import re

text = requests.get('https://digital-socials-shop.pages.dev/assets/MiniApp-Cj1TFNW6.js', timeout=8).text
chunks = re.findall(r'["\']([^"\']+\.js)["\']', text)
print("Chunks in MiniApp:", set(chunks))

main_text = requests.get('https://digital-socials-shop.pages.dev/assets/main-DZX2OZ_Y.js', timeout=8).text
chunks_m = re.findall(r'["\']([^"\']+\.js)["\']', main_text)
print("Chunks in Main:", set(chunks_m))
