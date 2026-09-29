import sys
sys.path.append('J:/101/StorePriceComparator')
from aggregator import PriceAggregator
from stores import SamsShopAdapter, DigitalAssetAdapter

agg = PriceAggregator()
agg.register_store(SamsShopAdapter())
agg.register_store(DigitalAssetAdapter())

print("=== Search: Duolingo ===")
res = agg.search_and_compare("Duolingo")
print("Total matches:", len(res["results"]))
if res["best_deal"]:
    print(f"🏆 Best Deal: [{res['best_deal']['store_name']}] {res['best_deal']['name']} -> {res['best_deal']['price']} {res['best_deal']['currency']}")
print("All offers:")
for r in res["results"]:
    print(f" - [{r['store_name']}] {r['name']}: {r['price']} {r['currency']}")

print("\n=== Search: Gmail ===")
res_gmail = agg.search_and_compare("Gmail")
for r in res_gmail["results"]:
    print(f" - [{r['store_name']}] {r['name']}: {r['price']} {r['currency']}")
