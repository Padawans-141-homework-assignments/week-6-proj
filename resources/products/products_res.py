from models.products_model import productModel

from flask import jsonify

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


@bpproduct.route('/products/<int:id>')
class prodResource(MethodView):

    
    def get(self, id):

        product = productModel.query.get(id)

        if product:
            return {"name" : product.product_name,
                    "price" : product.product_price,
                    "description" : product.product_description}
        else:
            return {"error" : "No product with that ID in the database."}