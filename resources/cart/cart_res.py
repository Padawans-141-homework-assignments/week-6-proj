from models.cart_model import cartModel

from flask import jsonify

from flask.views import MethodView

from flask_smorest import abort

from flask_jwt_extended import jwt_required

from schemas import cartSchema

from . import bpcart

#route that returns the contents of the cart and current cart total
@bpcart.route('/cart')
class cartResourceList(MethodView):
    #requires the user to be loggen in to access this route
    @jwt_required()
    @bpcart.response(200, cartSchema(many=True))
    def get(self):
    
        try:
            #grabs the contents of the cart table
            cart = cartModel.query.all()

            # Serializing them so it can be output in the return
            cart_contents = cartSchema(many=True).dump(cart)

            #initializes the cart amount to 0
            cart_total = 0

            #grabs the price and quantities rows
            prices = cartModel.query.with_entities(cartModel.item_price, cartModel.quantity).all()

            #for every row in the grabed rows
            for row in prices:
                #set the current total to its current plus the price * quantity
                cart_total = cart_total + (row.item_price * row.quantity)

            #returns the contents and the sum of all the items in the cart
            return jsonify({"Cart Contents" : f'{cart_contents}',
                            "Current cart total" : f'${cart_total}'}), 200
        except:
            abort(400, message = 'There was an error collecting the information from the db :(')

    #requires the user to be loggen in to access this route
    @jwt_required()
    #creates cart
    @bpcart.arguments(cartSchema)
    @bpcart.response(201, cartSchema)
    #adds item to cart
    def post(self, data):

        try:
            #calls the cart Model
            cart_layout = cartModel()

            #forms the passed in data for the cart
            cart_layout.form_cart(data)

            #saves the info to the cart
            cart_layout.save_cart()

            #confirms addition of new cart
            return jsonify({'Confirmed' : 'Item was successfully added to the cart database.'}), 200

        except:
            #notifies of any errors
            abort(400, message = 'There was a problem entering it into the database.')

#Route to delete entire cart
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
        return jsonify({"Confirmation" : 'All the items in the cart have been deleted'}),200
        
#route to delete specific cart item by id
@bpcart.route('/cart/<int:id>')
class cartResource(MethodView):
    def delete(self, id):
        
        #grabs product at the given id endpoint
        product = cartModel.query.get(id)

        if product:
            #deletes the product at that id if it exists
            product.del_item()
            return {'Confirmation' : 'Given item is now deleted from the cart.'}, 200
        else:
            #returns with abort if it isn't found
            abort(400, message = 'Item with that ID not found.')