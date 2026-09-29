import requests
from datetime import datetime
from typing import List
try:
    from .base import StoreAdapter, Product, extract_post_date
except ImportError:
    from base import StoreAdapter, Product, extract_post_date

class PAStoreAdapter(StoreAdapter):
    def __init__(self, api_key: str = "PA-292575994D5D30F31C1443FC677AB9994C2A3567"):
        super().__init__(name="PA Store", base_url="http://store.proaccesses.com/api/v1", bot_username="@p_a_store_bot", status="online")
        self.api_key = api_key
        # Direct unblocked Cloudflare Anycast IP to bypass local DNS/ISP routing drops
        self.direct_ip = "104.21.73.95"

    def fetch_products(self) -> List[Product]:
        url = f"http://{self.direct_ip}/api/v1/products"
        headers = {
            "Host": "store.proaccesses.com",
            "X-API-Key": self.api_key,
            "Accept": "application/json"
        }
        try:
            resp = requests.get(url, headers=headers, timeout=4)
            if resp.status_code == 200:
                data = resp.json()
                items = data.get("products", [])
                products = []
                now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
                now_ts = datetime.now().timestamp()
                
                for item in items:
                    pid = str(item.get("id", ""))
                    name = item.get("name", "Unknown")
                    price = float(item.get("price_usdt", 0.0))
                    stock = int(item.get("stock", 0)) if item.get("stock") is not None else 0
                    desc = item.get("description", "")
                    
                    # Date
                    date_str, ts = extract_post_date(pid, item)
                    if date_str == "غير محدد":
                        date_str, ts = now_str, now_ts
                        
                    products.append(Product(
                        id=f"pa_{pid}",
                        store_name=self.name,
                        name=name,
                        price=price,
                        currency="USDT",
                        in_stock=stock,
                        description=desc,
                        updated_at=date_str,
                        timestamp=ts,
                        category="Digital Services",
                        buy_url=f"https://t.me/p_a_store_bot?start=buy_{pid}",
                        raw_data=item
                    ))
                return products
            else:
                print(f"[{self.name}] Error status: {resp.status_code}")
                return []
        except Exception as e:
            print(f"[{self.name}] Exception while fetching products: {e}")
            return []

    def get_balance(self) -> float:
        url = f"http://{self.direct_ip}/api/v1/balance"
        headers = {
            "Host": "store.proaccesses.com",
            "X-API-Key": self.api_key
        }
        try:
            resp = requests.get(url, headers=headers, timeout=8)
            if resp.status_code == 200:
                return float(resp.json().get("balance", 0.0))
        except Exception:
            pass
        return 0.0
