#Fake data for testing
# If received any existing address in our fake list --> result = the price in our fake data
#  else a concatenated of inputted data will return
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import pickle
import os

app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user2db2:123456@67.215.253.70:3306/user2db2'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user1db1:123456@67.215.253.70:3306/user1db1'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user1db1:123456@localhost:8889/user1db1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
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
    if beds == '':
        beds = '2'
    if beds == '5+':
        beds = '5'
    if baths == '':
        baths = '1'
    house = '{"1":{"bedrooms":'+'"'+beds+'"' +',"bathrooms":"' + baths +'","sqft_living":"1800","sqft_lot":"6000","zipcode":"98058"}}'
    # res = model_rez('{"1":{"bedrooms":"3","bathrooms":"3","sqft_living":"1200","sqft_lot":"6000","zipcode":"98058"}}')
    res = model_rez(house)
    # print (res)
    # print (res)
    return res

def model_rez(home_data):
    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
    rel_path = 'kc.csv'
    abs_file_path = os.path.join(script_dir, rel_path)
    data = pd.read_csv(abs_file_path)
    y = data.price
    predictors = ['bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot']
    X = data[predictors]
    train_X, val_X, train_y, val_y = train_test_split(X, y, random_state=0)

    forest_model = RandomForestRegressor(random_state=100)
    forest_model.fit(train_X, train_y)
    mydata = pd.read_json(
        home_data,
        orient='index')

    test_X = mydata[predictors]
    predicted_prices = forest_model.predict(test_X)
    return predicted_prices[0]


# def model_rez(home_data):
#
#     script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
#     rel_path = "saved_model"
#     abs_file_path = os.path.join(script_dir, rel_path)
#     print(abs_file_path)
#     # with open('C:/Users/mikle/lc101/homeapp/saved_model', 'rb') as f:
#     #     rf = pickle.load(f)
#     mydata = pd.read_json(home_data, orient='index')
#     print(mydata.head())
#     predictors = ['bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot']
#     test_X = mydata[predictors]
#     global file
#     pikle_load()
#     predicted_prices = file.predict(test_X)
#     return predicted_prices

# def pikle_load():
#     global file
#     file = pickle.load(open("C:/Users/mikle/lc101/homeapp/saved_model", "rb"))