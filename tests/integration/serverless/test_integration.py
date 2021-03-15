import pytest
import requests
import uuid


@pytest.fixture(scope='function')
def driver(request, dynamo_service):
    # If Mocker is imported in the global scope, it eventually tries to make a dynamodb table before dynamo starts
    # This is gross but it seems to work
    from tests.integration.serverless.lambda_testing_shim import Mocker
    target_installation = request.config.getoption("--url")

    if 'nil' in target_installation:
        session = Mocker(target_installation)
    else:
        session = requests.session()

    yield session, target_installation

    # if 'nil' not in target_installation:
    #     recipes = session.get(target_installation)
    #     for recipe_id in recipes:
    #         session.delete(target_installation + '/' + str(recipe_id))


def test_empty_list(driver):
    resp = driver[0].get(driver[1])
    assert resp.json() == []


def test_happy_path(driver):
    recipe = {'ingredients': ['dirt'], 'title': 'garbage'}

    # post recipe to thing
    resp = driver[0].post(driver[1], json=recipe).json()

    assert 'id' in resp

    recipe = driver[0].get(driver[1] + '/' + resp.get('id')).json()

    assert recipe.get('title') == 'garbage'

    recipe.update(ingredients=['dirt', 'grime'])

    resp = driver[0].put(driver[1] + '/' + resp.get('id'), json=recipe).json()

    assert 'id' in resp

    recipe = driver[0].get(driver[1] + '/' + resp.get('id')).json()

    assert recipe.get('ingredients') == ['dirt', 'grime']

    driver[0].delete(driver[1] + '/' + resp.get('id'))

    resp = driver[0].get(driver[1])
    assert resp.json() == []


def test_bad_get(driver):
    resp = driver[0].get(driver[1] + '/' + str(uuid.uuid4())).json()
    assert 'errors' in resp
