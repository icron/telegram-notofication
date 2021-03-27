import boto3


def create_keywords_table(dynamodb):
    table = dynamodb.create_table(
        TableName='Keywords',
        KeySchema=[
            {
                'AttributeName': 'uuid',
                'KeyType': 'HASH'  # Partition key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'uuid',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    return table


def create_channels_table(dynamodb):
    table = dynamodb.create_table(
        TableName='Channels',
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'  # Partition key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'N'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    return table


def create_user_table(dynamodb):
    table = dynamodb.create_table(
        TableName='Users',
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'  # Partition key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'N'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    return table


if __name__ == '__main__':
    dynamoDb = boto3.client('dynamodb')
    try:
        keywords_table = create_keywords_table(dynamoDb)
        print("Table status:", keywords_table.table_status)
    except dynamoDb.exceptions.ResourceInUseException as e:
        pass

    try:
        channels_table = create_channels_table(dynamoDb)
        print("Table status:", channels_table.table_status)
    except dynamoDb.exceptions.ResourceInUseException as e:
        pass

    try:
        user_table = create_user_table(dynamoDb)
        print("Table status:", user_table.table_status)
    except dynamoDb.exceptions.ResourceInUseException as e:
        pass

    # TODO For sessions and set TTL for table
    # aws dynamodb create-table --profile PROFILE --region eu-west-1 --key-schema "AttributeName=id,KeyType=HASH" \
    # --attribute-definitions "AttributeName=id,AttributeType=S" \
    # --provisioned-throughput "ReadCapacityUnits=5,WriteCapacityUnits=5" \
    # --table-name Sessions
