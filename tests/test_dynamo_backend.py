import pytest

from cookbook.backends.dynamo import DynamoBackend
from cookbook.cookbook import Cookbook
from cookbook.util import get_test_table


# Starts services from tests/docker-compose.yml
@pytest.fixture(scope='session')
def http_service(docker_ip, docker_services):
    """Ensure that HTTP service is up and responsive."""

    # `port_for` takes a container port and returns the corresponding host port
    url = 'http://{}:{}'.format(docker_ip, 8000)
    return url


@pytest.fixture(scope='function')
def cookbook(http_service):
    table = get_test_table('us-east-2', http_service, cookbook)
    yield Cookbook(DynamoBackend(table))

    table.delete()
    table.wait_until_not_exists()


def test_happy_path(cookbook):
    recipe = {'ingredients': ['dirt'], 'title': 'garbage'}
    recipe_id = cookbook.save(recipe)
    returned = cookbook.read(recipe_id)
    recipe.update(id=recipe_id)
    assert recipe == returned
    ids = cookbook.list()
    assert recipe_id in ids
    assert len(ids) == 1
    cookbook.delete(recipe_id)
    assert len(cookbook.list()) == 0
