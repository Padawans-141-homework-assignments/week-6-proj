from models.products_model import productModel

from flask import jsonify

from flask.views import MethodView

from flask_smorest import abort

from flask_jwt_extended import jwt_required

from schemas import productsSchema

from . import bpproduct

#route that grabs all the products
@bpproduct.route('/products')
class prodResourceList(MethodView):

    @bpproduct.response(200, productsSchema(many=True))
    def get(self):
        try:
            return productModel.query.all(), 200
        except:
            abort(400, message = 'There was an error collecting the information from the db :(')

#route that gets the information on a specific product based on id
@bpproduct.route('/products/<int:id>')
class prodResource(MethodView):
    def get(self, id):
        #grabs the product at the with the given id
        product = productModel.query.get(id)
        #if that product exists
        if product:
            #return all of its details
            return {"name" : product.product_name,
                    "price" : product.product_price,
                    "description" : product.product_description}, 200
        else:
            #return error if it doesn't
            return {"error" : "No product with that ID in the database."}, 400


#Creates item in products
#     @bpproduct.arguments(productsSchema)
#     @bpproduct.response(201, productsSchema)
#     def post(self, data):
#         try:
#             #grabs product Model
#             prod_layout = productModel()
#             #forms the data from the request
#             prod_layout.from_products(data)
#             #saves the data to the table
#             prod_layout.save_product()
#             #confirms addition to the database
#             return jsonify({'Confirmed' : 'Product was successfully added to the products database.'}), 201

#         except:
#             #aborts if an error occurs
#             abort(400, message = 'There was a problem entering it into the database.')

#updates items in products
# @bpproduct.route('/products/<int:id>')
# class prodResource(MethodView):

#     @bpproduct.arguments(productsSchema)
#     def put(self, data, id):

#         #grabs the product Model at a specified id
#         product = productModel.query.get(id)

#         try:
#             #forms the request data
#             product.from_products(data)
#             #saves the product data to the table
#             product.save_product()
#             return {"Confirmed" : "Provided product has updated successfully."}
#         except:
#             #aborts if an error pops up
#             abort(400, message = 'There is no product with that id.')

#     def delete(self, id):

#             #grabs product at given id
#             product = productModel.query.get(id)

#             #if that product id exists
#             if product:
#                 #delete the product at the id
#                 product.del_product()
#                 return {'Confirmation' : 'Product is now deleted from the product selections.'}, 200
#             else:
#                 #aborts if an error pops up
#                 abort(400, message = 'Product with that ID not found.')