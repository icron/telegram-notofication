import traceback

from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.types import PeerChannel, Message

from app.keywords.compare import Compare


class Client:
    def __init__(self, key: str, api_id: int, api_hash: str, comparator: Compare, bot, logging):
        self._api_id = api_id
        self._api_hash = api_hash
        self._client = TelegramClient(StringSession(key), api_id, api_hash)
        self._client.add_event_handler(self._handle_new_messages, events.NewMessage)
        self._bot = bot
        self._comparator = comparator
        self._logging = logging

    async def start(self):
        await self._client.start()
        await self._client.catch_up()

    def disconnect(self):
        self._client.disconnect()

    def run_until_disconnected(self):
        self._client.run_until_disconnected()

    async def _handle_new_messages(self, event):
        self._logging.info(event.raw_text)
        self._logging.info(event)

        try:
            msg = event.original_update.message
            if not isinstance(msg, Message):
                msg = event.message

            if msg.from_id is None or msg.from_id.user_id == self._bot.get_me()['id']:
                return

            for user_id, keywords in self._comparator.search_matched_keywords(event.raw_text, msg.peer_id.channel_id).items():
                text = await self._build_message(msg, keywords, event.raw_text)
                self._bot.send_message(chat_id=int(user_id), text=text)

        except Exception as e:
            self._logging.error(traceback.format_exc())

    async def _build_message(self, msg, keywords, raw_text: str) -> str:
        link = ''
        if isinstance(msg.peer_id, PeerChannel):
            channel = await self._client.get_entity(PeerChannel(msg.peer_id.channel_id))
            link = 'https://t.me/{0}/{1}'.format(channel.username, msg.id)

        text = "keywords: " + "\n".join([self.decorate_tags(keywords), raw_text, link])

        return text

    @staticmethod
    def decorate_tags(tags):
        res = []
        for item in tags:
            res.append("#" + item)

        return ', '.join(res)
