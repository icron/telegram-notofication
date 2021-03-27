from botocore.client import BaseClient
from botocore.exceptions import ClientError


class Channel:
    id = None
    title = ""
    link = ""

    def __init__(self, id: int, title: str, link: str):
        self.id = id
        self.title = title
        self.link = link


class Channels:
    def __init__(self, client: BaseClient):
        self._table = client.Table('Channels')

    def all(self):
        """
        For all users
        """
        try:
            response = self._table.scan()
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            result = []
            for item in response['Items']:
                k = Channel(item.get('id'), item.get('title', ''), item.get('link', ''))
                result.append(k)

            return result

    @staticmethod
    def list_to_dict(items):
        res = {}
        for item in items:
            res[str(item.id)] = item

        return res
