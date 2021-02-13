import os

import yaml

from cookbook.backends.backend import Backend, BackendException


class LocalBackend(Backend):

    def __init__(self, target_dir="."):
        super().__init__()
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

        with open(file=os.path.join(self._target_dir, recipe_id), mode='w') as f:
            yaml.dump(recipe, f)

        return recipe_id

    def delete(self, recipe_id):
        try:
            os.remove(os.path.join(self._target_dir, recipe_id))
        except FileNotFoundError:
            pass
        return None

    def list(self):
        return os.listdir(self._target_dir)
