from flask import render_template, request, redirect, url_for, session
from data_handling import Results
from flask_config import get_app
from cookies_session import ChunkedSecureCookieSessionInterface
from statistics_db_model import UserEnvironment, User, Environment, CheckPoint
from statistics import Statistics

app = get_app()
file = None
app.session_interface = ChunkedSecureCookieSessionInterface()

# ====== ROUTES ====== ###
@app.before_request
def make_session_permanent():
    session.permanent = True

# Index Page
@app.route('/')
def index():

    #make_session_permanent()
    #Statistics.handle_homepage('hp')
    environment = UserEnvironment()
    current_env = environment.get_current_user_environment()

    try:
        user_id = session['id']
        u = Statistics.handle_page('hp', user_id, current_env)
        if u:
            session['id'] = u
        #     session['id'] = 44

        # user_id = session['id']
        # print(user_id)
        # user_id =user_id + 1
        # session['id'] = user_id
    except:
        #Statistics.handle_page('hp', None, current_env)
        session['id'] = Statistics.handle_page('hp', None, current_env)
        #print(current_env.version)
        #session['id'] = 95555899878

    # try:
    #     user_id = session['id']
    #     existing_user = User.get_user_by_id(user_id)
    #     if existing_user:
    #         last_env = Environment.get_env_by_id(existing_user.last_env_id)
    #         if last_env.is_equal(current_env):
    #             check_point = CheckPoint(existing_user.last_env_id, "hp")
    #             check_point.add_new()
    #         else:
    #             new_env = Environment(current_env, user_id)
    #             new_env.add_new()
    #             existing_user.change_last_env(new_env.id)
    #             check_point = CheckPoint(existing_user.last_env_id, "hp")
    #             check_point.add_new()
    # except:
    #     new_user = User()
    #     new_user.add_new()
    #     new_env = Environment(current_env, new_user.id)
    #     new_env.add_new()
    #     new_user.change_last_env(new_env.id)
    #     session['id'] = new_user.id
    #     check_point = CheckPoint(new_user.last_env_id, "hp")
    #     check_point.add_new()


    response = render_template('home.html')
    return response


# Results Page
# It requests a data from the form on the home page and renders a results page
@app.route('/results', methods=['GET', 'POST'])
def show_results():

    zil = ""
    zil_home = ""
    try:
        address = request.form['address']
    except:
        return redirect(url_for('index'))
    # address = ''
    beds = request.form['beds'].replace('Bed: ', '')
    baths = request.form['baths'].replace('Bath: ', '')
    living = request.form['living']
    lot = request.form['lot']
    year = request.form['year']
    if len(address) > 512:
        address = 'wrong data'
    data = Results(address, living, beds, baths, lot, year)
    data.get_result()
    source = 'zillow'
    if data.has_model_data:
        source = 'model'
    if data.has_zillow:
        zil_home = data.zillow
        zil = data.comps
    else:
        zil_home = None
        zil = None
    response = render_template('results.html', res=data.val, beds=data.beds,
                           baths=data.baths, source=source, address=address, lot=data.lot,
                           liv=data.living, zipcode=data.home_zip, year=data.year, zil=zil, zil_home=zil_home)

    return response



# About Page
@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run()