from flask_smorest import Blueprint

bpcart = Blueprint('cart', 'cart', description='Holds the contents of the user cart.')

from . import cart_res