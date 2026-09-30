import os
import json
import requests
from typing import List, Optional
try:
    from .base import StoreAdapter, Product, extract_post_date
except ImportError:
    from base import StoreAdapter, Product, extract_post_date

class VerifierStoreAdapter(StoreAdapter):
    """
    Adapter for Verifier Store (@Veriyferbot / Duskyr API).
    Supports live API with automatic fallback to local scraped snapshot.
    """
    def __init__(
        self, 
        api_key: str = "dsk_live_KBEIWn2u-CpDY5d0a5Eoq5ph7jKc2vyQZkAxlJiMaBA", 
        base_url: str = "https://duskyr.com/api/v1", 
        bot_username: str = "@Veriyferbot"
    ):
        super().__init__(name="Verifier Store", base_url=base_url, bot_username=bot_username, status="online")
        self.api_key = api_key
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.scraped_file = os.path.join(base_dir, "scraped_stores.json")

    def fetch_products(self) -> List[Product]:
        # 1. Try Direct API
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json"
        }
        url = f"{self.base_url}/products"
        try:
            resp = requests.get(url, headers=headers, timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                raw_items = data if isinstance(data, list) else (data.get("products") or data.get("data") or [])
                products = []
                for item in raw_items:
                    pid = str(item.get("id", ""))
                    name = item.get("name", "Unknown")
                    price = float(item.get("price_usdt") or item.get("price", 0.0))
                    in_stock = int(item.get("in_stock", 1)) if item.get("available", True) else 0
                    date_str, ts = extract_post_date(pid, item)
                    products.append(Product(
                        id=f"verifier_{pid}",
                        store_name=self.name,
                        name=name,
                        price=price,
                        currency="USDT",
                        in_stock=in_stock,
                        description=item.get("description", ""),
                        updated_at=date_str,
                        timestamp=ts,
                        category=item.get("category", "Digital Accounts"),
                        buy_url=f"https://t.me/Veriyferbot?start=buy_{pid}",
                        raw_data=item
                    ))
                if products:
                    return products
        except Exception as e:
            pass

        # 2. Fallback to Scraped Stores JSON
        if os.path.exists(self.scraped_file):
            try:
                with open(self.scraped_file, "r", encoding="utf-8") as f:
                    scraped_data = json.load(f)
                items = scraped_data.get(self.name, [])
                products = []
                for item in items:
                    pid = str(item.get("id", ""))
                    products.append(Product(
                        id=pid,
                        store_name=self.name,
                        name=item.get("name", ""),
                        price=float(item.get("price", 0.0)),
                        currency=item.get("currency", "USDT"),
                        in_stock=int(item.get("in_stock", 1)),
                        description=item.get("description", ""),
                        updated_at=item.get("updated_at", ""),
                        timestamp=float(item.get("timestamp", 0.0)),
                        category=item.get("category", "Digital Accounts"),
                        buy_url=item.get("buy_url", "https://t.me/Veriyferbot")
                    ))
                return products
            except Exception:
                pass

        return []
