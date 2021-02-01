import os
import uuid
import yaml

from cookbook.backends.backend import BackendException


class LocalBackend:

    def __init__(self, target_dir="."):
        self._target_dir = target_dir

    def read(self, recipe_id):
        try:
            with open(file=os.path.join(self._target_dir, recipe_id)) as f:
                recipe = yaml.safe_load(f)
        except OSError as e:
            raise BackendException(f'{recipe_id} not found') from e
        return recipe

    def save(self, recipe):
        recipe_id = recipe.get('id')

        # Do not allow users to set the ID
        if not recipe_id:
            recipe_id = str(uuid.uuid4())
            recipe.update(id=recipe_id)
        elif recipe_id not in self.list():
            raise BackendException('Used defined IDs are not allowed, recipe does not yet exist')

        with open(file=os.path.join(self._target_dir, recipe_id), mode='w') as f:
            yaml.dump(recipe, f)

        return recipe_id

    def delete(self, recipe_id):
        os.remove(os.path.join(self._target_dir, recipe_id))
        return None

    def list(self):
        return os.listdir(self._target_dir)
