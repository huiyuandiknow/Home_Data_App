from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from helper import dec

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user1:' + dec(
    'Nm7CVLX6fVhlA4kS') + '@67.215.253.70:3306/user1db1'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user1db1:123456@localhost:8889/user1db1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
# For testing purposes, will be deleted later.
app.debug = True


def get_app():
    return app