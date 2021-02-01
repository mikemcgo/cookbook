from marshmallow import Schema, fields


class IngredientSchema(Schema):
    # Possibly validate for measurements systems + pinch, etc
    unit = fields.Str(required=True)
    amount = fields.Number(required=True)
    name = fields.Str(required=True)
