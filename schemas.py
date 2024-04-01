from marshmallow import Schema, fields

#schema for the cart model
class cartSchema(Schema):
    item_in_cart = fields.Str(dump_only=True)
    item_name = fields.Str(required=True)
    quantity = fields.Int(required = True)

#schema for the products model
class productsSchema(Schema):
    product_id = fields.Str(dump_only=True)
    product_name = fields.Str(required=True)
    product_price = fields.Int(required=True)
    product_description = fields.Str(required=True)

#schema for the user model
class userSchema(Schema):
    user_id = fields.Str(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)