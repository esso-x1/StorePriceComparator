import asyncio
from telethon import TelegramClient

API_ID = 31746395
API_HASH = "ad1d901ef2d348f3c1a85995ce420183"
SESSION_NAME = "J:/101/StorePriceComparator/userbot"

async def test_navigation():
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    await client.connect()

    # 1. QuickDigiBot: click [🛍 Buy Products]
    print("=== Clicking [🛍 Buy Products] on QuickDigiBot ===")
    msgs = await client.get_messages("@QuickDigiBot", limit=3)
    for m in msgs:
        if m.buttons:
            for row in m.buttons:
                for b in row:
                    if "Buy Products" in b.text:
                        print("Clicking button:", b.text)
                        await b.click()
                        await asyncio.sleep(3)
                        break

    latest = await client.get_messages("@QuickDigiBot", limit=2)
    for m in latest:
        print(f"Reply text:\n{m.text}")
        if m.buttons:
            print("Buttons:")
            for row in m.buttons:
                print(" ", " | ".join([b.text for b in row]))

    # 2. aishopmopsbot: click [Product Catalog]
    print("\n=== Clicking [Product Catalog] on aishopmopsbot ===")
    msgs2 = await client.get_messages("@aishopmopsbot", limit=3)
    for m in msgs2:
        if m.buttons:
            for row in m.buttons:
                for b in row:
                    if "Product Catalog" in b.text:
                        print("Clicking button:", b.text)
                        await b.click()
                        await asyncio.sleep(3)
                        break

    latest2 = await client.get_messages("@aishopmopsbot", limit=2)
    for m in latest2:
        print(f"Reply text:\n{m.text}")
        if m.buttons:
            print("Buttons:")
            for row in m.buttons:
                print(" ", " | ".join([b.text for b in row]))

    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(test_navigation())
