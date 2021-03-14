import pytest

from cookbook.backends.dynamo import DynamoBackend
from cookbook.cookbook import Cookbook
from cookbook.util import get_test_table


def pytest_addoption(parser):
    parser.addoption(
        "--url", action="store", default="nil/dev/cookbook", help="nil indicates usage of shim"
    )


# Starts services from tests/docker-compose.yml
@pytest.fixture(scope='module')
def dynamo_service(docker_ip, docker_services):
    """Ensure that HTTP service is up and responsive."""

    # `port_for` takes a container port and returns the corresponding host port
    url = 'http://{}:{}'.format(docker_ip, 8000)
    return url


@pytest.fixture(scope='function')
def cookbook(dynamo_service):
    table = get_test_table('us-east-2', dynamo_service, 'cookbook-recipes-dev')
    yield Cookbook(DynamoBackend(table))
    table.delete()
    table.wait_until_not_exists()
