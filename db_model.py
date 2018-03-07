from flask_sqlalchemy import SQLAlchemy

from flask_config import get_app

app = get_app()
db = SQLAlchemy(app)
file = None


class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    address = db.Column(db.String(160), unique=True)
    beds = db.Column(db.Integer)
    baths = db.Column(db.Integer)
    h_type = db.Column(db.String(20))
    price = db.Column(db.Integer)

    def __init__(self, address, beds, baths, h_type):
        self.address = address
        self.beds = beds
        self.baths = baths
        self.baths = h_type


def existing_address(address, living, beds, baths, lot, year):
    existing_address = Property.query.filter_by(address=address).first()
    if existing_address:
        res = existing_address.price
    else:
        res = address + " " + living + " " + beds + " " + baths + " " + lot
    return res
