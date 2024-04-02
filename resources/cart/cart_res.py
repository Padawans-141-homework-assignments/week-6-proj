from models.cart_model import cartModel

from flask import jsonify

from flask.views import MethodView

from flask_smorest import abort

from flask_jwt_extended import jwt_required

from schemas import cartSchema

from . import bpcart

@bpcart.route('/cart')
class cartResourceList(MethodView):
    @bpcart.response(200, cartSchema(many=True))
    def get(self):
    
        try:
            return cartModel.query.all()
        except:
            abort(400, message = 'There was an error collecting the information from the db :(')

    @jwt_required()
    @bpcart.arguments(cartSchema)
    @bpcart.response(201, cartSchema)
    def post(self, data):

        try:
            cart_total = 0

            cart_layout = cartModel()

            cart_layout.form_cart(data)

            cart_layout.save_cart()

            prices = cartModel.query.with_entities(cartModel.item_price, cartModel.quantity).all()

            for row in prices:
                cart_total = cart_total + (row.item_price * row.quantity)

            return jsonify({'Confirmed' : 'Cart was successfully added to the carts database.',
                    'Current cart total' : f'${cart_total}'})

        except:

            abort(400, message = 'There was a problem entering it into the database.')

@bpcart.route('/empty-cart')
class emptyResource(MethodView):
    def delete(self):

        # Grabs the column of the table that has all the ID's
        id_list = cartModel.query.with_entities(cartModel.item_id).all()

        # Goes through the id_list and creates a list of all the id values
        id_list = [id[0] for id in id_list]

        # for every item in the list containing all ID's
        for item in id_list:

            # grabs the information at the ID's row
            item_id = cartModel.query.get(item)

            # if an id exists / was grabbed
            if item_id:
                # delete it
                item_id.del_item()
            # if none was found
            else:
                # outputs an error to the user
                abort(400, message = "item with that ID not found in the database.")

        # confirms the carts contents has been deleted
        return jsonify({"Confirmation" : 'All the items in the cart have been deleted'})
        

@bpcart.route('/cart/<int:id>')
class cartResource(MethodView):

    def delete(self, id):
        
        product = cartModel.query.get(id)

        if product:

            product.del_item()
            return {'Confirmation' : 'Given item is now deleted from the cart.'}
        else:

            abort(400, message = 'Item with that ID not found.')