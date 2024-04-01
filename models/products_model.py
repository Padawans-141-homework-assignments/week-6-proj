from app import db

class productModel(db.Model):

    __tablename__ = 'products'

    product_id = db.Column(db.Integer, primary_key = True)
    product_name = db.Column(db.String(50), nullable = False, unique = True)
    product_price = db.Column(db.Float, nullable = False)
    product_description = db.Column(db.String(500), nullable = False, unique = True)


    #adds and commits local information
    def add_product(self):
        db.session.add(self)
        db.session.commit()

    #saves local information to the database
    def save_product(self):
        db.session.add(self)
        db.session.commit()

    #deletes information from the database
    def del_product(self):
        db.session.delete(self)
        db.session.commit()

    #forms the requests for the database
    def from_products(self, dict):
        for k , v in dict.items():
            setattr(self, k, v)