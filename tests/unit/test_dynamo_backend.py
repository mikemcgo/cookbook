

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
