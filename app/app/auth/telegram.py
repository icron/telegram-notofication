import hashlib
import hmac
import time


class Telegram:
    def __init__(self, data, bot_token: str):
        self.__data = data
        self.__bot_token = bot_token

    def get_data(self):
        data = dict(self.__data)
        del data['hash']

        return data

    def check(self):
        data = dict(self.__data)
        check_hash = data['hash']

        del data['hash']
        data_check_attr = []
        for key, value in data.items():
            data_check_attr.append(key + '=' + str(value))
        data_check_attr.sort()

        data_check_string = "\n".join(data_check_attr)

        h = hashlib.sha256()
        h.update(self.__bot_token.encode('utf-8'))
        secret_key = h.digest()

        data_hash = self.hash_hmac(secret_key, data_check_string.encode('utf-8'))

        if data_hash != check_hash:
            return False

        if time.time() - data['auth_date'] > 86400:
            return False

        return True

    @staticmethod
    def hash_hmac(key, data):
        return hmac.new(key, data, hashlib.sha256).hexdigest()
