from os import environ

from telethon import TelegramClient, events
from telethon.sessions import StringSession

telegram_api_id = int(environ.get("TELEGRAM_API_ID", 0))
telegram_api_hash = str(environ.get("TELEGRAM_API_HASH", ""))
with TelegramClient(StringSession(), telegram_api_id, telegram_api_hash) as client:
    print(client.session.save())