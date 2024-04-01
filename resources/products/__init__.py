from flask_smorest import Blueprint

bpproduct = Blueprint('product', 'product', description='Holds all the products of the shop.')

from . import products_res