from .shared import db


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(80), nullable=False)
    image = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"<Product {self.name}>"
