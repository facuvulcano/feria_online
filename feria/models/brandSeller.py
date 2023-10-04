from feria.extensions import db


class BrandSeller(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    rating = db.Column(db.Float, default=0)
    social_media = db.Column(db.String(120))
    proof_of_stock = db.Column(db.String(120))
    clothing_models = db.Column(db.String(120))
    approved = db.Column(db.Boolean, default=False)
    notification = db.Column(db.Boolean, default=False)
