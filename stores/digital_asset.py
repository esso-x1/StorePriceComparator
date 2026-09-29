import requests
from datetime import datetime
from typing import List
try:
    from .base import StoreAdapter, Product, extract_post_date
except ImportError:
    from base import StoreAdapter, Product, extract_post_date

class DigitalAssetAdapter(StoreAdapter):
    def __init__(self, api_key: str = "rk_live_UtCaFiQCiztkP7pZBc-hHs04RJJKSxoJ9DKNlncCrEo"):
        super().__init__(name="Digital Asset", base_url="https://digital-assets-api.pe-supplykh.com/api/v1", bot_username="@digital_assetbot")
        self.api_key = api_key

    def fetch_products(self) -> List[Product]:
        url = f"{self.base_url}/products"
        headers = {
            "x-api-key": self.api_key,
            "Accept": "application/json"
        }
        try:
            resp = requests.get(url, headers=headers, timeout=12)
            if resp.status_code == 200:
                data = resp.json()
                items = data.get("data", [])
                products = []
                for group in items:
                    cat_name = group.get("name", "")
                    group_id = str(group.get("id", ""))
                    date_str, ts = extract_post_date(group_id, group)
                    description = group.get("description") or f"Category: {cat_name}"
                    for v in group.get("variations", []):
                        full_name = f"{cat_name} - {v.get('name')}"
                        stock_val = v.get("stock")
                        in_stock = int(stock_val) if stock_val is not None else 99
                        products.append(Product(
                            id=f"{group_id}_{v.get('id')}",
                            store_name=self.name,
                            name=full_name,
                            price=float(v.get("price", 0.0)),
                            currency="USD",
                            in_stock=in_stock,
                            description=description,
                            updated_at=date_str,
                            timestamp=ts,
                            category=group.get("category", "General"),
                            buy_url=f"https://t.me/digital_assetbot?start=buy_{clean_id}",
                            raw_data=v
                        ))
                return products
            else:
                print(f"[{self.name}] Error status: {resp.status_code}")
                return []
        except Exception as e:
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
