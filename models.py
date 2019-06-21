from db import db


class Product(db.Model):
    __tablename__ = 'products'

    sku = db.Column(db.String(), primary_key=True, nullable=False, unique=True, index=True)
    name = db.Column(db.String())
    description = db.Column(db.String())
    status = db.Column(db.String())

    def __init__(self, sku, name, description, status):
        self.name = name
        self.sku = sku
        self.description = description
        self.status = status

    def response(self):
        return {
            'sku': self.sku,
            'name': self.name,
            'description': self.description,
            'status': self.status
        }
