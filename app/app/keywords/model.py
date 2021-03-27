from boto3.dynamodb.conditions import Key
from botocore.client import BaseClient
from botocore.exceptions import ClientError
from flask_login import current_user


class Keyword:
    uuid = None
    channels = ""
    user_id = None
    keywords = ""
    negative_keywords = ""
    use_default_filter_pos = False

    def __init__(self, uuid: str, user_id: int, channels: str, keywords: str):
        self.uuid = uuid
        self.user_id = user_id
        self.channels = channels
        self.keywords = keywords

    def get_keywords_as_array(self):
        keywords = self.keywords.split(',')
        res = []
        for kw in keywords:
            # skip composed keyword
            if '+' in kw:
                continue

            if kw.startswith('-'):
                res.append(kw[1:])
            else:
                res.append(kw)

        return res

    def get_composed_keywords_as_array(self):
        keywords = self.keywords.split(',')
        res = []
        for kw in keywords:
            if '+' in kw:
                composed_keywords = kw.split('+')
                res.append(composed_keywords)

        return res

    def get_channels_as_array(self):
        return self.channels.split(',')

    def get_negative_keywords_as_array(self):
        keywords = self.keywords.split(',')
        res = []
        for kw in keywords:
            # skip composed keyword
            if '+' in kw:
                continue
            if kw.startswith('-'):
                res.append(kw[1:])

        return res


class Keywords:
    def __init__(self, client: BaseClient):
        self._table = client.Table('Keywords')

    def get(self, k_uuid: str):
        try:
            response = self._table.get_item(Key={'uuid': k_uuid})
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            item = response['Item']

            return Keyword(item.get('uuid'), item.get('user_id'), item.get('channels', ''), item.get('keywords', ''))

    def list(self):
        try:
            response = self._table.query(
                IndexName='user_id-index',
                KeyConditionExpression=Key('user_id').eq(current_user.get_id())
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            result = []
            for item in response['Items']:
                k = Keyword(item.get('uuid'), item.get('user_id'), item.get('channels', ''), item.get('keywords', ''))
                result.append(k)

            return result

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
                k = Keyword(item.get('uuid'), item.get('user_id'), item.get('channels', ''), item.get('keywords', ''))
                result.append(k)

            return result

    def create(self, model: Keyword):
        return self._table.put_item(
            Item={
                'uuid': model.uuid,
                'channels': model.channels,
                'user_id': current_user.get_id(),
                'keywords': model.keywords
            }
        )

    def update(self, data: Keyword):
        try:
            return self._table.update_item(
                Key={
                    'uuid': data.uuid
                },
                UpdateExpression="set channels=:channels, keywords=:keywords",
                ExpressionAttributeValues={
                    ':channels': data.channels,
                    ':keywords': data.keywords,
                },
                ReturnValues="UPDATED_NEW"
            )
        except ClientError as e:
            if e.response['Error']['Code'] == "ConditionalCheckFailedException":
                return False
            else:
                raise

    def delete(self, k_uuid: str):
        try:
            return self._table.delete_item(
                Key={
                    'uuid': k_uuid,
                },
            )
        except ClientError as e:
            if e.response['Error']['Code'] == "ConditionalCheckFailedException":
                return False
            else:
                raise
