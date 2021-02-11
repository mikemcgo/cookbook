import boto3
import pytest

from cookbook.backends.dynamo import DynamoBackend
from cookbook.cookbook import Cookbook


# Starts services from tests/docker-compose.yml
@pytest.fixture(scope='session')
def http_service(docker_ip, docker_services):
    """Ensure that HTTP service is up and responsive."""

    # `port_for` takes a container port and returns the corresponding host port
    url = 'http://{}:{}'.format(docker_ip, 8000)
    return url


@pytest.fixture(scope='function')
def cookbook(http_service):
    ddb = boto3.Session(region_name='us-east-2').resource('dynamodb', endpoint_url=http_service)
    table = ddb.create_table(
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'S'
            },
        ],
        TableName='cookbook',
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'
            },
        ],
        BillingMode='PAY_PER_REQUEST'
    )
    table.wait_until_exists()
    yield Cookbook(DynamoBackend(table))

    table.delete()
    table.wait_until_not_exists()


def test_table(cookbook):
    recipe = {'ingredients': ['dirt'], 'title': 'garbage'}
    recipe_id = cookbook.save(recipe)
    returned = cookbook.read(recipe_id)
    recipe.update(id=recipe_id)
    assert recipe == returned
    ids = cookbook.list()
    assert recipe_id in ids
    assert len(ids) == 1


def test_list_empty(cookbook):
    assert len(cookbook.list()) == 0
