from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from flask_config import get_app
from statistics_db_model import UserEnvironment, User, Environment, CheckPoint
from flask import session

#Base = declarative_base()



app = get_app()
db = SQLAlchemy(app)
file = None

class Statistics:
    @staticmethod
    def handle_homepage():

        environment = UserEnvironment()
        current_env = environment.get_current_user_environment()

        try:
            user_id = session['id']
            existing_user = User.get_user_by_id(user_id)
            if existing_user:
                last_env = Environment.get_env_by_id(existing_user.last_env_id)
                if last_env.is_equal(current_env):
                    check_point = CheckPoint(existing_user.last_env_id)
                    check_point.add_new()
                else:
                    new_env = Environment(current_env, user_id)
                    new_env.add_new()
                    existing_user.change_last_env(new_env.id)
                    check_point = CheckPoint(existing_user.last_env_id)
                    check_point.add_new()
        except:
            new_user = User()
            new_user.add_new()
            new_env = Environment(current_env, new_user.id)
            new_env.add_new()
            new_user.change_last_env(new_env.id)
            session['id'] = new_user.id
            check_point = CheckPoint(new_user.last_env_id)
            check_point.add_new()