import json
from aggregator import PriceAggregator
from stores.sams_shop import SamsShopAdapter
from stores.digital_asset import DigitalAssetAdapter
from stores.digital_socials import DigitalSocialsAdapter
from stores.pa_store import PAStoreAdapter
from stores.insightx import InsightXAdapter
from stores.scraped_store import ScrapedStoreAdapter
from stores.pending_store import PendingStoreAdapter

DS_INIT_DATA = "query_id=AAFM8p9WAgAAAEzyn1YdXi53&user=%7B%22id%22%3A5748290124%2C%22first_name%22%3A%22Media%22%2C%22last_name%22%3A%22Tech%22%2C%22username%22%3A%22MediaTech_Building%22%2C%22language_code%22%3A%22ar%22%2C%22allows_write_to_pm%22%3Atrue%2C%22photo_url%22%3A%22https%3A%5C%2F%5C%2Ft.me%5C%2Fi%5C%2Fuserpic%5C%2F320%5C%2F_aeV3vQ_7VvfNJv_Tq8IBywUw1JsyzYwQCHtLILyf-eBoRZmmw5QOb47U3pGaaJH.svg%22%7D&auth_date=1790677164&signature=gLAVh-dtXB5nl_9VEQnvtQLzeQFm_cdjSNkGDD7NRKFE8RnUYKVzgzUhRES2TJAx0JqBeuQ-7JR9M2SpBocuCA&hash=8a81e7acf05fc179357af2d1eb07329b88c5b92c441afc492ffac04293308c6d"

aggregator = PriceAggregator()

# Register 7 Active Stores
aggregator.register_store(SamsShopAdapter())
aggregator.register_store(DigitalAssetAdapter())
aggregator.register_store(DigitalSocialsAdapter(init_data=DS_INIT_DATA))
aggregator.register_store(PAStoreAdapter())
aggregator.register_store(InsightXAdapter())
aggregator.register_store(ScrapedStoreAdapter("AI Shop Mops", bot_username="@aishopmopsbot"))
aggregator.register_store(ScrapedStoreAdapter("QuickDigi Store", bot_username="@QuickDigiBot"))

# Register Pending Stores
aggregator.register_store(PendingStoreAdapter(
    name="BoomPay Shop",
    bot_username="@boompayshop_bot",
    status_label="غير متصل",
    base_url="https://api.boompay.shop/",
    api_key="bp_UMXpMbigljksmoBt1esML45IW3u16NXZj63ypm-4AKI"
))
aggregator.register_store(PendingStoreAdapter(
    name="Verifier Bot (duskyr)",
    bot_username="@Veriyferbot",
    status_label="غير متصل",
    base_url="https://duskyr.com/api/v1",
    api_key="dsk_live_j5xLScD0vuH53xvIJOGhnqruibi3woYY0Ru-7fsL7nY"
))
aggregator.register_store(PendingStoreAdapter(
    name="Gemini Pixel Extractor",
    bot_username="@GeminiPixel1_bot",
    status_label="بانتظار الرابط",
    api_key="gk_test_96c7cde6_th6vqN8JtoQjFzxTsLkhCDfRbQZukKws"
))

stores_info = aggregator.get_stores_info()
print("=" * 60)
print(f"Total Registered Stores: {len(stores_info)}")
for s in stores_info:
    print(f" - [{s['status'].upper()}] {s['name']} ({s.get('bot_username', '')}): {s.get('stock_count', 0)} products")

print("=" * 60)
for query in ["chatgpt", "canva", "capcut", "perplexity"]:
    res = aggregator.search_and_compare(query)
    results = res.get('results', [])
    best = res.get('best_deal')
    print(f"\n🔍 Search Query: '{query}' -> Found {len(results)} results across {len(res.get('stores_with_item', []))} stores: {', '.join(res.get('stores_with_item', []))}")
    if best:
        print(f"   🏆 CHEAPEST: {best['name']} @ {best['price']} {best['currency']} ({best['store_name']})")
    for s_name, info in res.get('store_comparison', {}).items():
        print(f"      • {s_name}: Lowest {info['lowest_price']} {info['currency']} ({info['item_name']})")
print("=" * 60)
