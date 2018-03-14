rom
flask_sqlalchemy
import SQLAlchemy
from flask_config import get_app
from statistics_db_model import UserEnvironment, User, Environment, CheckPoint
#from coockies_session import ChunkedSecureCookieSessionInterface
from flask import session, render_template
# from coockies_session import ChunkedSecureCookieSessionInterface
from flask import session, render_template
from flask_sqlalchemy import SQLAlchemy

from flask_config import get_app
from statistics_db_model import UserEnvironment, User, Environment, CheckPoint

app = get_app()
db = SQLAlchemy(app)
file = None
#app.session_interface = ChunkedSecureCookieSessionInterface()

class Statistics:

    @staticmethod
    def handle_page(page, user_id, current_env):
        res = None
        if user_id:

            existing_user = User.get_user_by_id(user_id)
            if existing_user:
                last_env = Environment.get_env_by_id(existing_user.last_env_id)
                if last_env.is_equal(current_env):
                    check_point = CheckPoint(existing_user.last_env_id, page)
                    check_point.add_new()
                else:
                    new_env = Environment(current_env, user_id)
                    new_env.add_new()
                    existing_user.change_last_env(new_env.id)
                    check_point = CheckPoint(existing_user.last_env_id, page)
                    check_point.add_new()
            else:
                new_user = User()
                new_user.add_new()
                new_env = Environment(current_env, new_user.id)
                new_env.add_new()
                new_user.change_last_env(new_env.id)
                check_point = CheckPoint(new_user.last_env_id, page)
                check_point.add_new()
                res = new_user.id

        else:
            new_user = User()
            new_user.add_new()
            new_env = Environment(current_env, new_user.id)
            new_env.add_new()
            new_user.change_last_env(new_env.id)
            check_point = CheckPoint(new_user.last_env_id, page)
            check_point.add_new()
            res = new_user.id
        return res

    @staticmethod
    def set_stats(page, template):
        environment = UserEnvironment()
        current_env = environment.get_current_user_environment()
        try:
            user_id = session['id']
            u = Statistics.handle_page(page, user_id, current_env)
            if u:
                session['id'] = u
        except:
            session['id'] = Statistics.handle_page(page, None, current_env)
        response = render_template(template)
        return response
