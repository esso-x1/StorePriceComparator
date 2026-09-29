import os
import re
import json
import time
import threading
import unicodedata
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any, Optional
try:
    from .stores.base import StoreAdapter, Product, resolve_product_image
except ImportError:
    from stores.base import StoreAdapter, Product, resolve_product_image

CATEGORY_KEYWORDS = {
    "ai": ["gemini", "google ai", "chatgpt", "gpt", "openai", "claude", "midjourney", "deepseek", "copilot", "anthropic"],
    "streaming": ["netflix", "spotify", "youtube", "shahid", "osn", "prime", "disney", "apple music", "crunchyroll", "watchit"],
    "design": ["canva", "capcut", "adobe", "photoshop", "figma", "autodesk", "freepik", "envato", "illustrator"],
    "tools": ["vpn", "duolingo", "notion", "telegram", "discord", "tradingview", "nordvpn", "surfshark", "expressvpn", "office"]
}

# Equivalent term sets for intelligent search
SYNONYM_GROUPS = [
    {"gemini", "google ai", "google ai pro", "google gemini", "google one", "جوجل", "قوقل", "جيمني", "جيميني", "جمناي"},
    {"chatgpt", "chat gpt", "gpt", "gpt4", "gpt-4", "gpt-4o", "openai", "شات جي بي تي"},
    {"claude", "claude 3", "claude pro", "anthropic", "كلود"},
    {"midjourney", "mid journey", "mj", "ميدجورني"},
    {"canva", "كانفا"},
    {"capcut", "كاب كات"},
    {"netflix", "نتفلكس", "نتفليكس"},
    {"spotify", "سبوتيفاي"},
    {"youtube", "yt", "يوتيوب"},
    {"telegram", "tg", "تليجرام", "تيليجرام"},
    {"duolingo", "دولينجو"},
    {"tradingview", "تريدنج فيو"},
    {"notion", "نوشن"},
    {"vpn", "nordvpn", "surfshark", "expressvpn", "في بي ان"}
]

ARABIC_EXPANSIONS = {
    "برو": "pro",
    "بلس": "plus",
    "شات": "chat",
    "ذكاء": "ai",
    "رابط": "link",
    "تفعيل": "activation",
    "حساب": "account",
    "سنة": "1y",
    "شهر": "1m"
}

GENERIC_WORDS = {"account", "link", "pro", "plus", "free", "months", "month", "year", "years", "12", "1", "3", "6", "18", "no", "warranty"}
STORE_KEYWORDS = {"sam", "sams", "insightx", "bite", "acczone", "diginest", "quickdigi", "mops"}

def normalize_search_text(text: str) -> str:
    """Normalize Arabic & English strings, strip diacritics, and expand common tokens"""
    if not text:
        return ""
    text = unicodedata.normalize("NFKD", text)
    text = re.sub(r'[إأآا]', 'ا', text)
    text = re.sub(r'ة', 'ه', text)
    text = re.sub(r'ى', 'ي', text)
    text = re.sub(r'[^a-zA-Z0-9\u0600-\u06FF\s]', ' ', text)
    tokens = text.lower().split()
    expanded = []
    for t in tokens:
        expanded.append(t)
        if t in ARABIC_EXPANSIONS:
            expanded.append(ARABIC_EXPANSIONS[t])
    return " ".join(expanded)

def evaluate_product_match(query: str, product: Product) -> tuple[bool, float, int]:
    """
    Intelligent Substring & Partial Text Matcher.
    Returns: (is_match, score, tier)
      tier 1 = Direct/High-relevance match (exact phrase, entity+qualifiers, or exact synonym)
      tier 2 = Broader/Partial match
    """
    q_norm = normalize_search_text(query)
    if not q_norm:
        return False, 0.0, 2

    name_norm = normalize_search_text(product.name)
    store_norm = normalize_search_text(product.store_name)
    desc_norm = normalize_search_text(product.description or "")
    name_tokens = name_norm.split()
    name_tokens_set = set(name_tokens)

    q_tokens = q_norm.split()
    q_compact = q_norm.replace(" ", "")
    name_compact = name_norm.replace(" ", "")

    # 1. Full Contiguous Substring match in Name (e.g. 'google ai pro' in 'google ai pro 18 months...')
    if q_norm in name_norm or q_compact in name_compact:
        return True, 150.0, 1

    # 2. Store name match ONLY if query mentions store keyword explicitly
    if any(t in STORE_KEYWORDS or t.rstrip('s') in STORE_KEYWORDS for t in q_tokens):
        if any(t.rstrip('s') in store_norm.split() or t.rstrip('s') in store_norm.replace(" ", "") for t in q_tokens if t.rstrip('s') in STORE_KEYWORDS):
            return True, 100.0, 1

    # 3. Check Synonym Group match with entity protection
    target_group = None
    for group in SYNONYM_GROUPS:
        if any(term in q_norm for term in group) or any(t in group for t in q_tokens if t not in GENERIC_WORDS):
            target_group = group
            break

    if target_group:
        prod_in_group = any(term in name_norm for term in target_group) or any(t in target_group for t in name_tokens_set)
        if prod_in_group:
            # Check qualifiers (e.g. 'pro', '18', 'activation')
            qualifiers = [t for t in q_tokens if t not in target_group and t not in {"google", "ai", "gemini", "chatgpt", "gpt", "claude"}]
            if not qualifiers:
                return True, 120.0, 1
            else:
                matched_qualifiers = 0
                for qual in qualifiers:
                    if qual in name_tokens_set:
                        matched_qualifiers += 1
                    elif len(qual) >= 3 and any(qual in t for t in name_tokens_set):
                        matched_qualifiers += 1
                    elif qual in name_compact:
                        matched_qualifiers += 1
                
                if matched_qualifiers >= len(qualifiers):
                    return True, 130.0, 1
                elif matched_qualifiers > 0:
                    return True, 90.0, 1
        else:
            # Belongs to a different entity brand, reject match
            return False, 0.0, 2

    # 4. Multi-token partial/substring search for generic queries
    matched_count = 0
    score = 0.0
    for q_tok in q_tokens:
        if q_tok in name_tokens_set:
            matched_count += 1
            score += 25.0
        elif len(q_tok) >= 3 and any(q_tok in t for t in name_tokens_set):
            matched_count += 1
            score += 20.0
        elif len(q_tok) >= 3 and q_tok in name_compact:
            matched_count += 1
            score += 15.0

    if matched_count == len(q_tokens):
        return True, score, 1
    elif len(q_tokens) >= 3 and matched_count >= (len(q_tokens) - 1):
        return True, score, 2

    return False, 0.0, 2

class PriceAggregator:
    def __init__(self, cache_ttl: int = 60, snapshot_file: str = "cache_snapshot.json"):
        self.stores: List[StoreAdapter] = []
        self.cache_ttl = cache_ttl
        self.snapshot_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), snapshot_file)
        self._memory_cache: Dict[str, List[Product]] = {}
        self._last_refresh_time: float = 0.0
        self._lock = threading.Lock()
        self._is_refreshing: bool = False
        
        # Load snapshot on startup for instant 0.01s initial response
        self._load_snapshot()

    def register_store(self, store: StoreAdapter):
        self.stores.append(store)

    def _load_snapshot(self):
        """Loads cached products from disk snapshot for instant cold startup"""
        if os.path.exists(self.snapshot_file):
            try:
                with open(self.snapshot_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for store_name, items in data.items():
                        prods = []
                        for i in items:
                            prods.append(Product(
                                id=i.get("id", ""),
                                store_name=i.get("store_name", store_name),
                                name=i.get("name", ""),
                                price=float(i.get("price", 0.0)),
                                currency=i.get("currency", "USDT"),
                                in_stock=int(i.get("in_stock", 0)),
                                description=i.get("description", ""),
                                updated_at=i.get("updated_at", ""),
                                timestamp=float(i.get("timestamp", 0.0)),
                                category=i.get("category", "General"),
                                buy_url=i.get("buy_url"),
                                image_url=i.get("image_url")
                            ))
                        self._memory_cache[store_name] = prods
                print(f"Loaded {len(self._memory_cache)} stores from disk snapshot.")
            except Exception as e:
                print(f"Failed to load cache snapshot: {e}")

    def _save_snapshot(self):
        """Saves active memory cache to disk snapshot atomically and safely"""
        try:
            serialized = {}
            with self._lock:
                for store_name, products in self._memory_cache.items():
                    if products:
                        serialized[store_name] = [p.to_dict() for p in products]
            if not serialized:
                return  # Never overwrite snapshot with empty content

            tmp_file = f"{self.snapshot_file}.tmp"
            with open(tmp_file, "w", encoding="utf-8") as f:
                json.dump(serialized, f, ensure_ascii=False, indent=2)
            os.replace(tmp_file, self.snapshot_file)
        except Exception as e:
            print(f"Failed to save snapshot: {e}")

    def _fetch_single_store_safe(self, store: StoreAdapter) -> List[Product]:
        """Safely fetch products from a single store with error isolation"""
        try:
            return store.fetch_products()
        except Exception as e:
            print(f"Error fetching from {store.name}: {e}")
            with self._lock:
                return self._memory_cache.get(store.name, [])

    def refresh_cache_now(self, async_mode: bool = True):
        """Refreshes all stores concurrently without blocking caller"""
        if self._is_refreshing:
            return
        
        def _run_refresh():
            self._is_refreshing = True
            try:
                # Concurrent fetch with worker pool
                with ThreadPoolExecutor(max_workers=max(len(self.stores), 1)) as executor:
                    future_to_store = {
                        executor.submit(self._fetch_single_store_safe, s): s.name 
                        for s in self.stores
                    }
                    
                    for future in as_completed(future_to_store):
                        store_name = future_to_store[future]
                        try:
                            products = future.result()
                            if products:
                                with self._lock:
                                    self._memory_cache[store_name] = products
                        except Exception as e:
                            print(f"Store {store_name} worker error: {e}")
                
                self._last_refresh_time = time.time()
                self._save_snapshot()
            finally:
                self._is_refreshing = False

        if async_mode:
            t = threading.Thread(target=_run_refresh, daemon=True)
            t.start()
        else:
            _run_refresh()

    def start_background_worker(self, interval: int = 60):
        """Runs a continuous background daemon that refreshes stores periodically"""
        def worker_loop():
            # Initial background warm up
            time.sleep(2)
            while True:
                self.refresh_cache_now(async_mode=False)
                time.sleep(interval)

        thread = threading.Thread(target=worker_loop, daemon=True)
        thread.start()

    def get_stores_info(self) -> List[Dict[str, Any]]:
        """Returns metadata for all stores instantly from memory (< 1ms)"""
        now = time.time()
        # Trigger background refresh if stale
        if (now - self._last_refresh_time) > self.cache_ttl:
            self.refresh_cache_now(async_mode=True)

        info = []
        for s in self.stores:
            bot_tag = getattr(s, "bot_username", "")
            with self._lock:
                products = self._memory_cache.get(s.name, [])
            in_stock_count = len([p for p in products if p.in_stock > 0 and p.price > 0])
            
            status = "online" if in_stock_count > 0 else "offline"
            status_text = "نشط" if in_stock_count > 0 else getattr(s, "default_status", "غير نشط")

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
        """Returns the latest products for a store instantly from memory (< 1ms)"""
        target_store = next((s for s in self.stores if s.name.lower() == store_name.lower()), None)
        if not target_store:
            return {"error": "المتجر غير موجود", "items": []}

        with self._lock:
            products = self._memory_cache.get(target_store.name, [])
            
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
        """Returns all products in memory instantly"""
        all_products = []
        with self._lock:
            for s_name, prods in self._memory_cache.items():
                if not enabled_stores or s_name in enabled_stores:
                    all_products.extend(prods)
        return all_products

    def search_and_compare(
        self, 
        query: str = "", 
        enabled_stores: Optional[List[str]] = None,
        category: Optional[str] = None,
        sort_by: str = "price_asc"
    ) -> Dict[str, Any]:
        """
        Ultra-fast instant search executed 100% in-memory (< 2ms).
        Supports query keywords, category filtering, and sorting.
        """
        # Auto-trigger refresh in background if cache is stale
        now = time.time()
        if (now - self._last_refresh_time) > self.cache_ttl:
            self.refresh_cache_now(async_mode=True)

        query_str = query.strip()
        all_products = self.fetch_all(enabled_stores)
        
        # If no query and no category, return empty results (initial state)
        if not query_str and (not category or category == "all"):
            return {
                "query": "",
                "best_deal": None,
                "stores_with_item": [],
                "store_comparison": {},
                "stats": {},
                "results": []
            }

        matched_with_meta: List[tuple[Product, float, int]] = []

        # Category keyword match
        cat_keywords = CATEGORY_KEYWORDS.get(category.lower(), []) if category and category != "all" else []

        for p in all_products:
            if p.in_stock <= 0 or p.price <= 0:
                continue

            name_clean = normalize_search_text(p.name)
            name_tokens = set(name_clean.split())
            name_compact = "".join(name_clean.split())

            # Category filter check if category is specified
            if cat_keywords:
                matches_cat = any(kw in name_compact or kw in name_tokens for kw in cat_keywords)
                if not matches_cat:
                    continue

            # Intelligent query match
            if query_str:
                is_match, score, tier = evaluate_product_match(query_str, p)
                if not is_match:
                    continue
                matched_with_meta.append((p, score, tier))
            else:
                # If only category was selected without query
                matched_with_meta.append((p, 50.0, 1))

        # Sorting logic: Direct matches (tier 1) prioritized over broad matches (tier 2),
        # then sorted according to user selection
        if sort_by == "date_desc":
            matched_with_meta.sort(key=lambda x: (x[2], -x[0].timestamp, x[0].price))
        elif sort_by == "stock_desc":
            matched_with_meta.sort(key=lambda x: (x[2], -x[0].in_stock, x[0].price))
        else: # default: price_asc
            matched_with_meta.sort(key=lambda x: (x[2], x[0].price, -x[0].timestamp))

        matched = [item[0] for item in matched_with_meta]

        stores_with_item = list(dict.fromkeys([p.store_name for p in matched]))
        best_deal = matched[0].to_dict() if matched else None

        # Build comparison summary per store
        store_comparison = {}
        for s_name in stores_with_item:
            store_items = [p for p in matched if p.store_name == s_name]
            if store_items:
                cheapest_in_store = sorted(store_items, key=lambda x: x.price)[0]
                store_comparison[s_name] = {
                    "lowest_price": cheapest_in_store.price,
                    "currency": cheapest_in_store.currency,
                    "item_name": cheapest_in_store.name,
                    "in_stock": cheapest_in_store.in_stock,
                    "updated_at": cheapest_in_store.updated_at,
                    "buy_url": cheapest_in_store.buy_url,
                    "total_offers": len(store_items)
                }

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
            "category": category,
            "sort_by": sort_by,
            "best_deal": best_deal,
            "stores_with_item": stores_with_item,
            "store_comparison": store_comparison,
            "stats": stats,
            "results": [p.to_dict() for p in matched]
        }
