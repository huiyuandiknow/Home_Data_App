rom
flask_sqlalchemy
import SQLAlchemy
from flask_config import get_app
from statistics_db_model import UserEnvironment, User, Environment, CheckPoint, SearchResults
#from coockies_session import ChunkedSecureCookieSessionInterface
from flask import session
# from coockies_session import ChunkedSecureCookieSessionInterface
from flask import session
from flask_sqlalchemy import SQLAlchemy

from flask_config import get_app
from statistics_db_model import UserEnvironment, User, Environment, CheckPoint, SearchResults

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
    def handle_res_page(user_id, current_env, addr, val):
        res = None
        ui = user_id
        existing_user = None
        if user_id:

            existing_user = User.get_user_by_id(ui)
            if existing_user:
                last_env = Environment.get_env_by_id(existing_user.last_env_id)
                if last_env.is_equal(current_env):
                    check_point = CheckPoint(existing_user.last_env_id, 'rt')
                    check_point.add_new()

                else:
                    new_env = Environment(current_env, ui)
                    new_env.add_new()
                    existing_user.change_last_env(new_env.id)
                    check_point = CheckPoint(existing_user.last_env_id, 'rt')
                    check_point.add_new()
            else:
                existing_user = User()
                existing_user.add_new()
                new_env = Environment(current_env, existing_user.id)
                new_env.add_new()
                existing_user.change_last_env(new_env.id)
                check_point = CheckPoint(existing_user.last_env_id, 'rt')
                check_point.add_new()
                res = existing_user.id

        else:
            existing_user = User()
            existing_user.add_new()
            new_env = Environment(current_env, existing_user.id)
            new_env.add_new()
            existing_user.change_last_env(new_env.id)
            check_point = CheckPoint(existing_user.last_env_id, 'rt')
            check_point.add_new()
            res = existing_user.id

        search_results = SearchResults(addr, existing_user.id, val)
        search_results.add_new()
        return res

    @staticmethod
    def set_stats(page, template, adr, val):
        environment = UserEnvironment()
        current_env = environment.get_current_user_environment()
        try:
            user_id = session['id']
            if val is None:
                u = Statistics.handle_page(page, user_id, current_env)
                if u:
                    session['id'] = u
            else:
                u = Statistics.handle_res_page(user_id, current_env, adr, val)
                if u:
                    session['id'] = u
        except:
            if val is None:
                session['id'] = Statistics.handle_page(page, None, current_env)
            else:
                session['id'] = Statistics.handle_res_page(None, current_env, adr, val)
                # response = render_template(template)
                # return response
