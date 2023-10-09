from feria.extensions import db

class ClothingItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand_seller_id = db.Column(db.Integer, db.ForeignKey('brand_seller.id'), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(120))
    
