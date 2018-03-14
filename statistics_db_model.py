from flask import request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from flask import session
Base = declarative_base()

from flask_config import get_app

app = get_app()
db = SQLAlchemy(app)
file = None

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    environments = relationship("Environment")
    time_of_creation = db.Column(db.String(26))
    last_env_id = db.Column(db.Integer)

    def __init__(self):
        self.time_of_creation = str(datetime.now())

    @staticmethod
    def get_user_by_id(user_id):
        return User.query.filter_by(id=user_id).first()

    def add_new(self):
        db.session.add(self)
        db.session.commit()

    def change_last_env(self, env_id):
        self.last_env_id = env_id
        db.session.commit()


class Environment(db.Model):
    __tablename__ = 'environment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = Column(db.Integer, ForeignKey('user.id'))
    browser = db.Column(db.String(15))
    check_points = relationship("CheckPoint")
    time_of_creation = db.Column(db.String(26))


    def __init__(self, ue, user_id):
        self.browser = ue.browser[:15]
        self.time_of_creation = str(datetime.now())
        self.user_id = user_id

    def is_equal(self, usr_env):
        return self.browser == usr_env.browser and True

    @staticmethod
    def get_env_by_id(env_id):
        return Environment.query.filter_by(id=env_id).first()

    def add_new(self):
        db.session.add(self)
        db.session.commit()


class CheckPoint(db.Model):
    __tablename__ = 'check_point'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    env_id = Column(db.Integer, ForeignKey('environment.id'))
    time = db.Column(db.String(26))

    def __init__(self, env_id):
        self.time = str(datetime.now())
        self.env_id = env_id
    def add_new(self):
        db.session.add(self)
        db.session.commit()

class UserEnvironment:
    browser = ""
    language = ""
    platform = ""
    user_agent_string = ""
    version = ""
    #time =""
    ip=""

    def __init__(self):
        self.ip = ""

    def get_current_user_environment(self):
        u_a = request.user_agent
        self.browser = u_a.browser
        self.language = u_a.language
        self.platform = u_a.platform
        self.user_agent_string = u_a.string
        self.version = u_a.version
        #self.time = str(datetime.now())
        self.ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        return self


# class UserSession:
#     session = ""
#     def __init__(self, sess):
#         self.session = sess
#         self.register_time = str(datetime.now())
#
#
# # class User:  #probably user session
# #     id =""
# #     register_time = ""
# #
# #     def __init__(self):
# #         self.register_time = str(datetime.now())
#
#
# class HomepageLoad:
#     load_time = ""
#
#     def __init__(self):
#         self.load_time = str(datetime.now())
#
#
# class ResultsPageLoad:
#     load_time = ""
#
#     def __init__(self):
#         self.load_time = str(datetime.now())
#
#
# class UserSearch:
#     load_time = ""
#
#     def __init__(self, address, living, beds, baths, lot, year, data, val, source):
#         self.load_time = str(datetime.now())
#         self.address = address
#         self.living = living
#         self.beds = beds
#         self.baths = baths
#         self.lot = lot
#         self.year = year
#         self.load_time = str(datetime.now())







