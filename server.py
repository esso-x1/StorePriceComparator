import os
from typing import List, Optional
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from aggregator import PriceAggregator
from stores.sams_shop import SamsShopAdapter
from stores.digital_asset import DigitalAssetAdapter
from stores.pending_store import PendingStoreAdapter

app = FastAPI(title="Digital Store Price Comparator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("static", exist_ok=True)
os.makedirs("static/icons", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/manifest.json")
def get_manifest():
    return FileResponse("static/manifest.json", media_type="application/manifest+json")

@app.get("/sw.js")
def get_sw():
    return FileResponse("static/sw.js", media_type="application/javascript")

# Initialize Aggregator with ALL stores
aggregator = PriceAggregator()

# 11 Active Connected Stores
aggregator.register_store(SamsShopAdapter())
aggregator.register_store(DigitalAssetAdapter())

from stores.insightx import InsightXAdapter
aggregator.register_store(InsightXAdapter())

from stores.pa_store import PAStoreAdapter
aggregator.register_store(PAStoreAdapter())

from stores.bite_store import BiteStoreAdapter
aggregator.register_store(BiteStoreAdapter())

from stores.acczone import AcczoneAdapter
aggregator.register_store(AcczoneAdapter())

from stores.scraped_store import ScrapedStoreAdapter
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

from stores.digital_socials import DigitalSocialsAdapter
DS_INIT_DATA = "query_id=AAFM8p9WAgAAAEzyn1YdXi53&user=%7B%22id%22%3A5748290124%2C%22first_name%22%3A%22Media%22%2C%22last_name%22%3A%22Tech%22%2C%22username%22%3A%22MediaTech_Building%22%2C%22language_code%22%3A%22ar%22%2C%22allows_write_to_pm%22%3Atrue%2C%22photo_url%22%3A%22https%3A%5C%2F%5C%2Ft.me%5C%2Fi%5C%2Fuserpic%5C%2F320%5C%2F_aeV3vQ_7VvfNJv_Tq8IBywUw1JsyzYwQCHtLILyf-eBoRZmmw5QOb47U3pGaaJH.svg%22%7D&auth_date=1790677164&signature=gLAVh-dtXB5nl_9VEQnvtQLzeQFm_cdjSNkGDD7NRKFE8RnUYKVzgzUhRES2TJAx0JqBeuQ-7JR9M2SpBocuCA&hash=8a81e7acf05fc179357af2d1eb07329b88c5b92c441afc492ffac04293308c6d"
aggregator.register_store(DigitalSocialsAdapter(init_data=DS_INIT_DATA))

# Start background warm up & continuous sync worker (every 60s)
aggregator.start_background_worker(interval=60)

import subprocess
import threading

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

@app.get("/api/stores")
def get_stores():
    return aggregator.get_stores_info()

@app.get("/api/store/{store_name}/feed")
def get_store_feed(store_name: str):
    return aggregator.get_store_feed(store_name)

@app.get("/api/search")
def search(
    q: str = Query("", description="Search term for product"),
    stores: Optional[str] = Query(None, description="Comma-separated store names to include"),
    category: Optional[str] = Query(None, description="Category filter (ai, streaming, design, tools)"),
    sort_by: str = Query("price_asc", description="Sort order (price_asc, date_desc, stock_desc)")
):
    enabled_stores = [s.strip() for s in stores.split(",")] if stores else None
    return aggregator.search_and_compare(
        query=q, 
        enabled_stores=enabled_stores,
        category=category,
        sort_by=sort_by
    )

@app.get("/", response_class=HTMLResponse)
def index():
    return """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover" />
  <title>مقارن أسعار المتاجر الرقمية | Store Price Aggregator</title>
  
  <!-- Apple & PWA Meta Tags -->
  <link rel="manifest" href="/manifest.json" />
  <meta name="theme-color" content="#060911" />
  <meta name="apple-mobile-web-app-capable" content="yes" />
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />
  <meta name="apple-mobile-web-app-title" content="StorePrices" />
  <link rel="apple-touch-icon" href="/static/icons/icon-192.png" />
  
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
  
  <style>
    :root {
      --bg: #060911;
      --glass-surface: rgba(18, 24, 40, 0.72);
      --glass-surface-hover: rgba(26, 35, 58, 0.85);
      --glass-border: rgba(255, 255, 255, 0.08);
      --glass-border-focus: rgba(0, 113, 227, 0.6);
      --glass-blur: blur(28px) saturate(190%);
      --apple-blue: #0071e3;
      --apple-blue-glow: rgba(0, 113, 227, 0.35);
      --green: #10b981;
      --green-glow: rgba(16, 185, 129, 0.3);
      --text: #f8fafc;
      --text-muted: #94a3b8;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; -webkit-tap-highlight-color: transparent; }
    
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Cairo', sans-serif;
      background: radial-gradient(circle at 10% 10%, rgba(0, 113, 227, 0.18) 0%, transparent 45%),
                  radial-gradient(circle at 90% 90%, rgba(139, 92, 246, 0.14) 0%, transparent 45%),
                  var(--bg);
      background-attachment: fixed;
      color: var(--text);
      min-height: 100vh;
      display: flex;
      overflow-x: hidden;
    }
    
    /* Layout */
    .app-layout {
      display: flex;
      width: 100%;
      min-height: 100vh;
      position: relative;
    }

    /* Fixed Stationary Left Sidebar (No visible scrollbar, fixed with site) */
    .sidebar {
      width: 320px;
      min-width: 320px;
      background: rgba(11, 16, 28, 0.94);
      backdrop-filter: var(--glass-blur);
      -webkit-backdrop-filter: var(--glass-blur);
      border-left: 1px solid var(--glass-border);
      padding: 1.6rem 1.2rem;
      display: flex;
      flex-direction: column;
      gap: 1rem;
      box-shadow: -4px 0 30px rgba(0,0,0,0.5);
      z-index: 40;
      position: sticky;
      top: 0;
      height: 100vh;
      overflow: hidden;
      transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .sidebar-header {
      display: flex;
      align-items: center;
      justify-content: flex-start;
      gap: 10px;
      padding-bottom: 0.9rem;
      border-bottom: 1px solid var(--glass-border);
    }
    .sidebar-header h2 {
      font-size: 1.15rem;
      font-weight: 800;
      color: #fff;
    }

    /* Store list without visible scrollbar */
    .store-list {
      display: flex;
      flex-direction: column;
      gap: 0.65rem;
      flex: 1;
      overflow-y: auto;
      scrollbar-width: none;
      -ms-overflow-style: none;
      padding-bottom: 1rem;
    }
    .store-list::-webkit-scrollbar {
      display: none;
    }

    /* Refined Store Item: matches uploaded image styling */
    .store-item {
      background: rgba(18, 24, 40, 0.75);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 16px;
      padding: 0.85rem 1rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
      cursor: pointer;
      user-select: none;
    }
    .store-item:hover {
      background: rgba(0, 113, 227, 0.15);
      border-color: rgba(0, 113, 227, 0.5);
      transform: translateX(-3px);
    }
    .store-item.selected {
      background: rgba(0, 113, 227, 0.25);
      border-color: var(--apple-blue);
      box-shadow: 0 0 16px var(--apple-blue-glow);
    }
    .store-info {
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .status-dot {
      width: 9px;
      height: 9px;
      border-radius: 50%;
      flex-shrink: 0;
    }
    .status-dot.online {
      background: #10b981;
      box-shadow: 0 0 10px #10b981;
    }
    .status-dot.offline {
      background: #ef4444;
      box-shadow: 0 0 8px rgba(239, 68, 68, 0.6);
    }
    .store-name {
      font-size: 0.92rem;
      font-weight: 800;
      color: #fff;
    }
    .store-bot {
      font-size: 0.74rem;
      color: var(--text-muted);
      font-family: 'JetBrains Mono', monospace;
      margin-top: 1px;
    }

    /* Store Price / Offer badge matching image */
    .store-price-badge {
      background: rgba(16, 185, 129, 0.12);
      border: 1px solid rgba(16, 185, 129, 0.35);
      color: #34d399;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.78rem;
      font-weight: 800;
      padding: 3px 8px;
      border-radius: 8px;
      display: inline-block;
    }
    .store-offers-text {
      font-size: 0.72rem;
      color: var(--text-muted);
      margin-top: 2px;
      text-align: left;
    }

    /* Click-outside backdrop overlay */
    .sidebar-backdrop {
      display: none;
      position: fixed;
      inset: 0;
      background: rgba(0, 0, 0, 0.65);
      backdrop-filter: blur(6px);
      -webkit-backdrop-filter: blur(6px);
      z-index: 38;
      opacity: 0;
      transition: opacity 0.25s ease;
    }
    .sidebar-backdrop.active {
      display: block;
      opacity: 1;
    }

    /* Main Content */
    .main-content {
      flex: 1;
      padding: 1.8rem 2.2rem 6.5rem;
      max-width: 1160px;
      margin: 0 auto;
      overflow-y: auto;
    }

    /* Top Sticky App Bar */
    .top-app-bar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 12px;
      margin-bottom: 1.5rem;
      padding-bottom: 1rem;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    }
    .app-brand {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .app-logo-badge {
      width: 42px;
      height: 42px;
      border-radius: 14px;
      background: linear-gradient(135deg, #0071e3 0%, #38bdf8 100%);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1.4rem;
      box-shadow: 0 4px 15px rgba(0, 113, 227, 0.4);
    }
    h1 {
      font-size: 1.55rem;
      font-weight: 900;
      background: linear-gradient(135deg, #ffffff 0%, #93c5fd 60%, #60a5fa 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      letter-spacing: -0.3px;
    }
    .status-counter-tag {
      display: inline-flex;
      align-items: center;
      gap: 5px;
      font-size: 0.75rem;
      color: #a7f3d0;
      background: rgba(16, 185, 129, 0.15);
      border: 1px solid rgba(16, 185, 129, 0.3);
      padding: 2px 8px;
      border-radius: 9999px;
      font-weight: 700;
    }

    /* Top Action Buttons */
    .top-actions {
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .apple-glass-pill {
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid var(--glass-border);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      color: #fff;
      padding: 0.45rem 0.95rem;
      border-radius: 9999px;
      font-size: 0.8rem;
      font-weight: 700;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      cursor: pointer;
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .apple-glass-pill:hover {
      background: rgba(255, 255, 255, 0.12);
      border-color: rgba(255, 255, 255, 0.25);
      transform: translateY(-1px);
    }
    .apple-glass-pill.active {
      background: rgba(16, 185, 129, 0.2);
      color: #34d399;
      border-color: rgba(16, 185, 129, 0.4);
    }

    /* Practical Search & Filters Section */
    .search-filter-section {
      background: rgba(18, 24, 40, 0.65);
      backdrop-filter: var(--glass-blur);
      -webkit-backdrop-filter: var(--glass-blur);
      border: 1px solid var(--glass-border);
      border-radius: 22px;
      padding: 1.15rem;
      margin-bottom: 1.5rem;
      box-shadow: 0 10px 30px rgba(0,0,0,0.35);
    }

    /* Search Input + Direct Product Picker Row */
    .search-top-row {
      display: flex;
      gap: 12px;
      align-items: center;
      margin-bottom: 1rem;
      flex-wrap: wrap;
    }
    .search-input-wrap {
      position: relative;
      flex: 1;
      min-width: 250px;
    }
    .search-input-wrap input {
      width: 100%;
      padding: 0.95rem 1.2rem 0.95rem 3.6rem;
      border-radius: 16px;
      background: rgba(11, 15, 26, 0.85);
      border: 1px solid var(--glass-border);
      color: #fff;
      font-size: 1.05rem;
      font-family: inherit;
      outline: none;
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .search-input-wrap input:focus {
      border-color: var(--apple-blue);
      box-shadow: 0 0 0 3px var(--apple-blue-glow);
    }
    .search-icon {
      position: absolute;
      left: 1.2rem;
      top: 50%;
      transform: translateY(-50%);
      font-size: 1.2rem;
      pointer-events: none;
      opacity: 0.6;
    }
    .search-clear-btn {
      position: absolute;
      right: 1.2rem;
      top: 50%;
      transform: translateY(-50%);
      background: none;
      border: none;
      color: var(--text-muted);
      font-size: 1.1rem;
      cursor: pointer;
      display: none;
    }
    .search-clear-btn.active { display: block; }

    /* Product Filter Picker Dropdown */
    .product-picker-wrap {
      min-width: 240px;
      flex: 0 0 auto;
    }
    .product-select {
      width: 100%;
      padding: 0.95rem 1.1rem;
      border-radius: 16px;
      background: rgba(11, 15, 26, 0.85);
      border: 1px solid var(--glass-border);
      color: #93c5fd;
      font-size: 0.9rem;
      font-weight: 700;
      font-family: inherit;
      outline: none;
      cursor: pointer;
      transition: all 0.2s;
    }
    .product-select:focus {
      border-color: var(--apple-blue);
      box-shadow: 0 0 0 3px var(--apple-blue-glow);
    }
    .product-select option, .product-select optgroup {
      background: #0d121f;
      color: #fff;
    }

    /* Category Filter Chips & Sort Controls */
    .filter-controls-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 10px;
    }
    .category-pills {
      display: flex;
      align-items: center;
      gap: 6px;
      flex-wrap: wrap;
    }
    .cat-pill {
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid var(--glass-border);
      color: var(--text-muted);
      padding: 0.35rem 0.85rem;
      border-radius: 9999px;
      font-size: 0.82rem;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.15s ease;
      display: inline-flex;
      align-items: center;
      gap: 5px;
    }
    .cat-pill:hover {
      background: rgba(255, 255, 255, 0.08);
      color: #fff;
    }
    .cat-pill.active {
      background: var(--apple-blue);
      color: #fff;
      border-color: var(--apple-blue);
      box-shadow: 0 2px 10px var(--apple-blue-glow);
    }

    .sort-control {
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .sort-control span {
      font-size: 0.8rem;
      color: var(--text-muted);
      font-weight: 600;
    }
    .sort-select {
      background: rgba(11, 15, 26, 0.85);
      border: 1px solid var(--glass-border);
      color: #fff;
      padding: 0.35rem 0.85rem;
      border-radius: 10px;
      font-size: 0.82rem;
      font-family: inherit;
      outline: none;
      cursor: pointer;
    }

    /* Store Feed Panel */
    .store-feed-panel {
      display: none;
      background: rgba(22, 28, 48, 0.75);
      backdrop-filter: var(--glass-blur);
      -webkit-backdrop-filter: var(--glass-blur);
      border: 1.5px solid var(--apple-blue);
      border-radius: 22px;
      padding: 1.6rem;
      margin-bottom: 2rem;
      box-shadow: 0 15px 35px rgba(0,0,0,0.5), 0 0 25px var(--apple-blue-glow);
      animation: fadeIn 0.25s ease-out;
    }
    .store-feed-panel.active { display: block; }
    .feed-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 1px solid var(--glass-border);
      padding-bottom: 1rem;
      margin-bottom: 1.4rem;
      flex-wrap: wrap;
      gap: 12px;
    }
    .feed-store-info {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .feed-store-badge {
      background: rgba(0, 113, 227, 0.2);
      border: 1px solid var(--apple-blue);
      color: #93c5fd;
      padding: 3px 10px;
      border-radius: 8px;
      font-size: 0.8rem;
      font-weight: 700;
    }
    .feed-close-btn {
      background: rgba(239, 68, 68, 0.15);
      color: #f87171;
      border: 1px solid rgba(239, 68, 68, 0.35);
      border-radius: 10px;
      padding: 0.45rem 1rem;
      cursor: pointer;
      font-weight: 800;
      font-size: 0.85rem;
      font-family: inherit;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
    }
    .feed-close-btn:hover {
      background: rgba(239, 68, 68, 0.25);
      color: #fff;
    }

    /* Stores Availability Summary */
    .stores-found-banner {
      background: rgba(22, 28, 48, 0.65);
      backdrop-filter: var(--glass-blur);
      -webkit-backdrop-filter: var(--glass-blur);
      border: 1px solid var(--glass-border);
      border-radius: 16px;
      padding: 0.85rem 1.15rem;
      margin-bottom: 1.5rem;
      display: none;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 10px;
    }
    .stores-found-banner.active { display: flex; }
    .stores-found-title {
      font-size: 0.88rem;
      font-weight: 700;
      color: #e2e8f0;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .stores-chips {
      display: flex;
      gap: 0.5rem;
      flex-wrap: wrap;
    }
    .store-chip {
      background: rgba(0, 113, 227, 0.18);
      border: 1px solid rgba(0, 113, 227, 0.4);
      color: #93c5fd;
      padding: 2px 9px;
      border-radius: 8px;
      font-size: 0.8rem;
      font-weight: 600;
    }

    /* Best deal banner: Apple Liquid Glass */
    .best-banner {
      background: linear-gradient(135deg, rgba(16, 185, 129, 0.18) 0%, rgba(0, 113, 227, 0.15) 100%);
      backdrop-filter: var(--glass-blur);
      -webkit-backdrop-filter: var(--glass-blur);
      border: 1.5px solid rgba(16, 185, 129, 0.5);
      border-radius: 20px;
      padding: 1.3rem 1.6rem;
      margin-bottom: 1.6rem;
      display: none;
      align-items: center;
      justify-content: space-between;
      box-shadow: 0 10px 30px rgba(16, 185, 129, 0.15), inset 0 1px 0 rgba(255, 255, 255, 0.15);
      gap: 15px;
      flex-wrap: wrap;
    }
    .best-banner.active { display: flex; }
    .best-badge {
      display: inline-block;
      background: var(--green);
      color: #022c22;
      font-weight: 800;
      font-size: 0.72rem;
      padding: 3px 9px;
      border-radius: 6px;
      margin-bottom: 0.4rem;
    }
    .best-name { font-size: 1.25rem; font-weight: 800; color: #fff; }
    .best-details { font-size: 0.88rem; color: #cbd5e1; margin-top: 4px; display: flex; gap: 15px; flex-wrap: wrap; }
    .best-price {
      font-family: 'JetBrains Mono', monospace;
      font-size: 1.95rem;
      font-weight: 900;
      color: #34d399;
      text-align: left;
    }

    /* Products Grid: 3-column responsive layout */
    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
      gap: 1.2rem;
    }

    /* Practical Apple Liquid Glass Card */
    .product-card {
      background: var(--glass-surface);
      backdrop-filter: var(--glass-blur);
      -webkit-backdrop-filter: var(--glass-blur);
      border: 1px solid var(--glass-border);
      border-radius: 20px;
      padding: 1.3rem;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      position: relative;
      overflow: hidden;
      box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.12);
      transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .product-card:hover {
      transform: translateY(-3px);
      border-color: rgba(255, 255, 255, 0.25);
      box-shadow: 0 15px 35px rgba(0, 113, 227, 0.18), inset 0 1px 0 rgba(255, 255, 255, 0.25);
    }
    .product-card.is-cheapest {
      border: 1.5px solid var(--green);
      background: linear-gradient(180deg, rgba(16, 185, 129, 0.12) 0%, rgba(22, 28, 48, 0.75) 45%);
    }

    .card-top-badge {
      position: absolute;
      top: 0.9rem;
      left: 0.9rem;
      background: var(--green);
      color: #022c22;
      font-size: 0.7rem;
      font-weight: 800;
      padding: 3px 9px;
      border-radius: 9999px;
      box-shadow: 0 2px 8px rgba(16, 185, 129, 0.4);
    }

    /* Card Top Flex */
    .card-header-flex {
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 0.9rem;
    }
    .product-img-box {
      width: 54px;
      height: 54px;
      border-radius: 16px;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.15);
      padding: 7px;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
      box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.15);
    }
    .product-img {
      width: 100%;
      height: 100%;
      object-fit: contain;
      filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));
    }
    .product-main-meta {
      flex: 1;
      min-width: 0;
    }
    .store-label {
      display: inline-block;
      background: rgba(0, 113, 227, 0.18);
      border: 1px solid rgba(0, 113, 227, 0.35);
      color: #93c5fd;
      border-radius: 6px;
      padding: 2px 7px;
      font-size: 0.75rem;
      font-weight: 700;
      margin-bottom: 0.3rem;
    }
    .item-value-name {
      font-size: 1rem;
      font-weight: 800;
      color: #fff;
      line-height: 1.35;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }

    /* Key Value Rows */
    .item-row {
      margin-bottom: 0.45rem;
      display: flex;
      align-items: baseline;
      justify-content: space-between;
      gap: 10px;
    }
    .item-label {
      font-weight: 700;
      color: var(--text-muted);
      font-size: 0.82rem;
    }
    .item-value-price {
      font-family: 'JetBrains Mono', monospace;
      font-size: 1.35rem;
      font-weight: 800;
      color: #38bdf8;
    }
    .item-value-stock {
      font-size: 0.85rem;
      font-weight: 700;
      color: #a7f3d0;
      display: inline-flex;
      align-items: center;
      gap: 5px;
    }
    .stock-indicator-dot {
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: var(--green);
      display: inline-block;
    }
    .item-value-date {
      font-size: 0.75rem;
      color: #94a3b8;
      font-family: 'JetBrains Mono', monospace;
    }

    .card-footer {
      margin-top: 0.9rem;
      padding-top: 0.85rem;
      border-top: 1px solid rgba(255, 255, 255, 0.08);
      display: flex;
      align-items: center;
      justify-content: flex-end;
    }

    /* Apple Pill Button */
    .apple-btn {
      background: linear-gradient(135deg, #0071e3 0%, #38bdf8 100%);
      color: #fff;
      border: none;
      padding: 0.58rem 1.25rem;
      border-radius: 9999px;
      font-weight: 800;
      font-size: 0.88rem;
      font-family: inherit;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      text-decoration: none;
      box-shadow: 0 4px 15px rgba(0, 113, 227, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.3);
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
      cursor: pointer;
    }
    .apple-btn:hover {
      transform: scale(1.02);
      box-shadow: 0 6px 20px rgba(0, 113, 227, 0.6);
    }
    .apple-btn.cheapest-btn {
      background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
      color: #022c22;
      box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.4);
    }

    .initial-prompt {
      text-align: center;
      padding: 4rem 1rem;
      color: var(--text-muted);
    }
    .initial-prompt .icon {
      font-size: 3rem;
      margin-bottom: 0.8rem;
      opacity: 0.8;
    }
    .initial-prompt h3 {
      font-size: 1.25rem;
      color: #fff;
      margin-bottom: 0.4rem;
    }

    .loading, .empty {
      text-align: center;
      color: var(--text-muted);
      padding: 3.5rem 0;
      font-size: 1.15rem;
    }

    /* Skeleton Loading Cards */
    .skeleton-card {
      background: rgba(22, 28, 48, 0.4);
      border: 1px solid var(--glass-border);
      border-radius: 20px;
      padding: 1.3rem;
      animation: shimmer 1.5s infinite;
      height: 220px;
    }
    @keyframes shimmer {
      0% { opacity: 0.4; }
      50% { opacity: 0.8; }
      100% { opacity: 0.4; }
    }

    /* Floating Mobile Glass Dock (Apple Style) */
    .mobile-glass-dock {
      display: none;
      position: fixed;
      bottom: 12px;
      left: 50%;
      transform: translateX(-50%);
      width: calc(100% - 24px);
      max-width: 440px;
      background: rgba(18, 24, 40, 0.85);
      backdrop-filter: blur(30px) saturate(200%);
      -webkit-backdrop-filter: blur(30px) saturate(200%);
      border: 1px solid rgba(255, 255, 255, 0.16);
      border-radius: 26px;
      padding: 0.55rem 0.8rem;
      box-shadow: 0 15px 40px rgba(0, 0, 0, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.2);
      z-index: 99;
      justify-content: space-around;
      align-items: center;
    }
    .dock-item {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 2px;
      color: var(--text-muted);
      font-size: 0.72rem;
      font-weight: 700;
      cursor: pointer;
      padding: 4px 10px;
      border-radius: 12px;
      transition: all 0.2s;
    }
    .dock-item:hover, .dock-item.active {
      color: #fff;
    }
    .dock-item.active {
      color: #38bdf8;
    }
    .dock-item .dock-icon {
      font-size: 1.3rem;
    }

    /* iOS Install Modal */
    .ios-modal {
      display: none;
      position: fixed;
      top: 0; left: 0; right: 0; bottom: 0;
      background: rgba(0, 0, 0, 0.65);
      backdrop-filter: blur(8px);
      z-index: 100;
      align-items: center;
      justify-content: center;
      padding: 1.5rem;
    }
    .ios-modal.active { display: flex; }
    .ios-modal-card {
      background: rgba(22, 28, 48, 0.95);
      border: 1px solid var(--glass-border);
      border-radius: 24px;
      max-width: 380px;
      width: 100%;
      padding: 1.6rem;
      text-align: center;
      box-shadow: 0 20px 50px rgba(0,0,0,0.6);
    }

    /* Responsive */
    @media (max-width: 860px) {
      .sidebar {
        position: fixed;
        right: -320px;
        top: 0;
        bottom: 0;
        height: 100vh;
      }
      .sidebar.open {
        transform: translateX(-320px);
      }
      .main-content {
        padding: 1.2rem 1rem 6.5rem;
      }
      .mobile-glass-dock {
        display: flex;
      }
      h1 {
        font-size: 1.35rem;
      }
      .search-top-row {
        flex-direction: column;
        align-items: stretch;
      }
      .product-picker-wrap {
        width: 100%;
      }
      .filter-controls-row {
        flex-direction: column;
        align-items: stretch;
      }
      .sort-control {
        justify-content: flex-end;
      }
    }
  </style>
</head>
<body>
  <!-- Click-outside backdrop overlay for sidebar -->
  <div id="sidebarBackdrop" class="sidebar-backdrop" onclick="closeSidebar()"></div>

  <div class="app-layout">
    
    <!-- Fixed Stationary Left Sidebar (No visible scrollbar) -->
    <aside id="sidebar" class="sidebar">
      <div class="sidebar-header">
        <span style="font-size:1.35rem;">🏪</span>
        <div>
          <h2>قائمة المتاجر</h2>
          <div id="sidebarSubtitle" style="font-size:0.75rem; color:var(--text-muted);">المتاجر المتصلة</div>
        </div>
      </div>

      <div id="storeList" class="store-list"></div>

      <div style="margin-top: 0.6rem; padding: 0.6rem 0; border-top: 1px solid var(--glass-border); text-align: center;">
        <button id="crawlBtn" onclick="runCrawlerNow()" class="apple-btn" style="width: 100%; border-radius: 12px; font-size: 0.8rem; padding: 0.55rem 0.8rem;">
          <span>🤖</span>
          <span id="crawlBtnText">تحديث عروض البوتات (الزاحف)</span>
        </button>
        <div id="crawlStatus" style="font-size:0.72rem; color:var(--text-muted); margin-top:5px; min-height:16px;"></div>
      </div>
    </aside>

    <!-- Main Content Area -->
    <main class="main-content">
      <!-- Top Sticky App Bar -->
      <header class="top-app-bar">
        <div class="app-brand" onclick="toggleSidebar()" style="cursor:pointer;" title="انقر لفتح قائمة المتاجر">
          <div class="app-logo-badge">🛍️</div>
          <div>
            <h1>مقارن الأسعار الذكي</h1>
            <div style="display:flex; align-items:center; gap:8px; margin-top:2px;">
              <span id="storesCounterBadge" class="status-counter-tag">⚡ 11 متجر نشط</span>
              <span style="font-size:0.75rem; color:var(--text-muted);">تحديث فوري <b style="color:#38bdf8;">0.01s</b></span>
            </div>
          </div>
        </div>
        
        <!-- Action Buttons -->
        <div class="top-actions">
          <button id="refreshDataBtn" onclick="manualRefreshCache()" class="apple-glass-pill" title="تحديث البيانات من السيرفر">
            <span id="refreshIcon">🔄</span>
            <span>تحديث الأسعار</span>
          </button>
          <button id="pushNotifBtn" onclick="togglePushNotifications()" class="apple-glass-pill" title="تفعيل الإشعارات الفورية">
            <span id="pushIcon">🔔</span>
            <span id="pushText">الإشعارات</span>
          </button>
          <button id="installPwaBtn" onclick="handleInstallClick()" class="apple-glass-pill" style="display:none;" title="تثبيت التطبيق">
            <span>📲</span>
            <span>تثبيت</span>
          </button>
        </div>
      </header>

      <!-- Practical Search & Filter Section -->
      <section class="search-filter-section">
        <div class="search-top-row">
          <div class="search-input-wrap">
            <input type="text" id="searchInput" placeholder="ابحث عن اسم السلعة (مثال: Gemini, ChatGPT, Canva...)" autofocus />
            <span class="search-icon">🔍</span>
            <button id="clearSearchBtn" class="search-clear-btn" onclick="clearSearch()" title="مسح البحث">✕</button>
          </div>
          <div class="product-picker-wrap">
            <select id="productSelect" class="product-select" onchange="handleProductSelect()">
              <option value="">🎯 فلتر تحديد المنتج مباشرة...</option>
              <optgroup label="🤖 الذكاء الاصطناعي (AI)">
                <option value="Gemini">Gemini Pro / Google AI</option>
                <option value="ChatGPT">ChatGPT Plus / GPT-4</option>
                <option value="Claude">Claude Pro / Anthropic</option>
                <option value="Midjourney">Midjourney AI</option>
                <option value="DeepSeek">DeepSeek</option>
              </optgroup>
              <optgroup label="🎨 التصميم والمونتاج">
                <option value="Canva">Canva Pro</option>
                <option value="CapCut">CapCut Pro</option>
                <option value="Autodesk">Autodesk Admin / 3D</option>
                <option value="Adobe">Adobe Creative Cloud</option>
              </optgroup>
              <optgroup label="🍿 البث والترفيه">
                <option value="Netflix">Netflix Premium 4K</option>
                <option value="Spotify">Spotify Premium</option>
                <option value="YouTube">YouTube Premium</option>
                <option value="Shahid">Shahid VIP</option>
              </optgroup>
              <optgroup label="⚡ الخدمات والأدوات">
                <option value="Duolingo">Duolingo Super</option>
                <option value="Telegram">Telegram Premium</option>
                <option value="Discord">Discord Nitro</option>
                <option value="TradingView">TradingView Pro</option>
                <option value="Notion">Notion Plus</option>
                <option value="VPN">VPN (NordVPN / Surfshark)</option>
              </optgroup>
            </select>
          </div>
        </div>

        <div class="filter-controls-row">
          <!-- Category Pills -->
          <div class="category-pills">
            <span class="cat-pill active" onclick="setCategory('all')">🌐 الكل</span>
            <span class="cat-pill" onclick="setCategory('ai')">🤖 ذكاء اصطناعي</span>
            <span class="cat-pill" onclick="setCategory('design')">🎨 تصميم ومونتاج</span>
            <span class="cat-pill" onclick="setCategory('streaming')">🍿 بث وترفيه</span>
            <span class="cat-pill" onclick="setCategory('tools')">⚡ أدوات وVPN</span>
          </div>

          <!-- Sort Select -->
          <div class="sort-control">
            <span>ترتيب حسب:</span>
            <select id="sortSelect" class="sort-select" onchange="handleSortChange()">
              <option value="price_asc">الأقل سعراً 🏆</option>
              <option value="date_desc">أحدث تاريخ 🕒</option>
              <option value="stock_desc">الأكثر توفراً 📊</option>
            </select>
          </div>
        </div>
      </section>

      <!-- Store Feed / Latest Notifications Panel -->
      <div id="storeFeedPanel" class="store-feed-panel">
        <div class="feed-header">
          <div class="feed-store-info">
            <span style="font-size: 1.8rem;">📢</span>
            <div>
              <div style="display:flex; align-items:center; gap:8px;">
                <h2 id="feedStoreName" style="font-size:1.25rem; font-weight:800; color:#fff;">-</h2>
                <span id="feedStoreBadge" class="feed-store-badge">أحدث الإشعارات والعروض</span>
              </div>
              <div id="feedStoreBot" style="font-size:0.8rem; color:var(--text-muted); font-family:'JetBrains Mono', monospace; margin-top:2px;">-</div>
            </div>
          </div>
          <button class="feed-close-btn" onclick="closeStoreFeed()">
            <span>✖</span>
            <span>إغلاق وعودة للبحث</span>
          </button>
        </div>
        
        <div id="feedLoading" style="text-align:center; padding:2rem 0; color:var(--text-muted); font-size:0.95rem;">
          جاري جلب أحدث إشعارات وعروض المتجر...
        </div>
        <div id="feedItemsGrid" class="grid"></div>
      </div>

      <!-- Initial Prompt -->
      <div id="initialPrompt" class="initial-prompt">
        <div class="icon">🔎</div>
        <h3>اكتب اسم المنتج أو اختر قسماً للبدء</h3>
        <p>البحث فوري في أجزاء من الثانية من كافة المتاجر الرقمية المتصلة.</p>
      </div>

      <!-- Stores Availability Summary -->
      <div id="storesBanner" class="stores-found-banner">
        <div class="stores-found-title">
          <span>📦 السلعة متوفرة في المتاجر التالية:</span>
          <div id="storesChips" class="stores-chips"></div>
        </div>
        <div id="storesCountBadge" style="font-size:0.8rem; color:var(--text-muted);"></div>
      </div>

      <!-- #1 Best Deal on latest post date -->
      <div id="bestBanner" class="best-banner">
        <div>
          <span class="best-badge">🏆 أقل سعر متوفر بناءً على أحدث تاريخ</span>
          <div id="bestName" class="best-name">-</div>
          <div class="best-details">
            <span id="bestStore" style="color:#93c5fd; font-weight:700;">-</span>
            <span id="bestStock" style="color:#a7f3d0;">-</span>
            <span id="bestDate" style="color:#94a3b8; font-family:'JetBrains Mono', monospace;">-</span>
          </div>
        </div>
        <div>
          <div id="bestPrice" class="best-price">0.00 USDT</div>
          <a id="bestLink" href="#" target="_blank" class="apple-btn cheapest-btn" style="margin-top:8px;">طلب السلعة الآن 👈</a>
        </div>
      </div>

      <!-- Results Grid -->
      <div id="resultsGrid" class="grid"></div>
      <div id="emptyState" class="empty" style="display:none;">لم يتم العثور على نتائج مطابقة لهذا البحث.</div>
      <div id="loadingState" class="grid" style="display:none;">
        <div class="skeleton-card"></div>
        <div class="skeleton-card"></div>
        <div class="skeleton-card"></div>
      </div>
    </main>

    <!-- Floating Mobile Glass Dock (Apple Style) -->
    <div class="mobile-glass-dock">
      <div class="dock-item active" onclick="focusSearch()">
        <span class="dock-icon">🔍</span>
        <span>البحث</span>
      </div>
      <div class="dock-item" onclick="toggleSidebar()">
        <span class="dock-icon">🏪</span>
        <span>المتاجر</span>
      </div>
      <div class="dock-item" onclick="openFirstStoreFeed()">
        <span class="dock-icon">📢</span>
        <span>الإشعارات</span>
      </div>
      <div class="dock-item" onclick="handleInstallClick()">
        <span class="dock-icon">📲</span>
        <span>تثبيت</span>
      </div>
    </div>

    <!-- iOS PWA Install Modal -->
    <div id="iosModal" class="ios-modal" onclick="closeIosModal()">
      <div class="ios-modal-card" onclick="event.stopPropagation()">
        <div style="font-size:2.5rem; margin-bottom:0.5rem;">📲</div>
        <h3 style="font-size:1.2rem; font-weight:800; color:#fff; margin-bottom:0.5rem;">تثبيت التطبيق على iPhone</h3>
        <p style="font-size:0.9rem; color:var(--text-muted); line-height:1.6; margin-bottom:1.2rem;">
          لتثبيت المنصة كتطبيق على شاشتك الرئيسية:<br>
          1. اضغط على زر المشاركة <b style="color:#38bdf8;">(Share ⎋)</b> أسفل متصفح Safari.<br>
          2. مرر للأسفل واختر <b style="color:#34d399;">«إضافة إلى الشاشة الرئيسية» ⊞</b>.
        </p>
        <button class="apple-btn" onclick="closeIosModal()" style="width:100%;">فهمت ذلك 👌</button>
      </div>
    </div>

  </div>

  <script>
    const searchInput = document.getElementById('searchInput');
    const clearSearchBtn = document.getElementById('clearSearchBtn');
    const productSelect = document.getElementById('productSelect');
    const resultsGrid = document.getElementById('resultsGrid');
    const storeList = document.getElementById('storeList');
    const bestBanner = document.getElementById('bestBanner');
    const storesBanner = document.getElementById('storesBanner');
    const storesChips = document.getElementById('storesChips');
    const storesCountBadge = document.getElementById('storesCountBadge');
    const initialPrompt = document.getElementById('initialPrompt');
    const emptyState = document.getElementById('emptyState');
    const loadingState = document.getElementById('loadingState');
    const sidebar = document.getElementById('sidebar');
    const sidebarBackdrop = document.getElementById('sidebarBackdrop');
    const sortSelect = document.getElementById('sortSelect');

    let debounceTimer;
    let currentActiveStore = null;
    let deferredPrompt = null;
    let currentCategory = 'all';
    let currentSortBy = 'price_asc';
    let allActiveStores = [];

    // Register Service Worker for PWA
    if ('serviceWorker' in navigator) {
      window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js').catch(err => {
          console.log('SW registration error:', err);
        });
      });
    }

    // PWA Install Prompt Listeners
    window.addEventListener('beforeinstallprompt', (e) => {
      e.preventDefault();
      deferredPrompt = e;
      const btn = document.getElementById('installPwaBtn');
      if (btn) btn.style.display = 'inline-flex';
    });

    const isIos = () => /iphone|ipad|ipod/.test(window.navigator.userAgent.toLowerCase());
    const isInStandaloneMode = () => ('standalone' in window.navigator) && (window.navigator.standalone);

    if (isIos() && !isInStandaloneMode()) {
      const btn = document.getElementById('installPwaBtn');
      if (btn) btn.style.display = 'inline-flex';
    }

    function handleInstallClick() {
      if (deferredPrompt) {
        deferredPrompt.prompt();
        deferredPrompt.userChoice.then((choiceResult) => {
          if (choiceResult.outcome === 'accepted') {
            document.getElementById('installPwaBtn').style.display = 'none';
          }
          deferredPrompt = null;
        });
      } else if (isIos()) {
        document.getElementById('iosModal').classList.add('active');
      } else {
        alert('يمكنك تثبيت التطبيق من قائمة خيارات المتصفح (Add to Home Screen).');
      }
    }

    function closeIosModal() {
      document.getElementById('iosModal').classList.remove('active');
    }

    // Push Notifications Toggle
    function togglePushNotifications() {
      if (!('Notification' in window)) {
        alert('متصفحك لا يدعم الإشعارات الفورية.');
        return;
      }

      if (Notification.permission === 'granted') {
        new Notification('مقارن الأسعار الذكي ⚡', {
          body: 'الإشعارات مفعلة بالفعل! سنخطرك بأقوى الصفقات فوراً.',
          icon: '/static/icons/icon-192.png'
        });
        updatePushBtnState(true);
      } else {
        Notification.requestPermission().then(permission => {
          if (permission === 'granted') {
            new Notification('تم تفعيل التنبيهات بنجاح! 🔔', {
              body: 'ستصلك الآن كافة التحديثات وأحدث عروض المتاجر أولاً بأول.',
              icon: '/static/icons/icon-192.png'
            });
            updatePushBtnState(true);
          } else {
            alert('تم رفض إذن الإشعارات.');
            updatePushBtnState(false);
          }
        });
      }
    }

    function updatePushBtnState(enabled) {
      const btn = document.getElementById('pushNotifBtn');
      const text = document.getElementById('pushText');
      if (enabled) {
        btn.classList.add('active');
        text.innerText = 'الإشعارات مفعلة';
      } else {
        btn.classList.remove('active');
        text.innerText = 'الإشعارات';
      }
    }

    if ('Notification' in window && Notification.permission === 'granted') {
      updatePushBtnState(true);
    }

    // Sidebar Toggle & Click Outside Behavior
    function toggleSidebar() {
      sidebar.classList.toggle('open');
      if (sidebar.classList.contains('open')) {
        sidebarBackdrop.classList.add('active');
      } else {
        sidebarBackdrop.classList.remove('active');
      }
    }

    function closeSidebar() {
      sidebar.classList.remove('open');
      sidebarBackdrop.classList.remove('active');
    }

    // Dismiss sidebar when clicking outside
    document.addEventListener('click', (e) => {
      if (sidebar && sidebar.classList.contains('open')) {
        if (!sidebar.contains(e.target) && !e.target.closest('.dock-item') && !e.target.closest('.app-brand')) {
          closeSidebar();
        }
      }
    });

    function focusSearch() {
      window.scrollTo({ top: 0, behavior: 'smooth' });
      searchInput.focus();
    }

    function openFirstStoreFeed() {
      if (allActiveStores && allActiveStores.length > 0) {
        openStoreFeed(allActiveStores[0].name);
      }
    }

    function handleProductSelect() {
      const prod = productSelect.value;
      if (prod) {
        searchInput.value = prod;
        clearSearchBtn.classList.add('active');
        doSearch(prod);
      }
    }

    function clearSearch() {
      searchInput.value = '';
      productSelect.value = '';
      clearSearchBtn.classList.remove('active');
      if (currentCategory === 'all') {
        showInitialState();
      } else {
        doSearch('');
      }
      searchInput.focus();
    }

    function setCategory(cat) {
      currentCategory = cat;
      document.querySelectorAll('.cat-pill').forEach(el => {
        if (el.textContent.includes(cat === 'ai' ? 'ذكاء' : cat === 'design' ? 'تصميم' : cat === 'streaming' ? 'بث' : cat === 'tools' ? 'أدوات' : 'الكل')) {
          el.classList.add('active');
        } else {
          el.classList.remove('active');
        }
      });
      doSearch(searchInput.value.trim());
    }

    function handleSortChange() {
      currentSortBy = sortSelect.value;
      doSearch(searchInput.value.trim());
    }

    searchInput.addEventListener('input', () => {
      const val = searchInput.value.trim();
      if (val) {
        clearSearchBtn.classList.add('active');
      } else {
        clearSearchBtn.classList.remove('active');
        productSelect.value = '';
      }

      if (currentActiveStore || document.getElementById('storeFeedPanel').classList.contains('active')) {
        document.getElementById('storeFeedPanel').classList.remove('active');
        currentActiveStore = null;
        document.querySelectorAll('.store-item').forEach(el => el.classList.remove('selected'));
      }

      clearTimeout(debounceTimer);
      if (!val && currentCategory === 'all') {
        showInitialState();
        return;
      }
      debounceTimer = setTimeout(() => doSearch(val), 100);
    });

    function showInitialState() {
      if (document.getElementById('storeFeedPanel')) {
        document.getElementById('storeFeedPanel').classList.remove('active');
      }
      currentActiveStore = null;
      initialPrompt.style.display = 'block';
      resultsGrid.innerHTML = '';
      bestBanner.classList.remove('active');
      storesBanner.classList.remove('active');
      emptyState.style.display = 'none';
      loadingState.style.display = 'none';
      renderSidebar(allActiveStores, false, {});
    }

    async function openStoreFeed(storeName) {
      currentActiveStore = storeName;
      if (window.innerWidth <= 860) closeSidebar();
      
      document.querySelectorAll('.store-item').forEach(el => {
        const nameEl = el.querySelector('.store-name');
        if (nameEl && nameEl.textContent.trim() === storeName) {
          el.classList.add('selected');
        } else {
          el.classList.remove('selected');
        }
      });

      initialPrompt.style.display = 'none';
      bestBanner.classList.remove('active');
      storesBanner.classList.remove('active');
      resultsGrid.innerHTML = '';
      emptyState.style.display = 'none';
      loadingState.style.display = 'none';

      const feedPanel = document.getElementById('storeFeedPanel');
      const feedStoreName = document.getElementById('feedStoreName');
      const feedStoreBot = document.getElementById('feedStoreBot');
      const feedLoading = document.getElementById('feedLoading');
      const feedItemsGrid = document.getElementById('feedItemsGrid');
      
      feedPanel.classList.add('active');
      feedStoreName.textContent = `🏪 متجر: ${storeName}`;
      feedStoreBot.textContent = 'جاري جلب أحدث إشعارات وعروض المتجر...';
      feedLoading.style.display = 'block';
      feedItemsGrid.innerHTML = '';

      window.scrollTo({ top: feedPanel.offsetTop - 30, behavior: 'smooth' });

      try {
        const res = await fetch(`/api/store/${encodeURIComponent(storeName)}/feed`);
        const data = await res.json();
        feedLoading.style.display = 'none';

        if (data.bot_username) {
          feedStoreBot.textContent = `${data.bot_username} • ${data.total_items} عرض وإشعار متاح`;
        } else {
          feedStoreBot.textContent = `${data.total_items} عرض وإشعار متاح`;
        }

        if (!data.items || data.items.length === 0) {
          feedItemsGrid.innerHTML = '<div style="text-align:center; grid-column:1 / -1; padding:3rem 0; color:var(--text-muted);">لا توجد عروض أو إشعارات حالية من هذا المتجر.</div>';
          return;
        }

        data.items.forEach(item => {
          const card = document.createElement('div');
          card.className = 'product-card';
          card.innerHTML = `
            <div>
              <div class="card-header-flex">
                <div class="product-img-box">
                  <img src="${escapeHtml(item.image_url)}" alt="${escapeHtml(item.name)}" class="product-img" onerror="this.src='https://upload.wikimedia.org/wikipedia/commons/8/8a/Google_Gemini_logo.svg'" loading="lazy" />
                </div>
                <div class="product-main-meta">
                  <span class="store-label">📦 ${escapeHtml(item.category || 'عرض رقمي')}</span>
                  <div class="item-value-name">${escapeHtml(item.name)}</div>
                </div>
              </div>

              <div class="item-row">
                <span class="item-label">💵 السعر:</span>
                <span class="item-value-price">${item.price} ${escapeHtml(item.currency)}</span>
              </div>

              <div class="item-row">
                <span class="item-label">📊 المتوفر:</span>
                <span class="item-value-stock">
                  <span class="stock-indicator-dot"></span>
                  ${item.in_stock} قطعة
                </span>
              </div>

              <div class="item-row" style="margin-top:4px;">
                <span class="item-label" style="font-size:0.75rem;">🕒 تاريخ البوست:</span>
                <span class="item-value-date">${escapeHtml(item.updated_at || 'أحدث تاريخ')}</span>
              </div>
            </div>

            <div class="card-footer">
              <a href="${item.buy_url || '#'}" target="_blank" class="apple-btn cheapest-btn" style="width:100%;">
                طلب السلعة الآن 🛒
              </a>
            </div>
          `;
          feedItemsGrid.appendChild(card);
        });

      } catch (err) {
        console.error("Feed error:", err);
        feedLoading.textContent = 'تعذر جلب إشعارات هذا المتجر حالياً.';
      }
    }

    function closeStoreFeed() {
      currentActiveStore = null;
      document.getElementById('storeFeedPanel').classList.remove('active');
      document.querySelectorAll('.store-item').forEach(el => el.classList.remove('selected'));
      
      const query = searchInput.value.trim();
      if (query || currentCategory !== 'all') {
        doSearch(query);
      } else {
        showInitialState();
      }
    }

    function renderSidebar(stores, isSearchResult = false, storeComparison = {}) {
      storeList.innerHTML = '';
      const titleSub = document.getElementById('sidebarSubtitle');
      
      if (isSearchResult) {
        titleSub.innerHTML = `المتاجر المتوفر بها المنتج (<b style="color:#38bdf8;">${stores.length}</b>)`;
      } else {
        titleSub.innerHTML = `المتاجر المتصلة (${stores.length})`;
      }

      if (stores.length === 0) {
        storeList.innerHTML = '<div style="text-align:center; padding:1.5rem 0.5rem; color:var(--text-muted); font-size:0.85rem;">لا يوجد متاجر تملك هذا المنتج</div>';
        return;
      }

      stores.forEach(s => {
        const item = document.createElement('div');
        item.className = 'store-item';
        if (s.name === currentActiveStore) {
          item.classList.add('selected');
        }
        item.title = `انقر لعرض أحدث إشعارات وعروض متجر ${s.name}`;
        item.onclick = () => openStoreFeed(s.name);
        
        let metaHtml = '';
        if (isSearchResult && storeComparison[s.name]) {
          const comp = storeComparison[s.name];
          metaHtml = `
            <div style="text-align: left;">
              <span class="store-price-badge">
                ${comp.lowest_price} ${comp.currency}
              </span>
              <div class="store-offers-text">${comp.total_offers} عروض</div>
            </div>
          `;
        } else {
          metaHtml = `
            <div style="text-align: left;">
              <span class="store-price-badge">نشط</span>
              <div class="store-offers-text">${s.product_count} متوفر</div>
            </div>
          `;
        }

        item.innerHTML = `
          <div class="store-info">
            <span class="status-dot online"></span>
            <div>
              <div class="store-name">${escapeHtml(s.name)}</div>
              <div class="store-bot">${escapeHtml(s.bot_username || '')}</div>
            </div>
          </div>
          ${metaHtml}
        `;
        storeList.appendChild(item);
      });
    }

    async function loadStores() {
      try {
        const res = await fetch('/api/stores');
        const stores = await res.json();
        allActiveStores = stores.filter(s => s.status === 'online' && s.product_count > 0);
        renderSidebar(allActiveStores, false, {});
        const countBadge = document.getElementById('storesCounterBadge');
        if (countBadge) countBadge.innerText = `⚡ ${allActiveStores.length} متجر نشط`;
      } catch (e) {
        console.error("Failed to load stores sidebar:", e);
      }
    }

    async function manualRefreshCache() {
      const icon = document.getElementById('refreshIcon');
      icon.style.display = 'inline-block';
      icon.style.transform = 'rotate(360deg)';
      icon.style.transition = 'transform 0.8s ease';
      await loadStores();
      const val = searchInput.value.trim();
      if (val || currentCategory !== 'all') {
        doSearch(val);
      }
      setTimeout(() => { icon.style.transform = 'rotate(0deg)'; }, 800);
    }

    async function runCrawlerNow() {
      const btn = document.getElementById('crawlBtn');
      const btnText = document.getElementById('crawlBtnText');
      const statusEl = document.getElementById('crawlStatus');
      btn.disabled = true;
      btn.style.opacity = '0.7';
      btnText.innerText = 'جاري سحب العروض...';
      statusEl.innerText = 'يقوم الزاحف بسحب عروض البوتات عبر التليجرام...';

      try {
        const res = await fetch('/api/crawler/run', { method: 'POST' });
        const data = await res.json();
        
        let attempts = 0;
        const interval = setInterval(async () => {
          attempts++;
          const stRes = await fetch('/api/crawler/status');
          const stData = await stRes.json();
          if (!stData.is_crawling || attempts > 30) {
            clearInterval(interval);
            btn.disabled = false;
            btn.style.opacity = '1';
            btnText.innerText = 'تحديث عروض البوتات (الزاحف)';
            statusEl.innerText = '✅ تم تحديث العروض بنجاح!';
            loadStores();
            const val = searchInput.value.trim();
            if (val || currentCategory !== 'all') doSearch(val);
            setTimeout(() => { statusEl.innerText = ''; }, 4000);
          }
        }, 2000);
      } catch (e) {
        btn.disabled = false;
        btn.style.opacity = '1';
        btnText.innerText = 'تحديث عروض البوتات (الزاحف)';
        statusEl.innerText = 'تعذر تشغيل الزاحف';
      }
    }

    async function doSearch(query) {
      if (document.getElementById('storeFeedPanel')) {
        document.getElementById('storeFeedPanel').classList.remove('active');
      }
      currentActiveStore = null;

      if (!query && currentCategory === 'all') {
        showInitialState();
        return;
      }

      initialPrompt.style.display = 'none';
      emptyState.style.display = 'none';

      try {
        const url = `/api/search?q=${encodeURIComponent(query || '')}&category=${encodeURIComponent(currentCategory)}&sort_by=${encodeURIComponent(currentSortBy)}`;
        const res = await fetch(url);
        const data = await res.json();

        resultsGrid.innerHTML = '';
        bestBanner.classList.remove('active');
        storesBanner.classList.remove('active');

        if (!data.results || data.results.length === 0) {
          emptyState.style.display = 'block';
          renderSidebar([], true, {});
          return;
        }

        const storesWithItems = data.stores_with_item || [];
        const matchingStores = allActiveStores.filter(s => storesWithItems.includes(s.name));
        storesWithItems.forEach(stName => {
          if (!matchingStores.some(m => m.name === stName)) {
            matchingStores.push({
              name: stName,
              bot_username: '',
              status: 'online',
              status_text: 'نشط',
              product_count: data.store_comparison[stName]?.total_offers || 1
            });
          }
        });
        renderSidebar(matchingStores, true, data.store_comparison || {});

        if (data.stores_with_item && data.stores_with_item.length > 0) {
          storesBanner.classList.add('active');
          storesChips.innerHTML = '';
          data.stores_with_item.forEach(stName => {
            const chip = document.createElement('span');
            chip.className = 'store-chip';
            chip.textContent = stName;
            storesChips.appendChild(chip);
          });
          storesCountBadge.textContent = `(${data.stores_with_item.length} متاجر توفر نتائج)`;
        }

        if (data.best_deal) {
          bestBanner.classList.add('active');
          document.getElementById('bestName').textContent = data.best_deal.name;
          document.getElementById('bestStore').textContent = `🏪 المتجر: ${data.best_deal.store_name}`;
          document.getElementById('bestStock').textContent = `📊 المتوفر: ${data.best_deal.in_stock} قطعة`;
          document.getElementById('bestDate').textContent = `🕒 تاريخ البوست: ${data.best_deal.updated_at || 'أحدث تاريخ'}`;
          document.getElementById('bestPrice').textContent = `${data.best_deal.price} ${data.best_deal.currency}`;
          document.getElementById('bestLink').href = data.best_deal.buy_url || '#';
        }

        data.results.forEach((item, index) => {
          if (!item.in_stock || item.in_stock <= 0) return;
          const isCheapest = index === 0;
          const card = document.createElement('div');
          card.className = `product-card ${isCheapest ? 'is-cheapest' : ''}`;
          card.innerHTML = `
            ${isCheapest ? '<span class="card-top-badge">🏆 الأقل سعراً</span>' : ''}
            <div>
              <div class="card-header-flex">
                <div class="product-img-box">
                  <img src="${escapeHtml(item.image_url)}" alt="${escapeHtml(item.name)}" class="product-img" onerror="this.src='https://upload.wikimedia.org/wikipedia/commons/8/8a/Google_Gemini_logo.svg'" loading="lazy" />
                </div>
                <div class="product-main-meta">
                  <span class="store-label">🏪 ${escapeHtml(item.store_name)}</span>
                  <div class="item-value-name">${escapeHtml(item.name)}</div>
                </div>
              </div>

              <div class="item-row">
                <span class="item-label">💵 السعر / Price:</span>
                <span class="item-value-price">${item.price} ${escapeHtml(item.currency)}</span>
              </div>

              <div class="item-row">
                <span class="item-label">📊 المتوفر / Stock:</span>
                <span class="item-value-stock">
                  <span class="stock-indicator-dot"></span>
                  ${item.in_stock} قطعة
                </span>
              </div>

              <div class="item-row" style="margin-top:4px;">
                <span class="item-label" style="font-size:0.75rem;">🕒 تاريخ البوست بالمتجر:</span>
                <span class="item-value-date">${escapeHtml(item.updated_at || 'أحدث تاريخ')}</span>
              </div>
            </div>

            <div class="card-footer">
              <a href="${item.buy_url || '#'}" target="_blank" class="apple-btn ${isCheapest ? 'cheapest-btn' : ''}" style="width:100%;">
                طلب المنتج 🛒
              </a>
            </div>
          `;
          resultsGrid.appendChild(card);
        });

      } catch (err) {
        console.error(err);
      }
    }

    function escapeHtml(text) {
      if (!text) return '';
      const div = document.createElement('div');
      div.textContent = text;
      return div.innerHTML;
    }

    loadStores();
    showInitialState();
  </script>
</body>
</html>
"""

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
