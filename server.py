import os
import io
import csv
import subprocess
import threading
from typing import List, Optional
from fastapi import FastAPI, Query, HTTPException, Response
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from aggregator import PriceAggregator
from stores.sams_shop import SamsShopAdapter
from stores.digital_asset import DigitalAssetAdapter
from stores.insightx import InsightXAdapter
from stores.pa_store import PAStoreAdapter
from stores.bite_store import BiteStoreAdapter
from stores.acczone import AcczoneAdapter
from stores.scraped_store import ScrapedStoreAdapter
from stores.digital_socials import DigitalSocialsAdapter
from stores.verifier_store import VerifierStoreAdapter
import database

app = FastAPI(title="رادار السوق | Market Radar", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
INDEX_FILE = os.path.join(STATIC_DIR, "index.html")

os.makedirs(STATIC_DIR, exist_ok=True)
os.makedirs(os.path.join(STATIC_DIR, "icons"), exist_ok=True)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/manifest.json")
def get_manifest():
    return FileResponse(os.path.join(STATIC_DIR, "manifest.json"), media_type="application/manifest+json")

@app.get("/sw.js")
def get_sw():
    return FileResponse(os.path.join(STATIC_DIR, "sw.js"), media_type="application/javascript")


# Initialize Aggregator with ALL 12 Stores
aggregator = PriceAggregator()
aggregator.register_store(SamsShopAdapter())
aggregator.register_store(DigitalAssetAdapter())
aggregator.register_store(InsightXAdapter())
aggregator.register_store(PAStoreAdapter())
aggregator.register_store(BiteStoreAdapter())
aggregator.register_store(AcczoneAdapter())
aggregator.register_store(ScrapedStoreAdapter(
    name="Gemini Pixel Extractor",
    bot_username="@GeminiPixel1_bot"
))
aggregator.register_store(ScrapedStoreAdapter(
    name="AI Shop Mops",
    bot_username="@aishopmopsbot"
))
aggregator.register_store(ScrapedStoreAdapter(
    name="QuickDigi Store",
    bot_username="@QuickDigiBot"
))
aggregator.register_store(ScrapedStoreAdapter(
    name="DIGINEST Store",
    bot_username="@DIGINEST1BOT"
))
DS_INIT_DATA = "query_id=AAFM8p9WAgAAAEzyn1YdXi53&user=%7B%22id%22%3A5748290124%2C%22first_name%22%3A%22Media%22%2C%22last_name%22%3A%22Tech%22%2C%22username%22%3A%22MediaTech_Building%22%2C%22language_code%22%3A%22ar%22%2C%22allows_write_to_pm%22%3Atrue%2C%22photo_url%22%3A%22https%3A%5C%2F%5C%2Ft.me%5C%2Fi%5C%2Fuserpic%5C%2F320%5C%2F_aeV3vQ_7VvfNJv_Tq8IBywUw1JsyzYwQCHtLILyf-eBoRZmmw5QOb47U3pGaaJH.svg%22%7D&auth_date=1790677164&signature=gLAVh-dtXB5nl_9VEQnvtQLzeQFm_cdjSNkGDD7NRKFE8RnUYKVzgzUhRES2TJAx0JqBeuQ-7JR9M2SpBocuCA&hash=8a81e7acf05fc179357af2d1eb07329b88c5b92c441afc492ffac04293308c6d"
aggregator.register_store(DigitalSocialsAdapter(init_data=DS_INIT_DATA))
aggregator.register_store(VerifierStoreAdapter())

# Start background refresh worker (every 60s)
aggregator.start_background_worker(interval=60)

# Security: Persistent PIN Authentication & User Management
class PinVerifyRequest(BaseModel):
    pin: str

class ChangePinRequest(BaseModel):
    current_pin: str
    new_pin: str

@app.post("/api/auth/verify")
def verify_pin(req: PinVerifyRequest):
    active_pin = database.get_app_pin()
    if req.pin.strip() == active_pin:
        return {
            "success": True, 
            "token": "session_authenticated",
            "user": {
                "name": "المسؤول (Admin)",
                "role": "admin",
                "avatar": "AD"
            }
        }
    return {"success": False, "message": "الرمز السري غير صحيح"}

@app.post("/api/auth/change-pin")
def change_pin(req: ChangePinRequest):
    active_pin = database.get_app_pin()
    if req.current_pin.strip() != active_pin:
        return {"success": False, "message": "الرمز السري الحالي غير صحيح"}
    if len(req.new_pin.strip()) < 4:
        return {"success": False, "message": "يجب أن يتكون الرمز السري من 4 أرقام على الأقل"}
    database.set_app_pin(req.new_pin.strip())
    return {"success": True, "message": "تم تحديث الرمز السري بنجاح"}


# Background Userbot Crawler trigger
is_crawling = False

@app.post("/api/crawler/run")
def trigger_crawler():
    global is_crawling
    if is_crawling:
        return {"status": "already_running", "message": "الزاحف يعمل حالياً في الخلفية"}
    
    def run_crawler_bg():
        global is_crawling
        is_crawling = True
        try:
            cmd = ["python", "userbot_scraper.py"]
            subprocess.run(cmd, cwd=os.path.dirname(os.path.abspath(__file__)), capture_output=True, text=True)
            aggregator.refresh_cache_now(async_mode=False)
        finally:
            is_crawling = False
            
    thread = threading.Thread(target=run_crawler_bg, daemon=True)
    thread.start()
    return {"status": "started", "message": "تم بدء تشغيل الزاحف في الخلفية بنجاح"}

@app.get("/api/crawler/status")
def crawler_status():
    return {"is_crawling": is_crawling}

# Catalog & Dependent Filters Endpoints
@app.get("/api/catalog")
def get_catalog():
    return aggregator.get_catalog_hierarchy()

@app.get("/api/stores")
def get_stores():
    return aggregator.get_stores_info()

@app.get("/api/store/{store_name}/feed")
def get_store_feed(store_name: str):
    return aggregator.get_store_feed(store_name)

@app.get("/api/search")
def search(
    q: str = Query("", description="Search query string"),
    category: Optional[str] = Query(None, description="Category filter"),
    product_family: Optional[str] = Query(None, description="Product family filter"),
    plan_duration: Optional[str] = Query(None, description="Plan / duration filter"),
    stores: Optional[str] = Query(None, description="Comma-separated store names"),
    sort_by: str = Query("lowest_price", description="Sort order")
):
    enabled_stores = [s.strip() for s in stores.split(",")] if stores else None
    return aggregator.search_and_compare(
        query=q,
        enabled_stores=enabled_stores,
        category=category,
        product_family=product_family,
        plan_duration=plan_duration,
        sort_by=sort_by
    )

# Historical Chart Endpoint (Reference Image 2)
@app.get("/api/history")
def get_product_history_endpoint(
    merchant: str = Query(..., description="Store/merchant name"),
    product: str = Query(..., description="Product name"),
    period_days: int = Query(7, description="Period in days (1, 7, 30)")
):
    return database.get_product_history(merchant_name=merchant, product_name=product, period_days=period_days)

# Comparative Multi-Merchant Chart Endpoint (Reference Image 1)
@app.get("/api/market-chart")
def get_market_chart_endpoint(
    product: str = Query(..., description="Product search string or family"),
    period_days: int = Query(7, description="Period in days (7, 30)")
):
    return database.get_multi_merchant_comparison(product_query=product, period_days=period_days)

# Price Alerts Endpoints
class CreateAlertRequest(BaseModel):
    product_name: str
    target_price: float
    merchant_name: Optional[str] = None
    currency: str = "USD"

@app.get("/api/alerts")
def list_alerts():
    return database.get_price_alerts()

@app.post("/api/alerts")
def create_alert(req: CreateAlertRequest):
    return database.create_price_alert(
        product_name=req.product_name,
        target_price=req.target_price,
        merchant_name=req.merchant_name,
        currency=req.currency
    )

@app.post("/api/alerts/{alert_id}/toggle")
def toggle_alert(alert_id: int, is_active: bool = Query(...)):
    success = database.toggle_price_alert(alert_id, is_active)
    return {"success": success}

@app.delete("/api/alerts/{alert_id}")
def delete_alert(alert_id: int):
    success = database.delete_price_alert(alert_id)
    return {"success": success}

# Favorites Endpoints
class ToggleFavoriteRequest(BaseModel):
    item_id: str
    merchant_name: str
    product_name: str
    price: float
    currency: str = "USD"
    buy_url: str = ""
    category: str = ""

@app.get("/api/favorites")
def list_favorites():
    return database.get_favorites()

@app.post("/api/favorites/toggle")
def toggle_fav(req: ToggleFavoriteRequest):
    return database.toggle_favorite(
        item_id=req.item_id,
        merchant_name=req.merchant_name,
        product_name=req.product_name,
        price=req.price,
        currency=req.currency,
        buy_url=req.buy_url,
        category=req.category
    )

# Reports & CSV Export Endpoints
@app.get("/api/reports/summary")
def get_reports_summary():
    all_prods = aggregator.fetch_all()
    valid = [p.to_dict() for p in all_prods if p.price > 0 and p.in_stock > 0]
    valid.sort(key=lambda x: x["price"])
    return {
        "total_tracked": len(valid),
        "top_cheapest": valid[:10],
        "merchants_count": len(aggregator.stores)
    }

@app.get("/api/reports/export.csv")
def export_reports_csv():
    all_prods = aggregator.fetch_all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Store Name", "Product Name", "Price", "Currency", "In Stock", "Category", "Updated At", "Buy URL"])
    
    for p in all_prods:
        if p.price > 0:
            writer.writerow([
                p.store_name,
                p.name,
                p.price,
                p.currency,
                p.in_stock,
                p.category,
                p.updated_at,
                p.buy_url or ""
            ])
            
    csv_bytes = output.getvalue().encode("utf-8-sig")
    return Response(
        content=csv_bytes,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=market_radar_report.csv"}
    )

# Settings Endpoints
@app.get("/api/settings")
def get_settings():
    return database.get_user_settings()

class UpdateSettingRequest(BaseModel):
    key: str
    value: str

@app.post("/api/settings")
def update_setting(req: UpdateSettingRequest):
    database.set_user_setting(req.key, req.value)
    return {"success": True}

# Instant Refresh Endpoint
@app.post("/api/refresh")
def refresh_all():
    aggregator.refresh_cache_now(async_mode=False)
    return {"success": True, "message": "تم تحديث كافة الأسعار بنجاح"}

# Main Application Entry Point
@app.get("/", response_class=FileResponse)
def index():
    return FileResponse(INDEX_FILE)


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=False)

