from marshmallow.exceptions import ValidationError
from cookbook.recipe import RecipeSchema


# Cookbook translates between front end tech (webserver, cli, etc) and backend (debug, db, etc)
class Cookbook:

    def __init__(self, backend):
        self._backend = backend

    # Raises ValidationError, or os.path errors
    def save(self, body):
        try:
            parsed = RecipeSchema().load(body)
        except ValidationError as e:
            raise CookbookException(e.messages) from e
        return self._backend.save(parsed)

    # Validate returned fields, add empty fields
    def read(self, recipe_id):
        return self._backend.read(recipe_id)

    def delete(self, recipe_id):
        return self._backend.delete(recipe_id)

    def list(self):
        return self._backend.list()


class CookbookException(Exception):
    def __init__(self, messages):
        self.messages = messages
        super().__init__(self.messages)
