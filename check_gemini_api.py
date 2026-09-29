import asyncio
from telethon import TelegramClient

API_ID = 31746395
API_HASH = "ad1d901ef2d348f3c1a85995ce420183"
SESSION_NAME = "J:/101/StorePriceComparator/userbot"

async def check():
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    await client.connect()
    if not await client.is_user_authorized():
        print("Not logged in")
        return

    print("Sending text: 🔌 API Reseller")
    await client.send_message("@GeminiPixel1_bot", "🔌 API Reseller")
    await asyncio.sleep(3)

    msgs = await client.get_messages("@GeminiPixel1_bot", limit=3)
    for m in msgs:
        print("=== MESSAGE ===")
        print(m.text)
        if m.reply_markup and hasattr(m.reply_markup, 'rows'):
            for row in m.reply_markup.rows:
                for b in row.buttons:
                    u = getattr(b, 'url', None)
                    w = getattr(b, 'web_app', None)
                    print(f"Button: text='{b.text}' url='{u}' web_app='{getattr(w, 'url', None)}'")

    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(check())
