from dataclasses import dataclass
from typing import Optional, List, Dict, Any, Tuple
from abc import ABC, abstractmethod
from datetime import datetime

def extract_post_date(item_id: str, raw_item: Optional[Dict[str, Any]] = None) -> Tuple[str, float]:
    """
    Extracts the true post creation date from the store item.
    Checks explicit date fields, or decodes the 24-char MongoDB ObjectId timestamp.
    """
    if raw_item and isinstance(raw_item, dict):
        for field in ["createdAt", "created_at", "updatedAt", "updated_at", "date", "post_date"]:
            val = raw_item.get(field)
            if val:
                try:
                    if isinstance(val, (int, float)):
                        dt = datetime.fromtimestamp(val if val < 1e11 else val / 1000)
                        return dt.strftime("%Y-%m-%d %H:%M"), dt.timestamp()
                    dt = datetime.fromisoformat(str(val).replace('Z', '+00:00'))
                    return dt.strftime("%Y-%m-%d %H:%M"), dt.timestamp()
                except Exception:
                    pass
    
    # Try decoding MongoDB ObjectId timestamp (first 8 hex chars = unix timestamp)
    clean_id = str(item_id).strip()
    if len(clean_id) >= 8:
        try:
            ts = int(clean_id[:8], 16)
            # Timestamp between years 2020 and 2030
            if 1577836800 <= ts <= 1893456000:
                dt = datetime.fromtimestamp(ts)
                return dt.strftime("%Y-%m-%d %H:%M"), dt.timestamp()
        except Exception:
            pass

    return "غير محدد", 0.0

@dataclass
class Product:
    id: str
    store_name: str
    name: str
    price: float
    currency: str = "USDT"
    in_stock: int = 0
    description: str = ""
    updated_at: str = ""
    timestamp: float = 0.0
    category: str = "General"
    buy_url: Optional[str] = None
    raw_data: Optional[Dict[str, Any]] = None

    def to_dict(self):
        return {
            "id": self.id,
            "store_name": self.store_name,
            "name": self.name,
            "price": self.price,
            "currency": self.currency,
            "in_stock": self.in_stock,
            "description": self.description,
            "updated_at": self.updated_at,
            "timestamp": self.timestamp,
            "category": self.category,
            "buy_url": self.buy_url
        }

class StoreAdapter(ABC):
    def __init__(self, name: str, base_url: str = "", bot_username: str = "", status: str = "online"):
        self.name = name
        self.base_url = base_url
        self.bot_username = bot_username
        self.default_status = status

    @abstractmethod
    def fetch_products(self) -> List[Product]:
        """Fetch all available products from the store"""
        pass

    def search(self, query: str) -> List[Product]:
        """Filter products locally by query in title or category"""
        products = self.fetch_products()
        query = query.lower().strip()
        if not query:
            return []
        return [p for p in products if query in p.name.lower() or query in p.category.lower()]
