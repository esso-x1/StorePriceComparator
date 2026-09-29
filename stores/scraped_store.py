import json
import os
from typing import List, Optional
from .base import StoreAdapter, Product

class ScrapedStoreAdapter(StoreAdapter):
    """
    Adapter for stores scraped directly from Telegram bots via Userbot scraper.
    Reads current data from scraped_stores.json or cached memory.
    """
    def __init__(self, name: str, bot_username: str = "", json_file: Optional[str] = None):
        super().__init__(name=name, bot_username=bot_username, status="online")
        if not json_file:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.json_file = os.path.join(base_dir, "scraped_stores.json")
        else:
            self.json_file = json_file

    def fetch_products(self) -> List[Product]:
        if not os.path.exists(self.json_file):
            return []

        try:
            with open(self.json_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            items = data.get(self.name, [])
            products = []
            for item in items:
                p = Product(
                    id=item.get("id", ""),
                    store_name=self.name,
                    name=item.get("name", ""),
                    price=float(item.get("price", 0.0)),
                    currency=item.get("currency", "USDT"),
                    in_stock=int(item.get("in_stock", 1)),
                    description=item.get("description", ""),
                    updated_at=item.get("updated_at", ""),
                    timestamp=float(item.get("timestamp", 0.0)),
                    category=item.get("category", "General"),
                    buy_url=item.get("buy_url", f"https://t.me/{self.bot_username.lstrip('@')}") if self.bot_username else None
                )
                products.append(p)
            return products
        except Exception as e:
            print(f"Error loading scraped products for {self.name}: {e}")
            return []
