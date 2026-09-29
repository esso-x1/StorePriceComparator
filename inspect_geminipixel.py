import asyncio
from telethon import TelegramClient

API_ID = 31746395
API_HASH = "ad1d901ef2d348f3c1a85995ce420183"
SESSION_NAME = "J:/101/StorePriceComparator/userbot"

async def inspect_geminipixel():
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    await client.connect()
    if not await client.is_user_authorized():
        print("Not authorized")
        return

    print("Sending /start to @GeminiPixel1_bot...")
    await client.send_message("@GeminiPixel1_bot", "/start")
    await asyncio.sleep(3)

    msgs = await client.get_messages("@GeminiPixel1_bot", limit=5)
    for m in msgs:
        print("--- Message ---")
        print("Text:", m.text)
        if m.reply_markup:
            print("Reply Markup type:", type(m.reply_markup))
            if hasattr(m.reply_markup, 'rows'):
                for row in m.reply_markup.rows:
                    for b in row.buttons:
                        print(f"Button: text='{b.text}', data={getattr(b, 'data', None)}, url={getattr(b, 'url', None)}")
                        # Check for web_app button
                        if hasattr(b, 'web_app') and b.web_app:
                            print(f"WEB APP URL: {b.web_app.url}")

    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(inspect_geminipixel())
