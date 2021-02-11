from abc import ABC, abstractmethod

class Backend(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def read(self, recipe_id):
        pass

    @abstractmethod
    def save(self, recipe):
        pass

    @abstractmethod
    def delete(self, recipe_id):
        pass

    @abstractmethod
    def list(self):
        pass


class BackendException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
