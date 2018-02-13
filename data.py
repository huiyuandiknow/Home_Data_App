#Fake data for testing
# If received any existing address in our fake list --> result = the price in our fake data
#  else a concatenated of inputted data will return
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user2db2:123456@67.215.253.70:3306/user2db2'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user1db1:123456@67.215.253.70:3306/user1db1'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user1db1:123456@localhost:8889/user1db1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


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


def results(address, h_type, beds, baths):

    existing_address = Property.query.filter_by(address=address).first()

    fake_list = [
        {
            'id': 1,
            'price': '$299,000',
            'zillowPrice': '$288,000',
            'date': '02-01-218',
            'address': "address1"

        },
        {
            'id': 2,
            'price': '$189,099',
            'zillowPrice': '$288,000',
            'date': '02-01-218',
            'address': "address2"

        }
    ]
    res = ""

    # for el in fake_list:
    # if el['address'] == address:
    if existing_address:
        res = existing_address.price
    else:
        res = address + " " + h_type + " " + beds + " " + baths

    return res
