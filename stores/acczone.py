import requests
from datetime import datetime
from typing import List
from .base import StoreAdapter, Product, extract_post_date

class AcczoneAdapter(StoreAdapter):
    """Adapter for Acczone Store (@Acczone_Store_bot) via api.acczone.xyz"""
    def __init__(self, api_key: str = "mpaRrF2QhLHHWxZQM4iuBDggPkBu72Yu38GUth3qQc8"):
        super().__init__(name="Acczone Store", base_url="https://api.acczone.xyz", bot_username="@Acczone_Store_bot", status="online")
        self.api_key = api_key

    def fetch_products(self) -> List[Product]:
        url = f"{self.base_url}/getServices"
        headers = {
            "X-API-Key": self.api_key,
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json"
        }
        params = {"key": self.api_key}
        try:
            resp = requests.get(url, headers=headers, params=params, timeout=4)
            if resp.status_code == 200:
                raw_items = resp.json()
                products = []
                now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
                now_ts = datetime.now().timestamp()

                if isinstance(raw_items, list):
                    for item in raw_items:
                        pid = str(item.get("key", ""))
                        name = item.get("name", "Unknown")
                        price = float(item.get("price", 0.0))
                        stock = int(item.get("stock", 0)) if item.get("is_active", 1) else 0
                        currency = "USDT"
                        desc = item.get("description", "")

                        date_str, ts = extract_post_date(pid, item)
                        if date_str == "غير محدد":
                            date_str, ts = now_str, now_ts

                        products.append(Product(
                            id=f"acc_{pid}",
                            store_name=self.name,
                            name=name,
                            price=price,
                            currency=currency,
                            in_stock=stock,
                            description=desc,
                            updated_at=date_str,
                            timestamp=ts,
                            category="Digital Services",
                            buy_url="https://t.me/Acczone_Store_bot",
                            raw_data=item
                        ))
                return products
            else:
                print(f"[{self.name}] Error status: {resp.status_code}")
                return []
        except Exception as e:
            print(f"[{self.name}] Exception while fetching products: {e}")
            return []
