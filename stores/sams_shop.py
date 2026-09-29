import requests
from datetime import datetime
from typing import List
try:
    from .base import StoreAdapter, Product, extract_post_date
except ImportError:
    from base import StoreAdapter, Product, extract_post_date

class SamsShopAdapter(StoreAdapter):
    def __init__(self, api_key: str = "sam_e194c2588b00516996029a20e258bf7764aa5c3ae74b22d4a5f4c716255a486e"):
        super().__init__(name="Sam Topup", base_url="https://sams-u7kj.onrender.com/api/v1", bot_username="@Samsshop_bot")
        self.api_key = api_key

    def fetch_products(self) -> List[Product]:
        url = f"{self.base_url}/products"
        headers = {
            "x-api-key": self.api_key,
            "Accept": "application/json"
        }
        for attempt in range(2):
            try:
                resp = requests.get(url, headers=headers, timeout=10)
                if resp.status_code == 200:
                    data = resp.json()
                    items = data.get("products", [])
                    products = []
                    for item in items:
                        pid = str(item.get("id"))
                        date_str, ts = extract_post_date(pid, item)
                        products.append(Product(
                            id=pid,
                            store_name=self.name,
                            name=item.get("name", "Unknown"),
                            price=float(item.get("price", 0.0)),
                            currency="USDT",
                            in_stock=int(item.get("inStock", 0)),
                            description=item.get("description", ""),
                            updated_at=date_str,
                            timestamp=ts,
                            buy_url=f"https://t.me/Samsshop_bot?start=buy_{pid}",
                            raw_data=item
                        ))
                    return products
                else:
                    print(f"[{self.name}] Error status: {resp.status_code} - {resp.text}")
            except Exception as e:
                if attempt == 1:
                    print(f"[{self.name}] Exception while fetching products: {e}")
        return []

    def get_balance(self) -> float:
        url = f"{self.base_url}/balance"
        headers = {"x-api-key": self.api_key}
        try:
            resp = requests.get(url, headers=headers, timeout=10)
            if resp.status_code == 200:
                return float(resp.json().get("balance", 0.0))
        except Exception:
            pass
        return 0.0
