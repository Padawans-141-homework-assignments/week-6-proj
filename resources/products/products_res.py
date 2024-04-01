from models.products_model import productModel

from flask.views import MethodView

from flask_smorest import abort

from flask_jwt_extended import jwt_required

from schemas import productsSchema

from . import bpproduct

@bpproduct.route('/products')
class prodResourceList(MethodView):

    @bpproduct.response(200, productsSchema(many=True))
    def get(self):
        try:
            return productModel.query.all()
        except:
            abort(400, message = 'There was an error collecting the information from the db :(')

    @bpproduct.arguments(productsSchema)
    @bpproduct.response(201, productsSchema)
    def post(self, data):
        try:
            prod_layout = productModel()

            prod_layout.from_products(data)

            prod_layout.save_product()

            return {'Confirmed' : 'Product was successfully added to the products database.'}

        except:

            abort(400, message = 'There was a problem entering it into the database.')


@bpproduct.route('/products/<int:id>')
class prodResource(MethodView):

    @bpproduct.arguments(productsSchema)
    def put(self, data, id):
        product = productModel.query.get(id)

        try:

            product.from_products(data)

            product.save_product()
            return {"Confirmed" : "Provided product has updated successfully."}
        except:
            abort(400, message = 'There is no product with that id.')

    def delete(self, id):
        
        product = productModel.query.get(id)

        if product:

            product.del_product()
            return {'Confirmation' : 'Product is now deleted from the product selections.'}
        else:

            abort(400, message = 'Product with that ID not found.')