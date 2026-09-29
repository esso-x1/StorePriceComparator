import requests
from datetime import datetime
from typing import List
try:
    from .base import StoreAdapter, Product, extract_post_date
except ImportError:
    from base import StoreAdapter, Product, extract_post_date

class DigitalSocialsAdapter(StoreAdapter):
    def __init__(self, init_data: str):
        super().__init__(name="Digital Socials", base_url="https://digital-socials-shop.pages.dev/api", bot_username="@Digitalsocials_bot", status="online")
        self.init_data = init_data

    def fetch_products(self) -> List[Product]:
        url = f"{self.base_url}/bootstrap"
        headers = {
            "accept": "application/json",
            "x-telegram-init-data": self.init_data,
            "referer": "https://digital-socials-shop.pages.dev/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        try:
            resp = requests.get(url, headers=headers, timeout=12)
            if resp.status_code == 200:
                data = resp.json()
                categories = data.get("categories", [])
                products = []
                now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
                now_ts = datetime.now().timestamp()
                
                for cat in categories:
                    base_name = cat.get("name", "Unknown Product")
                    desc = cat.get("description") or cat.get("tagline") or ""
                    cat_id = str(cat.get("id", ""))
                    variants = cat.get("variants", [])
                    
                    if not variants:
                        continue
                        
                    for v in variants:
                        var_name = v.get("name")
                        full_name = f"{base_name} ({var_name})" if var_name and var_name.lower() != "none" else base_name
                        price = float(v.get("price", 0.0))
                        stock = int(v.get("stock", 0)) if v.get("stock") is not None else 0
                        currency = str(v.get("currency") or "USD")
                        var_id = str(v.get("id", ""))
                        
                        # Date
                        date_str, ts = extract_post_date(cat_id, cat)
                        if date_str == "غير محدد":
                            date_str, ts = now_str, now_ts
                            
                        products.append(Product(
                            id=f"ds_{cat_id}_{var_id}",
                            store_name=self.name,
                            name=full_name,
                            price=price,
                            currency=currency,
                            in_stock=stock,
                            description=desc,
                            updated_at=date_str,
                            timestamp=ts,
                            category="Digital Services",
                            buy_url=f"https://t.me/Digitalsocials_bot?start=buy_{cat_id}",
                            raw_data=v
                        ))
                return products
            else:
                print(f"[{self.name}] Error status: {resp.status_code}")
                return []
        except Exception as e:
            print(f"[{self.name}] Exception while fetching products: {e}")
            return []
