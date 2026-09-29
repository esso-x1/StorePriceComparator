import asyncio
import re
import json
from datetime import datetime
from telethon import TelegramClient

API_ID = 31746395
API_HASH = "ad1d901ef2d348f3c1a85995ce420183"
SESSION_NAME = "J:/101/StorePriceComparator/userbot"
OUTPUT_FILE = "J:/101/StorePriceComparator/scraped_stores.json"

async def scrape_aishopmops(client):
    print("Scraping @aishopmopsbot...")
    products = []
    try:
        # Start bot
        await client.send_message("@aishopmopsbot", "/start")
        await asyncio.sleep(2)
        
        # Click [Product Catalog]
        msgs = await client.get_messages("@aishopmopsbot", limit=3)
        clicked = False
        for m in msgs:
            if m.buttons:
                for row in m.buttons:
                    for b in row:
                        if "Product Catalog" in b.text:
                            await b.click()
                            clicked = True
                            await asyncio.sleep(2)
                            break
                    if clicked:
                        break
            if clicked:
                break
                
        # Read the buttons containing products and prices
        latest = await client.get_messages("@aishopmopsbot", limit=2)
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        now_ts = datetime.now().timestamp()
        
        for m in latest:
            if m.buttons:
                for row in m.buttons:
                    for b in row:
                        btn_text = b.text.strip()
                        # Matches: "Product Name — 12.0 $" or "Name - 12.0 $"
                        match = re.search(r'^(.*?)\s*[—\-–]\s*([\d\.]+)\s*(\$|USDT)?', btn_text)
                        if match and "Back" not in btn_text and "Menu" not in btn_text:
                            p_name = match.group(1).strip()
                            p_price = float(match.group(2))
                            currency = "USD"
                            products.append({
                                "id": f"mops_{re.sub(r'[^a-zA-Z0-9]', '_', p_name).lower()}",
                                "store_name": "AI Shop Mops",
                                "name": p_name,
                                "price": p_price,
                                "currency": currency,
                                "in_stock": 99,
                                "description": f"Original Telegram Offer from @aishopmopsbot",
                                "updated_at": now_str,
                                "timestamp": now_ts,
                                "category": "AI & Subscriptions",
                                "buy_url": "https://t.me/aishopmopsbot"
                            })
        print(f"Scraped {len(products)} products from @aishopmopsbot!")
    except Exception as e:
        print(f"Error scraping @aishopmopsbot: {e}")
    return products

async def scrape_quickdigi(client):
    print("Scraping @QuickDigiBot...")
    products = []
    try:
        await client.send_message("@QuickDigiBot", "/start")
        await asyncio.sleep(2)
        
        # Click [🛍 Buy Products]
        msgs = await client.get_messages("@QuickDigiBot", limit=3)
        for m in msgs:
            if m.buttons:
                for row in m.buttons:
                    for b in row:
                        if "Buy Products" in b.text:
                            await b.click()
                            await asyncio.sleep(2)
                            break
                            
        # Click [Digital Products]
        msgs2 = await client.get_messages("@QuickDigiBot", limit=3)
        for m in msgs2:
            if m.buttons:
                for row in m.buttons:
                    for b in row:
                        if "Digital Products" in b.text:
                            await b.click()
                            await asyncio.sleep(2)
                            break

        # Read available category buttons and click top ones (e.g. CHTGPT, Gemini, Canva, Capcut, Duolingo)
        cat_msgs = await client.get_messages("@QuickDigiBot", limit=2)
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        now_ts = datetime.now().timestamp()
        
        target_cats = ["CHTGPT", "Gemini", "Canva", "Capcut", "Duolingo", "ElevenLabs", "Netflix", "Adobe"]
        for m in cat_msgs:
            if m.buttons:
                for row in m.buttons:
                    for b in row:
                        for target in target_cats:
                            if target in b.text:
                                try:
                                    print(f"Checking QuickDigi category: {b.text}...")
                                    await b.click()
                                    await asyncio.sleep(2)
                                    # read reply
                                    rep = await client.get_messages("@QuickDigiBot", limit=1)
                                    if rep and rep[0].text:
                                        # Parse prices from text or buttons
                                        lines = rep[0].text.split("\n")
                                        for line in lines:
                                            # e.g. "ChatGPT Plus 1 Month - 9.5 USDT"
                                            p_match = re.search(r'([A-Za-z0-9\s\+\(\)]+)\s*[:\-–—]\s*([\d\.]+)\s*(USDT|\$)?', line)
                                            if p_match:
                                                name_cand = p_match.group(1).strip()
                                                if len(name_cand) > 3 and not any(w in name_cand.lower() for w in ["wallet", "balance", "support", "order"]):
                                                    products.append({
                                                        "id": f"qd_{re.sub(r'[^a-zA-Z0-9]', '_', name_cand).lower()}",
                                                        "store_name": "QuickDigi Store",
                                                        "name": name_cand,
                                                        "price": float(p_match.group(2)),
                                                        "currency": "USDT",
                                                        "in_stock": 10,
                                                        "description": line.strip(),
                                                        "updated_at": now_str,
                                                        "timestamp": now_ts,
                                                        "category": "Digital Products",
                                                        "buy_url": "https://t.me/QuickDigiBot"
                                                    })
                                    # Also check buttons on the category page
                                    if rep and rep[0].buttons:
                                        for b_row in rep[0].buttons:
                                            for item_btn in b_row:
                                                btn_t = item_btn.text.strip()
                                                btn_m = re.search(r'^(.*?)\s*[—\-–]\s*([\d\.]+)\s*(\$|USDT)?', btn_t)
                                                if btn_m and "Back" not in btn_t:
                                                    products.append({
                                                        "id": f"qd_{re.sub(r'[^a-zA-Z0-9]', '_', btn_m.group(1)).lower()}",
                                                        "store_name": "QuickDigi Store",
                                                        "name": btn_m.group(1).strip(),
                                                        "price": float(btn_m.group(2)),
                                                        "currency": "USDT",
                                                        "in_stock": 10,
                                                        "description": btn_t,
                                                        "updated_at": now_str,
                                                        "timestamp": now_ts,
                                                        "category": "Digital Products",
                                                        "buy_url": "https://t.me/QuickDigiBot"
                                                    })
                                except Exception as e_click:
                                    print(f"Error on category {b.text}: {e_click}")
        print(f"Scraped {len(products)} products from @QuickDigiBot!")
    except Exception as e:
        print(f"Error scraping @QuickDigiBot: {e}")
    return products

async def scrape_geminipixel(client):
    print("Scraping @GeminiPixel1_bot...")
    products = []
    try:
        await client.send_message("@GeminiPixel1_bot", "/start")
        await asyncio.sleep(2)
        msgs = await client.get_messages("@GeminiPixel1_bot", limit=2)
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        now_ts = datetime.now().timestamp()
        
        credit_usd = 0.55
        for m in msgs:
            if m.text and "1 Credit" in m.text:
                cr_match = re.search(r'\$([\d\.]+)', m.text)
                if cr_match:
                    try:
                        credit_usd = float(cr_match.group(1))
                    except Exception:
                        pass
                
                # 1. 18M Offer Link
                products.append({
                    "id": "gp_gemini_18m_offer_link",
                    "store_name": "Gemini Pixel Extractor",
                    "name": "Gemini Pro / Google One - Extract Offer Link 18M",
                    "price": round(0.99 * credit_usd, 2),
                    "currency": "USD",
                    "in_stock": 99,
                    "description": "Exclusive 18 Month Offer Link Instantly without sharing account data",
                    "updated_at": now_str,
                    "timestamp": now_ts,
                    "category": "AI & Subscriptions",
                    "buy_url": "https://t.me/GeminiPixel1_bot"
                })
                # 2. 12M Offer Link
                products.append({
                    "id": "gp_gemini_12m_offer_link",
                    "store_name": "Gemini Pixel Extractor",
                    "name": "Gemini Pro / Google One - Extract Offer Link 12M",
                    "price": round(1.0 * credit_usd, 2),
                    "currency": "USD",
                    "in_stock": 99,
                    "description": "Extract secret activation link (12 Month Promo) for Google One",
                    "updated_at": now_str,
                    "timestamp": now_ts,
                    "category": "AI & Subscriptions",
                    "buy_url": "https://t.me/GeminiPixel1_bot"
                })
                # 3. Direct Subscription
                products.append({
                    "id": "gp_gemini_direct_subscription_12m",
                    "store_name": "Gemini Pixel Extractor",
                    "name": "Gemini Pro / Google One - Direct Subscription 12M",
                    "price": round(1.5 * credit_usd, 2),
                    "currency": "USD",
                    "in_stock": 99,
                    "description": "Full automated subscription directly inside Google account",
                    "updated_at": now_str,
                    "timestamp": now_ts,
                    "category": "AI & Subscriptions",
                    "buy_url": "https://t.me/GeminiPixel1_bot"
                })
                break
        print(f"Scraped {len(products)} products from @GeminiPixel1_bot!")
    except Exception as e:
        print(f"Error scraping @GeminiPixel1_bot: {e}")
    return products

async def scrape_diginest(client):
    print("Scraping @DIGINEST1BOT...")
    products = []
    try:
        await client.send_message("@DIGINEST1BOT", "🛍 Products")
        await asyncio.sleep(2)
        msgs = await client.get_messages("@DIGINEST1BOT", limit=10)
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        now_ts = datetime.now().timestamp()

        for m in msgs:
            if not m.out and m.buttons:
                for row in m.buttons:
                    for b in row:
                        btn_t = b.text.strip()
                        if "Back" in btn_t or "Menu" in btn_t:
                            continue
                        
                        stock_m = re.search(r'\[(✅\s*(\d+)|❌\s*Out)\]', btn_t)
                        price_m = re.search(r'\$([\d\.]+)', btn_t)
                        if price_m:
                            is_out = bool(stock_m and "Out" in stock_m.group(1))
                            stock = 0 if is_out else (int(stock_m.group(2)) if stock_m and stock_m.group(2) else 10)
                            price = float(price_m.group(1))

                            # Raw name before the price
                            raw_name = btn_t[:price_m.start()].strip()
                            clean_name = re.sub(r'^[^\w\d\s]+|[—\-–\s]+$', '', raw_name).strip()
                            clean_name = re.sub(r'[—\-–\s]+$', '', clean_name).strip()
                            clean_name = re.sub(r'\s+', ' ', clean_name)

                            if len(clean_name) >= 3:
                                products.append({
                                    "id": f"digi_{re.sub(r'[^a-zA-Z0-9]', '_', clean_name).lower()}",
                                    "store_name": "DIGINEST Store",
                                    "name": clean_name,
                                    "price": price,
                                    "currency": "USD",
                                    "in_stock": stock,
                                    "description": btn_t,
                                    "updated_at": now_str,
                                    "timestamp": now_ts,
                                    "category": "Digital Products",
                                    "buy_url": "https://t.me/DIGINEST1BOT"
                                })
                if products:
                    break
        print(f"Scraped {len(products)} products from @DIGINEST1BOT!")
    except Exception as e:
        print(f"Error scraping @DIGINEST1BOT: {e}")
    return products

async def run_crawler():
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    await client.connect()
    if not await client.is_user_authorized():
        print("User not authorized. Run login.bat first.")
        return

    all_scraped = {}
    
    # 1. AI Shop Mops
    mops_items = await scrape_aishopmops(client)
    all_scraped["AI Shop Mops"] = mops_items
    
    # 2. QuickDigi
    qd_items = await scrape_quickdigi(client)
    all_scraped["QuickDigi Store"] = qd_items

    # 3. Gemini Pixel Extractor
    gp_items = await scrape_geminipixel(client)
    all_scraped["Gemini Pixel Extractor"] = gp_items

    # 4. DIGINEST Store
    digi_items = await scrape_diginest(client)
    all_scraped["DIGINEST Store"] = digi_items

    await client.disconnect()

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_scraped, f, ensure_ascii=False, indent=2)
    print(f"\n✅ All scraped data saved successfully to {OUTPUT_FILE}!")

if __name__ == "__main__":
    asyncio.run(run_crawler())
