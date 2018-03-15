from datetime import datetime

from flask import request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

from flask_config import get_app

app = get_app()
db = SQLAlchemy(app)
file = None

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    environments = relationship("Environment")
    search_results = relationship("SearchResults")
    time_of_creation = db.Column(db.String(26))
    last_env_id = db.Column(db.Integer)

    def __init__(self):
        self.time_of_creation = str(datetime.now())

    @staticmethod
    def get_user_by_id(user_id):
        aa = User.query.filter_by(id=user_id).first()

        return aa

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
    platform = db.Column(db.String(15))
    version = db.Column(db.String(15))
    ip = db.Column(db.String(15))


    def __init__(self, ue, user_id):
        self.browser = ue.browser[:15]
        self.platform = ue.platform[:15]
        self.version = ue.version[:15]
        self.ip = ue.ip[:15]
        self.time_of_creation = str(datetime.now())
        self.user_id = user_id

    def is_equal(self, usr_env):

        return self.browser == usr_env.browser[:15] and self.platform == usr_env.platform[:15] \
               and self.ip == usr_env.ip[:15] and self.version == usr_env.version[:15]

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
    page = db.Column(db.String(2))

    def __init__(self, env_id, page):
        self.time = str(datetime.now())
        self.env_id = env_id
        self.page = page
    def add_new(self):
        db.session.add(self)
        db.session.commit()


class SearchResults(db.Model):
    __tablename__ = 'search_results'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = Column(db.Integer, ForeignKey('user.id'))
    address = db.Column(db.String(125))
    time_of_creation = db.Column(db.String(26))
    value = db.Column(db.String(15))

    def __init__(self, adr, user_id, val):
        self.address = adr[:125]
        self.value = str(val[:15])
        self.time_of_creation = str(datetime.now())
        self.user_id = user_id

    def add_new(self):
        db.session.add(self)
        db.session.commit()


class UserEnvironment:
    browser = ""
    language = ""
    platform = ""
    user_agent_string = ""
    version = ""
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
        self.ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        return self

class StatisticsTables:
    @staticmethod
    def get_hits_uniq_users():
        q = db.engine.execute("SELECT page, count(DISTINCT env_id) FROM `check_point` WHERE 1 GROUP BY page")
        result = []
        for row in q:
            result.append(row)
        return result
    @staticmethod
    def get_hits_users():
        q = db.engine.execute("SELECT page, count(DISTINCT env_id), count(env_id) FROM `check_point` WHERE 1 GROUP BY page ORDER BY count(DISTINCT env_id) DESC;")
        result = []
        for row in q:
            result.append(row)
        return result
    @staticmethod
    def get_searches():
        q = db.engine.execute("SELECT address, count(DISTINCT user_id), AVG(value) FROM `search_results` WHERE 1 GROUP BY address ORDER BY count(DISTINCT user_id) DESC;")
        result = []
        for row in q:
            result.append(row)
        return result




