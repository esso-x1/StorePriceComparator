import asyncio
from telethon import TelegramClient

API_ID = 31746395
API_HASH = "ad1d901ef2d348f3c1a85995ce420183"
SESSION_NAME = "J:/101/StorePriceComparator/userbot"

async def main():
    print("=" * 60)
    print("  Telegram Userbot Login - ربط جلسة تيليجرام للزاحف الآلي")
    print("=" * 60)
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    await client.start()
    
    me = await client.get_me()
    print("\n" + "=" * 60)
    print(f"✅ تم تسجيل الدخول بنجاح بحساب: {me.first_name} (@{me.username})")
    print("ملف الجلسة تم حفظه بنجاح وسيعمل الزاحف تلقائياً من الآن فصاعداً!")
    print("=" * 60)
    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
