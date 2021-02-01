import typing

from marshmallow import Schema, fields


class UUIDString(fields.UUID):

    def _deserialize(self, value, attr, obj, **kwargs) -> typing.Optional[str]:
        return str(self._validated(value))


class RecipeSchema(Schema):
    id = UUIDString()
    title = fields.Str(required=True)
    steps = fields.List(fields.Str)
    feedback = fields.Str()
    ingredients = fields.List(fields.Str, required=True)
