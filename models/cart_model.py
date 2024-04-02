from app import db

class cartModel(db.Model):

    #sets table name
    __tablename__ = 'cart'

    #sets table outline
    item_id = db.Column(db.Integer, primary_key= True)
    item_name = db.Column(db.String(50), nullable = False)
    quantity = db.Column(db.Integer, nullable = False)
    item_price = db.Column(db.Float, nullable = False)

    #adds and commits local information
    def add_2_cart(self):
        db.session.add(self)
        db.session.commit()

    #saves local information to the database
    def save_cart(self):
        db.session.add(self)
        db.session.commit()

    #deletes information from the database
    def del_item(self):
        db.session.delete(self)
        db.session.commit()

    #forms the requests for the database
    def form_cart (self, dict):
        for k , v in dict.items():
            setattr(self, k, v)