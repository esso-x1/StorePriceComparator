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
    from .database import (
        record_observation, 
        get_product_history, 
        get_multi_merchant_comparison,
        seed_initial_history_if_needed,
        check_and_evaluate_alerts
    )
    from .catalog import classify_product, build_catalog_hierarchy, CATEGORIES
except ImportError:
    from stores.base import StoreAdapter, Product, resolve_product_image
    import database
    from database import (
        record_observation, 
        get_product_history, 
        get_multi_merchant_comparison,
        seed_initial_history_if_needed,
        check_and_evaluate_alerts
    )
    from catalog import classify_product, build_catalog_hierarchy, CATEGORIES

STORE_HANDLES = {
    "Gemini Pixel Extractor": "@GeminiPixel1_bot",
    "AI Shop Mops": "@aishopmopsbot",
    "QuickDigi Store": "@QuickDigiBot",
    "DIGINEST Store": "@DIGINEST1BOT",
    "PA Store": "@pastore_bot",
    "InsightX Pro": "@insightx_bot",
    "Sam Topup": "@SamTopupBot",
    "Acczone Store": "@acczone_bot",
    "Bite Store": "@BiteStoreBot",
    "Digital Socials": "@DigitalSocialsBot",
    "Digital Asset": "@digitalasset_bot",
    "Verifier Store": "@Veriyferbot"
}

def get_store_initials(name: str) -> str:
    """Deterministic 2-letter uppercase initials for avatar badge"""
    clean = re.sub(r'(?i)\b(Store|Shop|Extractor|Pro|Topup|Asset|Socials)\b', '', name).strip()
    parts = clean.split()
    if len(parts) >= 2:
        return (parts[0][0] + parts[1][0]).upper()
    elif len(clean) >= 2:
        return clean[:2].upper()
    return name[:2].upper()

CATEGORY_KEYWORDS = {
    "ai": ["gemini", "google ai", "chatgpt", "gpt", "openai", "claude", "midjourney", "deepseek", "copilot", "anthropic", "perplexity", "cursor", "grok", "elevenlabs", "lovable", "replit"],
    "streaming": ["netflix", "spotify", "youtube", "shahid", "osn", "prime", "disney", "apple music", "crunchyroll", "watchit"],
    "design": ["canva", "capcut", "adobe", "photoshop", "figma", "autodesk", "freepik", "envato", "illustrator"],
    "productivity": ["vpn", "duolingo", "notion", "telegram", "discord", "tradingview", "nordvpn", "surfshark", "expressvpn", "office", "outlook", "hotmail", "mail"],
    "tools": ["vpn", "duolingo", "notion", "telegram", "discord", "tradingview", "nordvpn", "surfshark", "expressvpn", "office"]
}

SYNONYM_GROUPS = [
    {"gemini", "google ai", "google ai pro", "google gemini", "google one", "جوجل", "قوقل", "جيمني", "جيميني", "جمناي"},
    {"chatgpt", "chat gpt", "gpt", "gpt4", "gpt-4", "gpt-4o", "openai", "شات جي بي تي"},
    {"claude", "claude 3", "claude pro", "anthropic", "كلود"},
    {"perplexity", "بيربلكسيتي"},
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
STORE_KEYWORDS = {"sam", "sams", "insightx", "bite", "acczone", "diginest", "quickdigi", "mops", "verifier", "gemini"}

def normalize_search_text(text: str) -> str:
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
    q_norm = normalize_search_text(query)
    if not q_norm:
        return False, 0.0, 2

    name_norm = normalize_search_text(product.name)
    store_norm = normalize_search_text(product.store_name)
    name_tokens = name_norm.split()
    name_tokens_set = set(name_tokens)

    q_tokens = q_norm.split()
    q_compact = q_norm.replace(" ", "")
    name_compact = name_norm.replace(" ", "")

    if q_norm in name_norm or q_compact in name_compact:
        return True, 150.0, 1

    if any(t in STORE_KEYWORDS or t.rstrip('s') in STORE_KEYWORDS for t in q_tokens):
        if any(t.rstrip('s') in store_norm.split() or t.rstrip('s') in store_norm.replace(" ", "") for t in q_tokens if t.rstrip('s') in STORE_KEYWORDS):
            return True, 100.0, 1

    target_group = None
    for group in SYNONYM_GROUPS:
        if any(term in q_norm for term in group) or any(t in group for t in q_tokens if t not in GENERIC_WORDS):
            target_group = group
            break

    if target_group:
        prod_in_group = any(term in name_norm for term in target_group) or any(t in target_group for t in name_tokens_set)
        if prod_in_group:
            qualifiers = [t for t in q_tokens if t not in target_group and t not in {"google", "ai", "gemini", "chatgpt", "gpt", "claude"}]
            if not qualifiers:
                return True, 120.0, 1
            else:
                matched_qualifiers = 0
                for qual in qualifiers:
                    if qual in name_tokens_set or (len(qual) >= 3 and any(qual in t for t in name_tokens_set)) or qual in name_compact:
                        matched_qualifiers += 1
                if matched_qualifiers >= len(qualifiers):
                    return True, 130.0, 1
                elif matched_qualifiers > 0:
                    return True, 90.0, 1
        else:
            return False, 0.0, 2

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
        
        self._load_snapshot()

    def register_store(self, store: StoreAdapter):
        self.stores.append(store)

    def _load_snapshot(self):
        """Loads cached products from disk snapshot and seeds DB history"""
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
                seed_initial_history_if_needed(self._memory_cache)
            except Exception as e:
                print(f"Failed to load cache snapshot: {e}")

    def _save_snapshot(self):
        """Saves active memory cache to disk snapshot atomically and logs price changes"""
        try:
            serialized = {}
            with self._lock:
                for store_name, products in self._memory_cache.items():
                    if products:
                        serialized[store_name] = [p.to_dict() for p in products]
            if not serialized:
                return

            tmp_file = f"{self.snapshot_file}.tmp"
            with open(tmp_file, "w", encoding="utf-8") as f:
                json.dump(serialized, f, ensure_ascii=False, indent=2)
            os.replace(tmp_file, self.snapshot_file)

            # Record latest prices into SQLite price_history
            for store_name, products in serialized.items():
                for p in products:
                    if float(p.get("price", 0)) > 0:
                        record_observation(
                            merchant_name=store_name,
                            product_id=p.get("id", ""),
                            product_name=p.get("name", ""),
                            price=float(p.get("price", 0)),
                            currency=p.get("currency", "USDT"),
                            in_stock=int(p.get("in_stock", 0)),
                            category=p.get("category", ""),
                            variant=p.get("name", "")
                        )
            # Evaluate price alerts
            all_prods = self.fetch_all()
            check_and_evaluate_alerts(all_prods)
        except Exception as e:
            print(f"Failed to save snapshot: {e}")

    def _fetch_single_store_safe(self, store: StoreAdapter) -> List[Product]:
        try:
            return store.fetch_products()
        except Exception as e:
            print(f"Error fetching from {store.name}: {e}")
            with self._lock:
                return self._memory_cache.get(store.name, [])

    def refresh_cache_now(self, async_mode: bool = True):
        if self._is_refreshing:
            return
        
        def _run_refresh():
            self._is_refreshing = True
            try:
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
        def worker_loop():
            time.sleep(2)
            while True:
                self.refresh_cache_now(async_mode=False)
                time.sleep(interval)

        thread = threading.Thread(target=worker_loop, daemon=True)
        thread.start()

    def get_stores_info(self) -> List[Dict[str, Any]]:
        info = []
        for s in self.stores:
            bot_tag = getattr(s, "bot_username", STORE_HANDLES.get(s.name, ""))
            with self._lock:
                products = self._memory_cache.get(s.name, [])
            in_stock_count = len([p for p in products if p.in_stock > 0 and p.price > 0])
            
            status = "online" if in_stock_count > 0 else "offline"
            status_text = "نشط" if in_stock_count > 0 else getattr(s, "default_status", "غير نشط")

            info.append({
                "name": s.name,
                "bot_username": bot_tag,
                "initials": get_store_initials(s.name),
                "status": status,
                "status_text": status_text,
                "product_count": in_stock_count,
                "base_url": s.base_url or f"https://t.me/{bot_tag.lstrip('@')}"
            })
        return info

    def get_store_feed(self, store_name: str) -> Dict[str, Any]:
        target_store = next((s for s in self.stores if s.name.lower() == store_name.lower()), None)
        if not target_store:
            return {"error": "المتجر غير موجود", "items": []}

        with self._lock:
            products = self._memory_cache.get(target_store.name, [])
            
        valid_products = [p for p in products if p.in_stock > 0 and p.price > 0]
        valid_products.sort(key=lambda x: (-x.timestamp, x.price))

        return {
            "store_name": target_store.name,
            "bot_username": getattr(target_store, "bot_username", STORE_HANDLES.get(target_store.name, "")),
            "initials": get_store_initials(target_store.name),
            "total_items": len(valid_products),
            "items": [p.to_dict() for p in valid_products]
        }

    def fetch_all(self, enabled_stores: Optional[List[str]] = None) -> List[Product]:
        all_products = []
        with self._lock:
            for s_name, prods in self._memory_cache.items():
                if not enabled_stores or s_name in enabled_stores:
                    all_products.extend(prods)
        return all_products

    def get_catalog_hierarchy(self) -> Dict[str, Any]:
        return build_catalog_hierarchy(self.fetch_all())

    def search_and_compare(
        self, 
        query: str = "", 
        enabled_stores: Optional[List[str]] = None,
        category: Optional[str] = None,
        product_family: Optional[str] = None,
        plan_duration: Optional[str] = None,
        sort_by: str = "lowest_price"
    ) -> Dict[str, Any]:
        """
        High-performance comparison engine matching the visual requirements:
        Dependent filters: Category -> Product Family -> Plan Duration -> Comparable offers.
        """
        now = time.time()
        if (now - self._last_refresh_time) > self.cache_ttl:
            self.refresh_cache_now(async_mode=True)

        query_str = query.strip()
        all_products = self.fetch_all(enabled_stores)
        
        # If no filter at all, default to showing AI group (Gemini/ChatGPT) so the primary dashboard
        # immediately exposes comparison controls and actual offers as required
        if not query_str and (not category or category == "all") and not product_family and not plan_duration:
            category = "ai"
            product_family = "Google Gemini"

        matched_with_meta: List[tuple[Product, float, int, str, str, str, List[str]]] = []

        for p in all_products:
            if p.in_stock <= 0 or p.price <= 0:
                continue

            cat_id, fam, duration, tags = classify_product(p.name, p.category)

            # Category filter
            if category and category != "all" and cat_id != category:
                continue

            # Product family filter
            if product_family and product_family != "all" and fam.lower() != product_family.lower():
                continue

            # Plan duration filter
            if plan_duration and plan_duration != "all" and duration.lower() != plan_duration.lower():
                continue

            # Intelligent query match if query provided
            if query_str:
                is_match, score, tier = evaluate_product_match(query_str, p)
                if not is_match:
                    continue
                matched_with_meta.append((p, score, tier, cat_id, fam, duration, tags))
            else:
                matched_with_meta.append((p, 50.0, 1, cat_id, fam, duration, tags))

        # Enrich each product with historical stats for offer cards
        enriched_results = []
        for item in matched_with_meta:
            p, score, tier, cat_id, fam, duration, tags = item
            
            # Retrieve 7-day price history
            hist = get_product_history(p.store_name, p.name, period_days=7)
            
            change_amount = hist.get("change_amount", 0.0)
            change_pct = hist.get("change_pct", 0.0)
            direction = hist.get("direction", "neutral")
            sparkline = [pt["price"] for pt in hist.get("data_points", [])]
            if not sparkline:
                sparkline = [p.price, p.price]

            bot_handle = STORE_HANDLES.get(p.store_name, f"@{p.store_name.replace(' ', '')}Bot")
            
            p_dict = p.to_dict()
            p_dict.update({
                "category_id": cat_id,
                "product_family": fam,
                "duration_plan": duration,
                "tags": tags,
                "initials": get_store_initials(p.store_name),
                "bot_handle": bot_handle,
                "weekly_change_amount": change_amount,
                "weekly_change_pct": change_pct,
                "direction": direction,
                "sparkline": sparkline,
                "buy_url": p.buy_url or f"https://t.me/{bot_handle.lstrip('@')}",
                "is_cheapest": False
            })
            enriched_results.append(p_dict)

        # Sorting logic
        if sort_by in ["lowest_price", "price_asc"]:
            enriched_results.sort(key=lambda x: (x["price"], -x["in_stock"]))
        elif sort_by in ["highest_price", "price_desc"]:
            enriched_results.sort(key=lambda x: (-x["price"], -x["in_stock"]))
        elif sort_by == "biggest_decrease":
            enriched_results.sort(key=lambda x: (x["weekly_change_pct"], x["price"]))
        elif sort_by == "biggest_increase":
            enriched_results.sort(key=lambda x: (-x["weekly_change_pct"], x["price"]))
        elif sort_by in ["newest", "date_desc"]:
            enriched_results.sort(key=lambda x: (-x["timestamp"], x["price"]))
        elif sort_by in ["stock", "stock_desc"]:
            enriched_results.sort(key=lambda x: (-x["in_stock"], x["price"]))
        else:
            enriched_results.sort(key=lambda x: x["price"])

        # Mark cheapest deal
        if enriched_results:
            enriched_results[0]["is_cheapest"] = True

        stores_with_item = list(dict.fromkeys([p["store_name"] for p in enriched_results]))
        best_deal = enriched_results[0] if enriched_results else None

        # Calculate fair market summary
        stats = {
            "lowest_price": 0.0,
            "highest_price": 0.0,
            "avg_price": 0.0,
            "cheapest_store": "",
            "merchants_count": 0,
            "total_offers": 0,
            "savings": 0.0,
            "savings_percentage": 0.0,
            "currency": "USD"
        }

        if enriched_results:
            prices = [p["price"] for p in enriched_results]
            min_price = min(prices)
            max_price = max(prices)
            avg_price = round(sum(prices) / len(prices), 2)
            savings = round(max_price - min_price, 2)
            savings_pct = round(((max_price - min_price) / max_price * 100), 1) if max_price > 0 else 0
            
            stats = {
                "lowest_price": min_price,
                "highest_price": max_price,
                "avg_price": avg_price,
                "cheapest_store": best_deal["store_name"],
                "merchants_count": len(stores_with_item),
                "total_offers": len(enriched_results),
                "savings": savings,
                "savings_percentage": savings_pct,
                "currency": best_deal.get("currency", "USD")
            }

        # Multi-merchant comparative series for market chart
        comp_query = product_family if (product_family and product_family != "all") else (query_str or "Gemini")
        market_chart_data = get_multi_merchant_comparison(comp_query, period_days=7)

        return {
            "query": query_str,
            "category": category,
            "product_family": product_family,
            "plan_duration": plan_duration,
            "sort_by": sort_by,
            "best_deal": best_deal,
            "stores_with_item": stores_with_item,
            "stats": stats,
            "market_chart": market_chart_data,
            "results": enriched_results
        }
