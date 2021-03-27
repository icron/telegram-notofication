from botocore.client import BaseClient
from botocore.exceptions import ClientError
from flask_login import UserMixin


class User(UserMixin):
    id = None
    first_name = ""
    last_name = ""
    username = ""
    photo_url = ""
    moderated = False

    def __init__(self, id, first_name, last_name, username, photo_url):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.photo_url = photo_url

    def get_full_name(self):
        return "{0} {1}".format(self.first_name, self.last_name)

    def get_id(self):
        return int(self.id)

    def to_dict(self):
        return {
            'id': int(self.id),
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username,
            'photo_url': self.photo_url,
            'moderated': self.moderated
        }


class Users:
    def __init__(self, client: BaseClient):
        self.__client = client
        self._table = client.Table('Users')

    def list(self):
        try:
            response = self._table.query()
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            result = []
            for item in response['Items']:
                k = User(item.get('id'), item.get('first_name'), item.get('last_name'), item.get('username'),
                         item.get('photo_url'))
                result.append(k)

            return result

    def find(self, user_id: int):
        # try:
        res = self._table.get_item(
            Key={
                'id': user_id,
            }
        )

        res = res.get('Item', None)
        if res is None:
            return None

        u = User(
            id=res.get('id', 0),
            first_name=res.get('first_name', ''),
            last_name=res.get('last_name', ''),
            username=res.get('username', ''),
            photo_url=res.get('photo_url', ''),
        )

        return u

        # except self.__client.Client.exceptions.ResourceNotFoundException as e:
        #     return None

    def create(self, data):
        res = self._table.put_item(
            Item={
                'id': data.get('id'),
                'first_name': data.get('first_name', ''),
                'last_name': data.get('last_name', ''),
                'auth_date': data.get('auth_date', ''),
                'username': data.get('username', ''),
                'photo_url': data.get('photo_url', ''),
                'hash': data.get('hash'),
            }
        )

        u = User(
            id=data.get('id', 0),
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', ''),
            username=data.get('username', ''),
            photo_url=data.get('photo_url', '')
        )

        return u

    def delete(self, user_id: int):
        try:
            return self._table.delete_item(
                Key={
                    'id': user_id,
                },
            )
        except ClientError as e:
            if e.response['Error']['Code'] == "ConditionalCheckFailedException":
                return False
            else:
                raise
