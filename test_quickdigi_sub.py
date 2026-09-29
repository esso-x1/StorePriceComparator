import asyncio
from telethon import TelegramClient

API_ID = 31746395
API_HASH = "ad1d901ef2d348f3c1a85995ce420183"
SESSION_NAME = "J:/101/StorePriceComparator/userbot"

async def test_quickdigi_sub():
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    await client.connect()

    msgs = await client.get_messages("@QuickDigiBot", limit=3)
    for m in msgs:
        if m.buttons:
            for row in m.buttons:
                for b in row:
                    if "Digital Products" in b.text:
                        print("Clicking [Digital Products]...")
                        await b.click()
                        await asyncio.sleep(3)
                        break

    latest = await client.get_messages("@QuickDigiBot", limit=3)
    for m in latest:
        print(f"\nQuickDigi Reply ID {m.id}:\n{m.text}")
        if m.buttons:
            print("Buttons:")
            for row in m.buttons:
                print(" ", " | ".join([b.text for b in row]))

    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(test_quickdigi_sub())
