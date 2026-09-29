import re
import requests
from datetime import datetime
from typing import List
from .base import StoreAdapter, Product, extract_post_date

class BiteStoreAdapter(StoreAdapter):
    """Adapter for Bite Store (@Bite_storee_bot) via Railway API"""
    def __init__(self, api_key: str = "bsk_eNB_wmuVWLiHXO1T41qIN7D5ufKgTWbOPtxIsccoRXc"):
        super().__init__(name="Bite Store", base_url="https://bite-store-bot-production.up.railway.app", bot_username="@Bite_storee_bot", status="online")
        self.api_key = api_key

    def fetch_products(self) -> List[Product]:
        url = f"{self.base_url}/v1/products?perPage=200"
        headers = {
            "X-API-Key": self.api_key,
            "Accept": "application/json"
        }
        try:
            resp = requests.get(url, headers=headers, timeout=4)
            if resp.status_code == 200:
                data = resp.json()
                raw_items = data.get("products", [])
                products = []
                now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
                now_ts = datetime.now().timestamp()

                for item in raw_items:
                    pid = str(item.get("id", ""))
                    name = item.get("name", "Unknown")
                    # Clean up emojis from raw name if needed
                    clean_name = re.sub(r'<[^>]+>', '', name).strip()
                    price = float(item.get("price", 0.0))
                    stock = int(item.get("stock", 0)) if item.get("inStock") else 0
                    currency = item.get("currency", "USD")
                    desc = item.get("description", "")

                    date_str, ts = extract_post_date(pid, item)
                    if date_str == "غير محدد":
                        date_str, ts = now_str, now_ts

                    products.append(Product(
                        id=f"bite_{pid}",
                        store_name=self.name,
                        name=clean_name,
                        price=price,
                        currency=currency,
                        in_stock=stock,
                        description=desc,
                        updated_at=date_str,
                        timestamp=ts,
                        category="Digital Subscriptions",
                        buy_url=f"https://t.me/Bite_storee_bot?start=buy_{pid}",
                        raw_data=item
                    ))
                return products
            else:
                print(f"[{self.name}] Error status: {resp.status_code}")
                return []
        except Exception as e:
            print(f"[{self.name}] Exception while fetching products: {e}")
            return []
