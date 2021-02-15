import pytest

from cookbook.backends.backend import BackendException
from cookbook.backends.local_backend import LocalBackend
from cookbook.cookbook import Cookbook, CookbookException


@pytest.fixture(scope='function')
def local(tmpdir):
    return Cookbook(LocalBackend(tmpdir.strpath))


def test_happy_path(local):
    recipe = {'title': 'recip1', 'ingredients': ['dirt']}
    recipe_id = local.save(recipe)
    assert recipe_id
    returned = local.read(recipe_id)
    for key, item in recipe.items():
        assert item == returned.get(key)
    assert recipe_id in local.list()
    returned.update(steps=['abcd'])
    local.save(returned)
    updated = local.read(recipe_id)
    assert 'abcd' in updated.get('steps')
    local.delete(updated.get('id'))
    assert len(local.list()) == 0


def test_empty_read(local):
    with pytest.raises(CookbookException):
        local.read('1234')


def test_bad_obj(local):
    with pytest.raises(CookbookException):
        local.save({'id': 'abcd'})


def test_first_write(local):
    local.save({'id': '4a2c6f07-5286-4665-9875-7babd8719192', 'ingredients': ['asdf'], 'title': 'nah'})


def test_nonexist_delete(local):
    local.delete('abcd')


def test_unwanted_fields(local):
    with pytest.raises(CookbookException):
        local.save({'ingredients': ['dirt'], 'title': 'garbage', 'badthings': 'i123'})
