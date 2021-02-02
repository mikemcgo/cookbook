from cookbook.backends.backend import Backend

class DynamoBackend(Backend):

    def __init__(self, table):
        pass

    def read(self, recipe_id):
        pass

    def save(self, recipe):
        pass

    def delete(self, recipe_id):
        pass

    def list(self):
        pass