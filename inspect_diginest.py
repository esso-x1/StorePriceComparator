import asyncio
from telethon import TelegramClient

API_ID = 31746395
API_HASH = "ad1d901ef2d348f3c1a85995ce420183"
SESSION_NAME = "J:/101/StorePriceComparator/userbot"

async def check_diginest():
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    await client.connect()
    if not await client.is_user_authorized():
        print("Not logged in")
        return

    print("Sending /start to @DIGINEST1BOT...")
    await client.send_message("@DIGINEST1BOT", "/start")
    await asyncio.sleep(3)

    msgs = await client.get_messages("@DIGINEST1BOT", limit=3)
    for m in msgs:
        print("=== Message ===")
        print(m.text)
        if m.buttons:
            for row in m.buttons:
                for b in row:
                    u = getattr(b, 'url', None)
                    w = getattr(b, 'web_app', None)
                    print(f"Button: text='{b.text}' url='{u}' web_app='{getattr(w, 'url', None)}'")

    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(check_diginest())
