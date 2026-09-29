from aggregator import PriceAggregator
from stores.sams_shop import SamsShopAdapter
from stores.digital_asset import DigitalAssetAdapter
from stores.digital_socials import DigitalSocialsAdapter
from stores.pa_store import PAStoreAdapter
from stores.insightx import InsightXAdapter
from stores.scraped_store import ScrapedStoreAdapter

DS_INIT = 'query_id=AAFM8p9WAgAAAEzyn1YdXi53&user=%7B%22id%22%3A5748290124%2C%22first_name%22%3A%22Media%22%2C%22last_name%22%3A%22Tech%22%2C%22username%22%3A%22MediaTech_Building%22%2C%22language_code%22%3A%22ar%22%2C%22allows_write_to_pm%22%3Atrue%2C%22photo_url%22%3A%22https%3A%5C%2F%5C%2Ft.me%5C%2Fi%5C%2Fuserpic%5C%2F320%5C%2F_aeV3vQ_7VvfNJv_Tq8IBywUw1JsyzYwQCHtLILyf-eBoRZmmw5QOb47U3pGaaJH.svg%22%7D&auth_date=1790677164&signature=gLAVh-dtXB5nl_9VEQnvtQLzeQFm_cdjSNkGDD7NRKFE8RnUYKVzgzUhRES2TJAx0JqBeuQ-7JR9M2SpBocuCA&hash=8a81e7acf05fc179357af2d1eb07329b88c5b92c441afc492ffac04293308c6d'

agg = PriceAggregator()
agg.register_store(SamsShopAdapter())
agg.register_store(DigitalAssetAdapter())
agg.register_store(DigitalSocialsAdapter(DS_INIT))
agg.register_store(PAStoreAdapter())
agg.register_store(InsightXAdapter())
agg.register_store(ScrapedStoreAdapter('AI Shop Mops', bot_username='@aishopmopsbot'))
agg.register_store(ScrapedStoreAdapter('QuickDigi Store', bot_username='@QuickDigiBot'))
agg.register_store(ScrapedStoreAdapter('Gemini Pixel Extractor', bot_username='@GeminiPixel1_bot'))

queries = ['chatgpt', 'gemini', 'canva', 'capcut', 'duolingo', 'spotify', 'netflix']
for q in queries:
    res = agg.search_and_compare(q)
    results = res.get('results', [])
    stores = res.get('stores_with_item', [])
    print(f"\n==================================================")
    print(f"QUERY: '{q}' -> {len(results)} items across {len(stores)} stores: {stores}")
    print(f"==================================================")
    for r in results:
        print(f"  [{r['store_name']}] {r['name']} ({r['category']}) -> {r['price']} {r['currency']}")
