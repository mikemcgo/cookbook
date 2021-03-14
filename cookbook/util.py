import boto3


def get_test_table(region, endpoint_url, table_name):
    fake_creds = {
        'aws_access_key_id': 'a',
        'aws_secret_access_key': 'b',
        'aws_session_token': 'c'
    }
    ddb = boto3.Session(region_name=region, **fake_creds).resource('dynamodb', endpoint_url=endpoint_url)
    if len(list(ddb.tables.all())) > 0:
        table = ddb.Table(table_name)
    else:
        table = ddb.create_table(
            AttributeDefinitions=[
                {
                    'AttributeName': 'id',
                    'AttributeType': 'S'
                },
            ],
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'id',
                    'KeyType': 'HASH'
                },
            ],
            BillingMode='PAY_PER_REQUEST'
        )
        table.wait_until_exists()
    return table
