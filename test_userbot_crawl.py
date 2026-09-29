import asyncio
from telethon import TelegramClient

API_ID = 31746395
API_HASH = "ad1d901ef2d348f3c1a85995ce420183"
SESSION_NAME = "J:/101/StorePriceComparator/userbot"

async def inspect_bot(client, bot_username):
    print(f"\n==========================================")
    print(f"Testing Bot: {bot_username}")
    print(f"==========================================")
    try:
        # Send /start
        await client.send_message(bot_username, "/start")
        print("Sent /start, waiting 3 seconds for response...")
        await asyncio.sleep(3)

        # Get last 3 messages from the bot
        messages = await client.get_messages(bot_username, limit=3)
        for msg in messages:
            print(f"\n[Message from {bot_username}] ID: {msg.id}")
            print(f"Text:\n{msg.text}")
            if msg.buttons:
                print("Buttons:")
                for row in msg.buttons:
                    row_texts = [f"[{b.text}]" for b in row]
                    print("  ", " | ".join(row_texts))
    except Exception as e:
        print(f"Error communicating with {bot_username}: {e}")

async def main():
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    await client.connect()
    if not await client.is_user_authorized():
        print("User not authorized!")
        return

    for bot in ["@QuickDigiBot", "@aishopmopsbot"]:
        await inspect_bot(client, bot)

    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
