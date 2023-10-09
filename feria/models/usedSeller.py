from feria.extensions import db


class UsedSeller(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    rating = db.Column(db.Float, default=0)
    social_media = db.Column(db.String(120))
    contact_number = db.Column(db.String(20))
    location = db.Column(db.String(120))
    number_of_items = db.Column(db.Integer)
    approved = db.Column(db.Boolean, default=False)
    notification = db.Column(db.Boolean, default=False)
    items_sold = db.Column(db.Integer, default=0)