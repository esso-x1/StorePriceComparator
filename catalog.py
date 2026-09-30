import re
from typing import List, Dict, Any, Tuple, Optional

# Structured Categories with Arabic & English labels
CATEGORIES = [
    {"id": "all", "name_ar": "الكل", "icon": "🌐"},
    {"id": "ai", "name_ar": "ذكاء اصطناعي", "icon": "⚡"},
    {"id": "productivity", "name_ar": "الإنتاجية والأدوات", "icon": "💼"},
    {"id": "design", "name_ar": "التصميم والمونتاج", "icon": "🎨"},
    {"id": "streaming", "name_ar": "خدمات البث والترفيه", "icon": "🎬"}
]

def classify_product(name: str, raw_cat: str = "") -> Tuple[str, str, str, List[str]]:
    """
    Classifies a product into:
    (category_id, product_family, duration_plan, tags)
    """
    n = name.lower()
    cat_id = "productivity"
    family = "أخرى"
    tags = []

    # AI Group
    if any(k in n for k in ['gemini', 'google one', 'google ai']):
        cat_id = "ai"
        family = "Google Gemini"
        tags = ["Google", "AI"]
    elif any(k in n for k in ['chatgpt', 'chat gpt', 'gpt', 'openai']):
        cat_id = "ai"
        family = "ChatGPT / OpenAI"
        tags = ["OpenAI", "AI"]
    elif 'claude' in n:
        cat_id = "ai"
        family = "Claude AI"
        tags = ["Anthropic", "AI"]
    elif 'perplexity' in n:
        cat_id = "ai"
        family = "Perplexity AI"
        tags = ["Search", "AI"]
    elif 'cursor' in n:
        cat_id = "ai"
        family = "Cursor Pro"
        tags = ["IDE", "AI"]
    elif 'grok' in n:
        cat_id = "ai"
        family = "SuperGrok"
        tags = ["xAI", "AI"]
    elif 'elevenlabs' in n:
        cat_id = "ai"
        family = "ElevenLabs"
        tags = ["Voice", "AI"]
    elif 'lovable' in n:
        cat_id = "ai"
        family = "Lovable Pro"
        tags = ["Builder", "AI"]
    elif 'replit' in n:
        cat_id = "ai"
        family = "Replit Core"
        tags = ["Dev", "AI"]
    elif 'midjourney' in n:
        cat_id = "ai"
        family = "Midjourney"
        tags = ["Image", "AI"]

    # Design & Video
    elif 'canva' in n:
        cat_id = "design"
        family = "Canva Pro"
        tags = ["Design", "Pro"]
    elif 'capcut' in n:
        cat_id = "design"
        family = "CapCut Pro"
        tags = ["Video", "Editing"]
    elif any(k in n for k in ['adobe', 'photoshop', 'illustrator', 'creative cloud']):
        cat_id = "design"
        family = "Adobe CC / Express"
        tags = ["Adobe", "Design"]
    elif 'figma' in n:
        cat_id = "design"
        family = "Figma"
        tags = ["UI/UX", "Edu"]
    elif 'autodesk' in n:
        cat_id = "design"
        family = "Autodesk"
        tags = ["3D", "CAD"]

    # Streaming & Media
    elif 'netflix' in n:
        cat_id = "streaming"
        family = "Netflix"
        tags = ["Movies", "4K"]
    elif any(k in n for k in ['youtube', 'yt']):
        cat_id = "streaming"
        family = "YouTube Premium"
        tags = ["Music", "NoAds"]
    elif 'apple music' in n:
        cat_id = "streaming"
        family = "Apple Music"
        tags = ["Audio", "Lossless"]
    elif any(k in n for k in ['spotify', 'shahid', 'osn', 'prime']):
        cat_id = "streaming"
        family = "Streaming Hub"
        tags = ["Media", "Sub"]

    # Productivity & Tools
    elif 'notion' in n:
        cat_id = "productivity"
        family = "Notion"
        tags = ["Notes", "AI"]
    elif 'duolingo' in n:
        cat_id = "productivity"
        family = "Super Duolingo"
        tags = ["Learning", "Edu"]
    elif any(k in n for k in ['vpn', 'surfshark', 'nordvpn', 'expressvpn']):
        cat_id = "productivity"
        family = "VPN Services"
        tags = ["Security", "Privacy"]
    elif any(k in n for k in ['outlook', 'hotmail', 'mail']):
        cat_id = "productivity"
        family = "Accounts & Mail"
        tags = ["Email", "Verified"]
    elif 'telegram' in n or 'tg' in n:
        cat_id = "productivity"
        family = "Telegram Premium"
        tags = ["Social", "Premium"]
    else:
        # Fallback to cleaned title
        cat_id = "productivity"
        family = name.split('-')[0].split('|')[0].strip()[:24]
        tags = ["Digital", "Offer"]

    # Duration extraction
    duration = "خطة افتراضية"
    if '18m' in n or '18 m' in n or '18 شهر' in n or '18 months' in n:
        duration = "18 شهر"
    elif '2y' in n or '2 y' in n or '2 years' in n or 'سنتين' in n or '2 year' in n:
        duration = "2 سنة"
    elif '12m' in n or '12 m' in n or '1y' in n or '1 y' in n or '1 year' in n or 'سنة' in n or '12 months' in n or '12 month' in n or 'annual' in n:
        duration = "12 شهر (سنة)"
    elif '6m' in n or '6 m' in n or '6 month' in n or '6 months' in n or '6 أشهر' in n:
        duration = "6 أشهر"
    elif '4m' in n or '4 month' in n or '4 months' in n:
        duration = "4 أشهر"
    elif '3m' in n or '3 m' in n or '3 month' in n or '3 months' in n or '3 أشهر' in n:
        duration = "3 أشهر"
    elif '2m' in n or '2 month' in n:
        duration = "2 شهر"
    elif '1m' in n or '1 m' in n or '1 month' in n or '30d' in n or '30 d' in n or '30 يوم' in n or 'شهر' in n:
        duration = "1 شهر"
    elif '7d' in n or '7 days' in n or '7 day' in n or '7 أيام' in n:
        duration = "7 أيام"

    return cat_id, family, duration, tags

def build_catalog_hierarchy(all_products: List[Any]) -> Dict[str, Any]:
    """
    Builds the dependent navigation hierarchy:
    Categories -> Products -> Durations
    """
    catalog = {
        "categories": CATEGORIES,
        "products_by_category": {},
        "durations_by_product": {},
        "total_products_count": 0,
        "total_merchants_count": 0
    }

    merchants_set = set()
    category_products_map = {c["id"]: {} for c in CATEGORIES}

    for p in all_products:
        prod = p if isinstance(p, dict) else p.to_dict()
        if prod.get("price", 0) <= 0 or prod.get("in_stock", 0) <= 0:
            continue

        merchants_set.add(prod.get("store_name"))
        cat_id, family, duration, tags = classify_product(prod.get("name", ""), prod.get("category", ""))

        # Add to specific category
        if cat_id in category_products_map:
            if family not in category_products_map[cat_id]:
                category_products_map[cat_id][family] = {"count": 0, "durations": set(), "min_price": 999999, "currency": prod.get("currency", "USD")}
            category_products_map[cat_id][family]["count"] += 1
            category_products_map[cat_id][family]["durations"].add(duration)
            category_products_map[cat_id][family]["min_price"] = min(category_products_map[cat_id][family]["min_price"], prod.get("price", 999999))

        # Add to 'all' category
        if family not in category_products_map["all"]:
            category_products_map["all"][family] = {"count": 0, "durations": set(), "min_price": 999999, "currency": prod.get("currency", "USD")}
        category_products_map["all"][family]["count"] += 1
        category_products_map["all"][family]["durations"].add(duration)
        category_products_map["all"][family]["min_price"] = min(category_products_map["all"][family]["min_price"], prod.get("price", 999999))

        # Track durations for family
        if family not in catalog["durations_by_product"]:
            catalog["durations_by_product"][family] = set()
        catalog["durations_by_product"][family].add(duration)

    # Format into serializable lists
    for cat_id, families in category_products_map.items():
        formatted_list = []
        for fam_name, info in sorted(families.items(), key=lambda x: -x[1]["count"]):
            formatted_list.append({
                "name": fam_name,
                "count": info["count"],
                "min_price": round(info["min_price"], 2) if info["min_price"] < 999990 else 0.0,
                "currency": info["currency"],
                "durations": sorted(list(info["durations"]))
            })
        catalog["products_by_category"][cat_id] = formatted_list

    for fam_name, dur_set in catalog["durations_by_product"].items():
        catalog["durations_by_product"][fam_name] = sorted(list(dur_set))

    catalog["total_products_count"] = len(all_products)
    catalog["total_merchants_count"] = len(merchants_set)

    return catalog
