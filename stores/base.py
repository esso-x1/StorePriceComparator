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

BRAND_ICONS = {
    "gemini": "https://upload.wikimedia.org/wikipedia/commons/8/8a/Google_Gemini_logo.svg",
    "google ai": "https://upload.wikimedia.org/wikipedia/commons/8/8a/Google_Gemini_logo.svg",
    "chatgpt": "https://upload.wikimedia.org/wikipedia/commons/0/04/ChatGPT_logo.svg",
    "gpt": "https://upload.wikimedia.org/wikipedia/commons/0/04/ChatGPT_logo.svg",
    "openai": "https://upload.wikimedia.org/wikipedia/commons/0/04/ChatGPT_logo.svg",
    "claude": "https://upload.wikimedia.org/wikipedia/commons/7/78/Anthropic_logo.svg",
    "midjourney": "https://upload.wikimedia.org/wikipedia/commons/e/e6/Midjourney_Emblem.png",
    "canva": "https://upload.wikimedia.org/wikipedia/commons/0/08/Canva_icon_2021.svg",
    "capcut": "https://upload.wikimedia.org/wikipedia/commons/a/af/Capcut-icon.svg",
    "duolingo": "https://upload.wikimedia.org/wikipedia/commons/1/15/Duolingo_logo.svg",
    "spotify": "https://upload.wikimedia.org/wikipedia/commons/8/84/Spotify_icon.svg",
    "netflix": "https://upload.wikimedia.org/wikipedia/commons/0/08/Netflix_2015_logo.svg",
    "youtube": "https://upload.wikimedia.org/wikipedia/commons/0/09/YouTube_full-color_icon_%282017%29.svg",
    "notion": "https://upload.wikimedia.org/wikipedia/commons/e/e9/Notion-logo.svg",
    "autodesk": "https://upload.wikimedia.org/wikipedia/commons/d/d7/Autodesk_Logo_2021.svg",
    "telegram": "https://upload.wikimedia.org/wikipedia/commons/8/82/Telegram_logo.svg",
    "discord": "https://upload.wikimedia.org/wikipedia/commons/6/6b/Font_Awesome_5_brands_discord_color.svg",
    "apple": "https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_logo_black.svg",
    "adobe": "https://upload.wikimedia.org/wikipedia/commons/8/8d/Adobe_Corporate_Logo.png",
    "tradingview": "https://upload.wikimedia.org/wikipedia/commons/2/23/TradingView_Logo.svg",
    "shahid": "https://upload.wikimedia.org/wikipedia/commons/b/ba/Shahid_VIP_Logo.svg",
    "vpn": "https://upload.wikimedia.org/wikipedia/commons/7/7e/OOjs_UI_icon_key-ltr.svg",
}

def resolve_product_image(name: str, raw_item: Optional[Dict[str, Any]] = None) -> str:
    """Extracts image from API raw_item or resolves the brand icon from the product title."""
    if raw_item and isinstance(raw_item, dict):
        for field in ["image", "image_url", "imageUrl", "photo", "photo_url", "thumbnail", "thumb", "img", "logo", "banner"]:
            val = raw_item.get(field)
            if val and isinstance(val, str) and (val.startswith("http://") or val.startswith("https://")):
                return val

    name_lower = name.lower()
    for brand, icon_url in BRAND_ICONS.items():
        if brand in name_lower:
            return icon_url
    
    # Elegant fallback gradient icon for general digital goods
    return "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=150&auto=format&fit=crop&q=80"

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
    image_url: Optional[str] = None
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
            "buy_url": self.buy_url,
            "image_url": self.image_url or resolve_product_image(self.name, self.raw_data)
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
