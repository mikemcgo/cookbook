from marshmallow import Schema, fields


class CommentSchema(Schema):
    id = fields.Number()
    content = fields.Str(required=True)
