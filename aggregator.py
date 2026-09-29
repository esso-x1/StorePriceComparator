import re
import time
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict, Any, Optional
try:
    from .stores.base import StoreAdapter, Product
except ImportError:
    from stores.base import StoreAdapter, Product

class PriceAggregator:
    def __init__(self, cache_ttl: int = 45):
        self.stores: List[StoreAdapter] = []
        self.cache_ttl = cache_ttl
        self._cache: Dict[str, tuple[float, List[Product]]] = {}

    def register_store(self, store: StoreAdapter):
        self.stores.append(store)

    def clear_cache(self):
        self._cache.clear()

    def _fetch_single_store(self, store: StoreAdapter) -> List[Product]:
        now = time.time()
        cached = self._cache.get(store.name)
        if cached and (now - cached[0]) < self.cache_ttl:
            return cached[1]

        try:
            products = store.fetch_products()
            self._cache[store.name] = (now, products)
            return products
        except Exception as e:
            print(f"Error fetching from {store.name}: {e}")
            if cached:
                return cached[1] # fallback to stale cache on network glitch
            return []

    def get_stores_info(self) -> List[Dict[str, Any]]:
        """Returns metadata for ALL stores (active and inactive) for the sidebar"""
        # Fetch concurrently
        with ThreadPoolExecutor(max_workers=max(len(self.stores), 1)) as executor:
            store_prods = list(executor.map(self._fetch_single_store, self.stores))

        info = []
        for s, products in zip(self.stores, store_prods):
            bot_tag = getattr(s, "bot_username", "")
            in_stock_count = len([p for p in products if p.in_stock > 0])
            if in_stock_count > 0:
                status = "online"
                status_text = "نشط"
            else:
                status = "offline"
                status_text = getattr(s, "default_status", "غير نشط")

            info.append({
                "name": s.name,
                "bot_username": bot_tag,
                "status": status,
                "status_text": status_text,
                "product_count": in_stock_count,
                "base_url": s.base_url
            })
        return info

    def get_store_feed(self, store_name: str) -> Dict[str, Any]:
        """Returns the latest products/notifications for a specific store, sorted by newest first"""
        target_store = next((s for s in self.stores if s.name.lower() == store_name.lower()), None)
        if not target_store:
            return {"error": "المتجر غير موجود", "items": []}
        
        products = self._fetch_single_store(target_store)
        valid_products = [p for p in products if p.in_stock > 0 and p.price > 0]
        # Sort by newest timestamp first, then lower price
        valid_products.sort(key=lambda x: (-x.timestamp, x.price))
        
        return {
            "store_name": target_store.name,
            "bot_username": getattr(target_store, "bot_username", ""),
            "total_items": len(valid_products),
            "items": [p.to_dict() for p in valid_products]
        }

    def fetch_all(self, enabled_stores: Optional[List[str]] = None) -> List[Product]:
        target_stores = [
            s for s in self.stores 
            if not enabled_stores or s.name in enabled_stores
        ]
        
        with ThreadPoolExecutor(max_workers=max(len(target_stores), 1)) as executor:
            results = list(executor.map(self._fetch_single_store, target_stores))

        all_products = []
        for prods in results:
            all_products.extend(prods)
        return all_products

    def search_and_compare(self, query: str = "", enabled_stores: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Searches strictly by query without showing unqueried products.
        Filters out 0 stock, matches product name & category,
        and ranks by lowest price based on latest post dates.
        """
        query_str = query.strip()
        # If no query was submitted, return empty results (do not show unqueried items)
        if not query_str:
            return {
                "query": "",
                "best_deal": None,
                "stores_with_item": [],
                "store_comparison": {},
                "stats": {},
                "results": []
            }

        all_products = self.fetch_all(enabled_stores)
        query_tokens = [t.lower() for t in re.split(r'\s+', query_str) if t]

        matched: List[Product] = []
        for p in all_products:
            # 1. Ignore items that are out of stock or price <= 0
            if p.in_stock <= 0 or p.price <= 0:
                continue
            
            # 2. Strict matching exclusively on Product Name (ignore generic category strings)
            # Remove symbols/emojis and keep letters, numbers, and arabic
            name_clean = re.sub(r'[^a-zA-Z0-9\u0600-\u06FF\s]', ' ', p.name).lower()
            name_tokens = set(name_clean.split())
            name_compact = "".join(name_clean.split())

            is_match = True
            for q_tok in query_tokens:
                q_compact = "".join(q_tok.split())
                # Exact token match or substring in compact name
                if q_tok in name_tokens or q_compact in name_compact:
                    continue
                # Match partial word if token length >= 3
                if len(q_tok) >= 3 and any(q_tok in t for t in name_tokens):
                    continue
                # Acronym support: "gpt" matches "chatgpt"
                if q_tok == "gpt" and ("chatgpt" in name_compact or "gpt" in name_tokens):
                    continue
                # Synonym support: "gemini" matches "google ai" (e.g. Sam Topup's Google AI Pro)
                if q_tok == "gemini" and ("google" in name_tokens and "ai" in name_tokens):
                    continue
                is_match = False
                break

            if is_match:
                matched.append(p)

        # 3. Sort: Lowest price first, then newest date/timestamp first
        matched.sort(key=lambda x: (x.price, -x.timestamp))

        # Identify all stores that carry this item
        stores_with_item = list(dict.fromkeys([p.store_name for p in matched]))

        # Best offer in the whole search
        best_deal = matched[0].to_dict() if matched else None

        # Build comparison summary per store (each store's lowest price for this item)
        store_comparison = {}
        for s_name in stores_with_item:
            store_items = [p for p in matched if p.store_name == s_name]
            if store_items:
                cheapest_in_store = store_items[0]
                store_comparison[s_name] = {
                    "lowest_price": cheapest_in_store.price,
                    "currency": cheapest_in_store.currency,
                    "item_name": cheapest_in_store.name,
                    "in_stock": cheapest_in_store.in_stock,
                    "updated_at": cheapest_in_store.updated_at,
                    "buy_url": cheapest_in_store.buy_url,
                    "total_offers": len(store_items)
                }

        # Calculate statistics
        stats = {}
        if matched:
            min_price = matched[0].price
            max_price = matched[-1].price
            savings = round(max_price - min_price, 2)
            savings_pct = round(((max_price - min_price) / max_price * 100), 1) if max_price > 0 else 0
            stats = {
                "lowest_price": min_price,
                "highest_price": max_price,
                "savings": savings,
                "savings_percentage": savings_pct,
                "total_results": len(matched),
                "stores_count": len(stores_with_item)
            }

        return {
            "query": query_str,
            "best_deal": best_deal,
            "stores_with_item": stores_with_item,
            "store_comparison": store_comparison,
            "stats": stats,
            "results": [p.to_dict() for p in matched]
        }
