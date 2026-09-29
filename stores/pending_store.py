from typing import List
from .base import StoreAdapter, Product

class PendingStoreAdapter(StoreAdapter):
    """Adapter for stores that are pending API URL or currently offline"""
    def __init__(self, name: str, bot_username: str, status_label: str = "غير نشط", api_key: str = "", base_url: str = ""):
        super().__init__(name=name, base_url=base_url, bot_username=bot_username, status=status_label)
        self.status_label = status_label
        self.api_key = api_key

    def fetch_products(self) -> List[Product]:
        return []
