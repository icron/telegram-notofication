import asyncio
import boto3
import telegram
from os import environ

from app import client
from app.keywords.compare import Compare
from app.parser.parser import Parser

import logging
import sys

root = logging.getLogger()
root.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)

telegram_api_id = int(environ.get("TELEGRAM_API_ID", 0))
telegram_api_hash = str(environ.get("TELEGRAM_API_HASH", ""))
telegram_key = str(environ.get("TELEGRAM_KEY",""))
telegram_bot_token = str(environ.get("TELEGRAM_BOT_TOKEN", ""))

loop = asyncio.get_event_loop()
dynamoDb = boto3.resource('dynamodb')
parser = Parser()
bot = telegram.Bot(token=telegram_bot_token)
comparator = Compare(dynamoDb, parser)
t_client = client.Client(telegram_key, telegram_api_id, telegram_api_hash, comparator, bot, root)

try:
    loop.run_until_complete(t_client.start())
    t_client.run_until_disconnected()
finally:
    t_client.disconnect()