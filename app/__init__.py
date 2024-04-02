import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_smorest import Api

from Config import Config

app = Flask(__name__)
app.config.from_object(Config)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_PROJ_URL')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models.cart_model import cartModel
from models.products_model import productModel
from models.user_model import userModel

from resources.cart import bpcart as cart_bp
app.register_blueprint(cart_bp)
from resources.products import bpproduct as product_bp
app.register_blueprint(product_bp)
from resources.loginandout import bplog as login_bp
app.register_blueprint(login_bp)

app.run()