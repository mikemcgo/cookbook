from boto3.dynamodb.table import TableResource

from cookbook.backends.backend import Backend, BackendException


# Backed by https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#table
class DynamoBackend(Backend):

    def __init__(self, table):
        super().__init__()
        if not isinstance(table, TableResource):
            raise BackendException(f'boto3 dyanmodb table resource expected, instead received {type(table)}')
        self._table = table

    def read(self, recipe_id):
        resp = self._table.get_item(
            Key={
                'id': recipe_id
            })
        return resp.get('Item')

    # TODO: this might be over-simplified
    def save(self, recipe):
        self._table.put_item(
            Item=recipe
        )
        return recipe.get('id')

    # TODO: this might be over-simplified
    def delete(self, recipe_id):
        self._table.delete_item(
            Key={
                'id': recipe_id
            },
            ReturnValues='NONE'
        )
        return None

    # This does not scale
    def list(self):
        ids = []
        last_scanned = 'val'
        while last_scanned:
            resp = self._table.scan(
                ProjectionExpression="id"
            )
            ids.extend(map(lambda a: a.get('id'), resp.get('Items')))
            last_scanned = resp.get('LastEvaluatedKey')

        return ids