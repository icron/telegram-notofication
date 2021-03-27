from app.keywords.model import Keywords
from app.parser.parser import Parser
from app.util.util import levenshtein


class Compare:
    min_levenshtein_len = 5

    def __init__(self, dynamodb, parser: Parser):
        self._dynamodb = dynamodb
        self._parser = parser

    def search_matched_keywords(self, msg: str, channel_id: int):
        """
        Compares keywords from database and message_keywords
        Returns dictionary where key - user_id, value - keywords
        """
        result = {}
        message_keywords = self._parser.parse(msg, False)

        models = Keywords(self._dynamodb).all()
        for model in models:
            if str(channel_id) not in model.get_channels_as_array():
                continue

            keywords_from_storage = self._get_normalised_keywords(model.get_keywords_as_array(), model.use_default_filter_pos)
            negative_keywords = self._get_normalised_keywords(model.get_negative_keywords_as_array(), model.use_default_filter_pos)

            if self._has_negative_keyword(message_keywords, negative_keywords):
                return {}

            crossed_keywords = self._get_crossed_keywords(
                message_keywords,
                keywords_from_storage
            )
            if len(crossed_keywords) > 0:
                self._append_keywords_to_user(result, int(model.user_id), crossed_keywords)

            # composed keywords
            composed_keywords_raw = model.get_composed_keywords_as_array()
            for item_composed_keywords in composed_keywords_raw:
                composed_keywords = self._get_normalised_keywords(item_composed_keywords, model.use_default_filter_pos)
                crossed_composed_keywords = self._get_crossed_keywords(
                    message_keywords,
                    composed_keywords
                )

                # if all composed words from group exists in text
                if len(crossed_composed_keywords) > 0 and len(crossed_composed_keywords) == len(item_composed_keywords):
                    self._append_keywords_to_user(result, int(model.user_id), crossed_composed_keywords)

        return result

    def _has_negative_keyword(self, keywords_from_storage, negative_keywords):
        for keyword_from_storage in keywords_from_storage:
            if keyword_from_storage in negative_keywords:
                return True

        return False

    def _get_crossed_keywords(self, message_keywords, keywords_from_storage):
        res = []
        for keyword_from_storage in keywords_from_storage:
            for message_keyword in message_keywords:
                if self._compare_keywords(keyword_from_storage, message_keyword):
                    res.append(keyword_from_storage)

        return res

    def _get_normalised_keywords(self, keywords, use_default_filter_pos: bool):
        res = []
        for kw in keywords:
            parsed = self._parser.parse(kw, use_default_filter_pos)
            if parsed:
                res.append(self._parser.parse(kw, use_default_filter_pos)[0])

        return res

    def _append_keywords_to_user(self, haystack, user_id: int, keywords):
        for ckw in keywords:
            if user_id not in haystack:
                haystack[user_id] = []

            haystack[user_id].append(ckw)

    def _compare_keywords(self, key1: str, key2: str) -> bool:
        if len(key1) > self.min_levenshtein_len and len(key2) > self.min_levenshtein_len:
            return levenshtein(key1, key2) <= 1
        else:
            return key1 == key2
