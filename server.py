import os
from typing import List, Optional
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
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

# Initialize Aggregator with ALL stores (Active + Pending/Offline)
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
            aggregator.clear_cache()
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
    stores: Optional[str] = Query(None, description="Comma-separated store names to include")
):
    enabled_stores = [s.strip() for s in stores.split(",")] if stores else None
    return aggregator.search_and_compare(query=q, enabled_stores=enabled_stores)

@app.get("/", response_class=HTMLResponse)
def index():
    return """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>مقارن أسعار المتاجر الرقمية | Store Price Aggregator</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #090d16;
      --sidebar-bg: #0d1322;
      --card-bg: rgba(20, 29, 48, 0.85);
      --card-border: rgba(45, 65, 100, 0.4);
      --accent: #3b82f6;
      --accent-glow: rgba(59, 130, 246, 0.25);
      --green: #10b981;
      --green-glow: rgba(16, 185, 129, 0.2);
      --gold: #f59e0b;
      --red: #ef4444;
      --text: #f8fafc;
      --text-muted: #94a3b8;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Cairo', sans-serif;
      background: var(--bg);
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
    }

    /* Left Sidebar: Shows ALL Stores */
    .sidebar {
      width: 320px;
      min-width: 320px;
      background: var(--sidebar-bg);
      border-left: 1px solid var(--card-border);
      padding: 1.8rem 1.4rem;
      display: flex;
      flex-direction: column;
      gap: 1.2rem;
      box-shadow: -4px 0 25px rgba(0,0,0,0.4);
      z-index: 20;
    }

    .sidebar-header {
      display: flex;
      align-items: center;
      gap: 10px;
      padding-bottom: 1rem;
      border-bottom: 1px solid var(--card-border);
    }
    .sidebar-header h2 {
      font-size: 1.15rem;
      font-weight: 800;
      color: #fff;
    }

    .store-list {
      display: flex;
      flex-direction: column;
      gap: 0.65rem;
      flex: 1;
      overflow-y: auto;
    }
    .store-item {
      background: rgba(255,255,255,0.03);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 0.75rem 0.9rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
      transition: all 0.2s;
      cursor: pointer;
      user-select: none;
    }
    .store-item:hover {
      background: rgba(59, 130, 246, 0.12);
      border-color: var(--accent);
      transform: translateX(-3px);
    }
    .store-item.selected {
      background: rgba(59, 130, 246, 0.22);
      border-color: var(--accent);
      box-shadow: 0 0 16px var(--accent-glow);
    }
    .store-info {
      display: flex;
      align-items: center;
      gap: 9px;
    }
    .status-dot {
      width: 10px;
      height: 10px;
      border-radius: 50%;
      flex-shrink: 0;
    }
    .status-dot.online {
      background: var(--green);
      box-shadow: 0 0 10px var(--green);
    }
    .status-dot.offline {
      background: var(--red);
      box-shadow: 0 0 8px rgba(239, 68, 68, 0.6);
    }
    .store-name {
      font-size: 0.9rem;
      font-weight: 700;
    }
    .store-bot {
      font-size: 0.72rem;
      color: var(--text-muted);
      font-family: 'JetBrains Mono', monospace;
    }
    .status-badge {
      font-size: 0.72rem;
      font-weight: 700;
      padding: 2px 7px;
      border-radius: 6px;
    }
    .status-badge.online {
      background: rgba(16, 185, 129, 0.15);
      color: var(--green);
    }
    .status-badge.offline {
      background: rgba(239, 68, 68, 0.15);
      color: #f87171;
    }

    /* Main Content */
    .main-content {
      flex: 1;
      padding: 2.2rem 2.5rem;
      max-width: 1100px;
      margin: 0 auto;
      overflow-y: auto;
    }

    header {
      margin-bottom: 2rem;
    }
    h1 {
      font-size: 2.2rem;
      font-weight: 900;
      margin-bottom: 0.4rem;
      background: linear-gradient(135deg, #60a5fa, #38bdf8, #a855f7);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    p.subtitle {
      color: var(--text-muted);
      font-size: 0.98rem;
    }

    /* Search Box */
    .search-box {
      position: relative;
      margin-bottom: 1.5rem;
    }
    .search-box input {
      width: 100%;
      padding: 1.15rem 1.4rem 1.15rem 3.6rem;
      border-radius: 16px;
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      color: #fff;
      font-size: 1.15rem;
      font-family: inherit;
      outline: none;
      transition: all 0.2s ease;
      box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    .search-box input:focus {
      border-color: var(--accent);
      box-shadow: 0 0 0 4px var(--accent-glow);
    }
    .search-icon {
      position: absolute;
      left: 1.4rem;
      top: 50%;
      transform: translateY(-50%);
      font-size: 1.4rem;
      pointer-events: none;
    }

    /* Quick tags */
    .tags {
      display: flex;
      gap: 0.5rem;
      flex-wrap: wrap;
      margin-bottom: 2rem;
    }
    .tag {
      background: rgba(255,255,255,0.05);
      border: 1px solid var(--card-border);
      padding: 0.35rem 0.95rem;
      border-radius: 20px;
      font-size: 0.85rem;
      cursor: pointer;
      color: var(--text-muted);
      transition: all 0.15s ease;
    }
    .tag:hover {
      background: var(--accent-glow);
      color: #fff;
      border-color: var(--accent);
    }

    /* Store Feed / Notifications Panel */
    .store-feed-panel {
      display: none;
      background: linear-gradient(180deg, rgba(20, 29, 48, 0.95) 0%, rgba(13, 19, 34, 0.98) 100%);
      border: 1.5px solid var(--accent);
      border-radius: 20px;
      padding: 1.8rem;
      margin-bottom: 2rem;
      box-shadow: 0 15px 35px rgba(0,0,0,0.4), 0 0 25px rgba(59, 130, 246, 0.15);
      animation: fadeIn 0.25s ease-out;
    }
    .store-feed-panel.active { display: block; }
    .feed-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 1px solid var(--card-border);
      padding-bottom: 1.2rem;
      margin-bottom: 1.5rem;
      flex-wrap: wrap;
      gap: 12px;
    }
    .feed-store-info {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .feed-store-badge {
      background: rgba(59, 130, 246, 0.15);
      border: 1px solid var(--accent);
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
      padding: 0.5rem 1.1rem;
      cursor: pointer;
      font-weight: 800;
      font-size: 0.88rem;
      font-family: inherit;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
    }
    .feed-close-btn:hover {
      background: rgba(239, 68, 68, 0.3);
      color: #fff;
      transform: scale(1.02);
    }

    /* Stores Availability Summary */
    .stores-found-banner {
      background: rgba(30, 41, 59, 0.7);
      border: 1px solid var(--card-border);
      border-radius: 14px;
      padding: 1rem 1.25rem;
      margin-bottom: 1.8rem;
      display: none;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 10px;
    }
    .stores-found-banner.active { display: flex; }
    .stores-found-title {
      font-size: 0.9rem;
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
      background: rgba(59, 130, 246, 0.15);
      border: 1px solid rgba(59, 130, 246, 0.35);
      color: #93c5fd;
      padding: 3px 10px;
      border-radius: 8px;
      font-size: 0.82rem;
      font-weight: 600;
    }

    /* Best deal banner */
    .best-banner {
      background: linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(59, 130, 246, 0.15));
      border: 2px solid rgba(16, 185, 129, 0.6);
      border-radius: 18px;
      padding: 1.5rem 1.8rem;
      margin-bottom: 2rem;
      display: none;
      align-items: center;
      justify-content: space-between;
      box-shadow: 0 10px 30px rgba(16, 185, 129, 0.15);
    }
    .best-banner.active { display: flex; }
    .best-badge {
      display: inline-block;
      background: var(--green);
      color: #000;
      font-weight: 800;
      font-size: 0.75rem;
      padding: 2px 10px;
      border-radius: 6px;
      margin-bottom: 0.5rem;
    }
    .best-name { font-size: 1.35rem; font-weight: 800; color: #fff; }
    .best-details { font-size: 0.9rem; color: #cbd5e1; margin-top: 4px; display: flex; gap: 15px; }
    .best-price {
      font-family: 'JetBrains Mono', monospace;
      font-size: 2.1rem;
      font-weight: 900;
      color: var(--green);
      text-align: left;
    }

    /* Products Grid */
    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
      gap: 1.3rem;
    }

    /* Item Card according to user requirements */
    .product-card {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 16px;
      padding: 1.5rem;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      position: relative;
      transition: transform 0.2s, border-color 0.2s, box-shadow 0.2s;
    }
    .product-card:hover {
      transform: translateY(-4px);
      border-color: rgba(96, 165, 250, 0.6);
      box-shadow: 0 12px 30px rgba(0,0,0,0.4);
    }
    .product-card.is-cheapest {
      border: 2px solid var(--green);
      background: linear-gradient(180deg, rgba(16, 185, 129, 0.08) 0%, var(--card-bg) 40%);
    }

    .card-top-badge {
      position: absolute;
      top: 1rem;
      left: 1rem;
      background: var(--green);
      color: #000;
      font-size: 0.72rem;
      font-weight: 800;
      padding: 3px 10px;
      border-radius: 6px;
    }

    .store-label {
      display: inline-block;
      background: rgba(59, 130, 246, 0.15);
      color: #93c5fd;
      border-radius: 8px;
      padding: 3px 9px;
      font-size: 0.8rem;
      font-weight: 700;
      margin-bottom: 0.9rem;
    }

    /* Specified format by user */
    .item-row {
      margin-bottom: 0.6rem;
      line-height: 1.5;
    }
    .item-label {
      font-weight: 800;
      color: #e2e8f0;
      font-size: 0.95rem;
    }
    .item-value-name {
      font-size: 1.12rem;
      font-weight: 700;
      color: #fff;
    }
    .item-value-price {
      font-family: 'JetBrains Mono', monospace;
      font-size: 1.45rem;
      font-weight: 800;
      color: #38bdf8;
    }
    .item-value-stock {
      font-size: 0.95rem;
      font-weight: 700;
      color: #a7f3d0;
    }
    .item-value-date {
      font-size: 0.82rem;
      color: #94a3b8;
      font-family: 'JetBrains Mono', monospace;
    }

    .card-footer {
      margin-top: 1.2rem;
      padding-top: 1rem;
      border-top: 1px solid rgba(255,255,255,0.06);
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
    .buy-btn {
      background: var(--accent);
      color: #fff;
      text-decoration: none;
      padding: 0.55rem 1.3rem;
      border-radius: 10px;
      font-weight: 800;
      font-size: 0.9rem;
      transition: opacity 0.15s, transform 0.15s;
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }
    .buy-btn:hover {
      opacity: 0.9;
      transform: scale(1.02);
    }
    .buy-btn.cheapest-btn {
      background: var(--green);
      color: #000;
    }

    .initial-prompt {
      text-align: center;
      padding: 4.5rem 1rem;
      color: var(--text-muted);
    }
    .initial-prompt .icon {
      font-size: 3.5rem;
      margin-bottom: 1rem;
      opacity: 0.8;
    }
    .initial-prompt h3 {
      font-size: 1.3rem;
      color: #fff;
      margin-bottom: 0.5rem;
    }

    .loading, .empty {
      text-align: center;
      color: var(--text-muted);
      padding: 4rem 0;
      font-size: 1.2rem;
    }
  </style>
</head>
<body>
  <div class="app-layout">
    
    <!-- Left Sidebar: Shows ALL Stores (Active and Inactive) -->
    <aside class="sidebar">
      <div class="sidebar-header">
        <span style="font-size:1.4rem;">🏪</span>
        <div>
          <h2>قائمة المتاجر</h2>
          <div id="sidebarSubtitle" style="font-size:0.75rem; color:var(--text-muted);">المتاجر المتصلة</div>
        </div>
      </div>

      <div id="storeList" class="store-list">
        <!-- Rendered dynamically -->
      </div>

      <div style="margin-top: 0.8rem; padding: 0.8rem 0; border-top: 1px solid var(--card-border); text-align: center;">
        <button id="crawlBtn" onclick="runCrawlerNow()" style="width: 100%; background: linear-gradient(135deg, #2563eb, #7c3aed); color: #fff; border: 1px solid rgba(255,255,255,0.15); border-radius: 10px; padding: 0.65rem 0.8rem; font-weight: 700; cursor: pointer; font-size: 0.82rem; display: flex; align-items: center; justify-content: center; gap: 6px; box-shadow: 0 4px 14px rgba(37,99,235,0.3); transition: all 0.2s;">
          <span>🤖</span>
          <span id="crawlBtnText">تحديث عروض البوتات (الزاحف)</span>
        </button>
        <div id="crawlStatus" style="font-size:0.75rem; color:var(--text-muted); margin-top:6px; min-height:16px;"></div>
      </div>

      <div style="padding-top: 0.6rem; border-top: 1px solid var(--card-border); font-size: 0.75rem; color: var(--text-muted); text-align: center;">
        يتم الفرز وفق أحدث تاريخ بوست وأقل سعر
      </div>
    </aside>

    <!-- Main Search Area -->
    <main class="main-content">
      <header>
        <h1>🛍️ مقارن الأسعار الذكي للمتاجر الرقمية</h1>
        <p class="subtitle">ابحث عن أي سلعة أو اشتراك، ويعرض المحرك كافة المتاجر المتوفرة بها مع ترشيح أقل سعر بناءً على أحدث تاريخ بوست</p>
      </header>

      <div class="search-box">
        <input type="text" id="searchInput" placeholder="ابحث عن اسم السلعة (مثال: Gemini, ChatGPT, Canva, Capcut, Duolingo...)" autofocus />
        <span class="search-icon">🔍</span>
      </div>

      <div class="tags">
        <span class="tag" onclick="quickSearch('Gemini')">✨ Gemini</span>
        <span class="tag" onclick="quickSearch('ChatGPT')">🔥 ChatGPT</span>
        <span class="tag" onclick="quickSearch('Canva')">🎨 Canva</span>
        <span class="tag" onclick="quickSearch('CapCut')">🎬 CapCut</span>
        <span class="tag" onclick="quickSearch('Duolingo')">🦉 Duolingo</span>
        <span class="tag" onclick="quickSearch('Spotify')">🎵 Spotify</span>
        <span class="tag" onclick="quickSearch('Netflix')">🍿 Netflix</span>
      </div>

      <!-- Store Feed / Latest Notifications Panel -->
      <div id="storeFeedPanel" class="store-feed-panel">
        <div class="feed-header">
          <div class="feed-store-info">
            <span style="font-size: 2rem;">📢</span>
            <div>
              <div style="display:flex; align-items:center; gap:10px;">
                <h2 id="feedStoreName" style="font-size:1.35rem; font-weight:800; color:#fff;">-</h2>
                <span id="feedStoreBadge" class="feed-store-badge">أحدث الإشعارات والعروض</span>
              </div>
              <div id="feedStoreBot" style="font-size:0.85rem; color:var(--text-muted); font-family:'JetBrains Mono', monospace; margin-top:3px;">-</div>
            </div>
          </div>
          <button class="feed-close-btn" onclick="closeStoreFeed()">
            <span>✖</span>
            <span>إغلاق وعودة للبحث</span>
          </button>
        </div>
        
        <div id="feedLoading" style="text-align:center; padding:2.5rem 0; color:var(--text-muted); font-size:1rem;">
          جاري جلب أحدث إشعارات وعروض المتجر...
        </div>
        <div id="feedItemsGrid" class="grid"></div>
      </div>

      <!-- Initial Prompt (When nothing is searched yet) -->
      <div id="initialPrompt" class="initial-prompt">
        <div class="icon">🔎</div>
        <h3>اكتب اسم المنتج للبدء بالبحث</h3>
        <p>اكتب اسم السلعة في شريط البحث أعلاه لجلب نتائج المقارنة من كافة المتاجر فورياً.</p>
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
          <a id="bestLink" href="#" target="_blank" class="buy-btn cheapest-btn" style="margin-top:8px;">طلب السلعة الآن 👈</a>
        </div>
      </div>

      <!-- Results Grid -->
      <div id="resultsGrid" class="grid"></div>
      <div id="emptyState" class="empty" style="display:none;">لم يتم العثور على نتائج مطابقة لهذا البحث.</div>
      <div id="loadingState" class="loading" style="display:none;">جاري البحث ومقارنة الأسعار من المتاجر...</div>
    </main>
  </div>

  <script>
    const searchInput = document.getElementById('searchInput');
    const resultsGrid = document.getElementById('resultsGrid');
    const storeList = document.getElementById('storeList');
    const bestBanner = document.getElementById('bestBanner');
    const storesBanner = document.getElementById('storesBanner');
    const storesChips = document.getElementById('storesChips');
    const storesCountBadge = document.getElementById('storesCountBadge');
    const initialPrompt = document.getElementById('initialPrompt');
    const emptyState = document.getElementById('emptyState');
    const loadingState = document.getElementById('loadingState');

    let debounceTimer;
    let currentActiveStore = null;

    searchInput.addEventListener('input', () => {
      // If store feed is open, close it immediately and return page to search mode!
      if (currentActiveStore || document.getElementById('storeFeedPanel').classList.contains('active')) {
        document.getElementById('storeFeedPanel').classList.remove('active');
        currentActiveStore = null;
        document.querySelectorAll('.store-item').forEach(el => el.classList.remove('selected'));
      }

      clearTimeout(debounceTimer);
      const val = searchInput.value.trim();
      if (!val) {
        showInitialState();
        return;
      }
      debounceTimer = setTimeout(() => doSearch(val), 250);
    });

    function quickSearch(q) {
      if (currentActiveStore || document.getElementById('storeFeedPanel').classList.contains('active')) {
        document.getElementById('storeFeedPanel').classList.remove('active');
        currentActiveStore = null;
        document.querySelectorAll('.store-item').forEach(el => el.classList.remove('selected'));
      }
      searchInput.value = q;
      doSearch(q);
    }

    let allActiveStores = [];

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

    // Open Feed / Latest Notifications of a clicked store
    async function openStoreFeed(storeName) {
      currentActiveStore = storeName;
      
      // Update selected store in sidebar
      document.querySelectorAll('.store-item').forEach(el => {
        const nameEl = el.querySelector('.store-name');
        if (nameEl && nameEl.textContent.trim() === storeName) {
          el.classList.add('selected');
        } else {
          el.classList.remove('selected');
        }
      });

      // Hide comparison and prompt elements
      initialPrompt.style.display = 'none';
      bestBanner.classList.remove('active');
      storesBanner.classList.remove('active');
      resultsGrid.innerHTML = '';
      emptyState.style.display = 'none';
      loadingState.style.display = 'none';

      // Open store feed panel
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
              <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.8rem;">
                <span class="store-label" style="margin-bottom:0;">📦 ${escapeHtml(item.category || 'عرض رقمي')}</span>
                <span style="font-size:0.75rem; color:var(--text-muted); font-family:'JetBrains Mono', monospace;">🕒 ${escapeHtml(item.updated_at || 'أحدث تاريخ')}</span>
              </div>

              <div class="item-row">
                <span class="item-label">🛍️ المنتج:</span>
                <span class="item-value-name">${escapeHtml(item.name)}</span>
              </div>

              <div class="item-row">
                <span class="item-label">💵 السعر:</span>
                <span class="item-value-price">${item.price} ${escapeHtml(item.currency)}</span>
              </div>

              <div class="item-row">
                <span class="item-label">📊 المتوفر:</span>
                <span class="item-value-stock">${item.in_stock} قطعة</span>
              </div>
            </div>

            <div class="card-footer">
              <a href="${item.buy_url || '#'}" target="_blank" class="buy-btn cheapest-btn" style="width:100%; justify-content:center;">
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
      if (query) {
        doSearch(query);
      } else {
        showInitialState();
      }
    }

    // Render Sidebar: shows only matching stores during search, or all active stores otherwise
    function renderSidebar(stores, isSearchResult = false, storeComparison = {}) {
      storeList.innerHTML = '';
      const titleSub = document.getElementById('sidebarSubtitle');
      
      if (isSearchResult) {
        titleSub.innerHTML = `المتاجر المتوفر بها المنتج (<b style="color:var(--accent);">${stores.length}</b>)`;
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
              <span class="status-badge online" style="background:rgba(16,185,129,0.18); color:#34d399; font-weight:700; border:1px solid rgba(16,185,129,0.3);">
                ${comp.lowest_price} ${comp.currency}
              </span>
              <div style="font-size:0.7rem; color:var(--text-muted); margin-top:2px;">${comp.total_offers} عروض</div>
            </div>
          `;
        } else {
          metaHtml = `
            <div style="text-align: left;">
              <span class="status-badge online">نشط</span>
              <div style="font-size:0.7rem; color:var(--text-muted); margin-top:2px;">${s.product_count} متوفر</div>
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

    // Load active stores into sidebar
    async function loadStores() {
      try {
        const res = await fetch('/api/stores');
        const stores = await res.json();
        // Keep strictly stores with available stock
        allActiveStores = stores.filter(s => s.status === 'online' && s.product_count > 0);
        renderSidebar(allActiveStores, false, {});
      } catch (e) {
        console.error("Failed to load stores sidebar:", e);
      }
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
            if (val) doSearch(val);
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

    // Search and display items matching requested format
    async function doSearch(query) {
      if (document.getElementById('storeFeedPanel')) {
        document.getElementById('storeFeedPanel').classList.remove('active');
      }
      currentActiveStore = null;

      if (!query || !query.trim()) {
        showInitialState();
        return;
      }

      initialPrompt.style.display = 'none';
      loadingState.style.display = 'block';
      emptyState.style.display = 'none';
      resultsGrid.innerHTML = '';
      bestBanner.classList.remove('active');
      storesBanner.classList.remove('active');

      try {
        const res = await fetch(`/api/search?q=${encodeURIComponent(query.trim())}`);
        const data = await res.json();
        loadingState.style.display = 'none';

        if (!data.results || data.results.length === 0) {
          emptyState.style.display = 'block';
          renderSidebar([], true, {});
          return;
        }

        // DECISIVE FILTERING: Show ONLY stores with search results in the sidebar!
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

        // Show stores availability summary banner
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

        // Show best deal on latest date
        if (data.best_deal) {
          bestBanner.classList.add('active');
          document.getElementById('bestName').textContent = data.best_deal.name;
          document.getElementById('bestStore').textContent = `🏪 المتجر: ${data.best_deal.store_name}`;
          document.getElementById('bestStock').textContent = `📊 المتوفر: ${data.best_deal.in_stock} قطعة`;
          document.getElementById('bestDate').textContent = `🕒 تاريخ البوست: ${data.best_deal.updated_at || 'أحدث تاريخ'}`;
          document.getElementById('bestPrice').textContent = `${data.best_deal.price} ${data.best_deal.currency}`;
          document.getElementById('bestLink').href = data.best_deal.buy_url || '#';
        }

        // Render Cards in exact specified format
        data.results.forEach((item, index) => {
          if (!item.in_stock || item.in_stock <= 0) return;
          const isCheapest = index === 0;
          const card = document.createElement('div');
          card.className = `product-card ${isCheapest ? 'is-cheapest' : ''}`;
          card.innerHTML = `
            ${isCheapest ? '<span class="card-top-badge">🏆 الأقل سعراً</span>' : ''}
            <div>
              <span class="store-label">🏪 المتجر: ${escapeHtml(item.store_name)}</span>
              
              <!-- Requested format -->
              <div class="item-row">
                <span class="item-label">🛍️ المنتج / Product:</span>
                <span class="item-value-name">${escapeHtml(item.name)}</span>
              </div>

              <div class="item-row">
                <span class="item-label">💵 السعر / Price:</span>
                <span class="item-value-price">${item.price} ${escapeHtml(item.currency)}</span>
              </div>

              <div class="item-row">
                <span class="item-label">📊 الكمية المتوفرة / Stock:</span>
                <span class="item-value-stock">${item.in_stock} قطعة</span>
              </div>

              <div class="item-row" style="margin-top:6px;">
                <span class="item-label" style="font-size:0.8rem; color:var(--text-muted);">🕒 تاريخ البوست بالمتجر / Post Date:</span>
                <span class="item-value-date">${escapeHtml(item.updated_at || 'أحدث تاريخ')}</span>
              </div>
            </div>

            <div class="card-footer">
              <a href="${item.buy_url || '#'}" target="_blank" class="buy-btn ${isCheapest ? 'cheapest-btn' : ''}">
                طلب المنتج 🛒
              </a>
            </div>
          `;
          resultsGrid.appendChild(card);
        });

      } catch (err) {
        console.error(err);
        loadingState.textContent = 'حدث خطأ أثناء تحميل الأسعار.';
      }
    }

    function escapeHtml(text) {
      if (!text) return '';
      const div = document.createElement('div');
      div.textContent = text;
      return div.innerHTML;
    }

    // Initial load: load stores and wait for search
    loadStores();
    showInitialState();
  </script>
</body>
</html>
"""

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
