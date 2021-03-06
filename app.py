import os

import jinja2
from flask import render_template, request, redirect, url_for, session

from cookies_session import SecureCookieSessionInterface
from data_handling import Results
from flask_config import get_app
from statistics import Statistics

#import sys #debug



template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)


app = get_app()
file = None
app.session_interface = SecureCookieSessionInterface()

# ====== ROUTES ====== ###
@app.before_request
def make_session_permanent():
    session.permanent = True

# Index Page
@app.route('/')
def index():
    # return Statistics.set_stats('hp', 'home.html', None, None)
    Statistics.set_stats('hp', 'home.html', None, None)
    return render_template('home.html')


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
    Statistics.set_stats('rt', 'results.html', address, str(data.val))
    response = render_template('results.html', res=data.val, beds=data.beds,
                           baths=data.baths, source=source, address=address, lot=data.lot,
                           liv=data.living, zipcode=data.home_zip, year=data.year, zil=zil, zil_home=zil_home)

    return response



# About Page
@app.route('/about')
def about():
    # return Statistics.set_stats('ab', 'about.html', None, None)
    Statistics.set_stats('ab', 'about.html', None, None)
    #Statistics.get_stats()
    return render_template('about.html')
# Stats Page

@app.route('/stats')
def stats():
    Statistics.set_stats('st', 'stats.html', None, None)
    res = Statistics.get_stats()
    template = jinja_env.get_template('stats.html')
    return template.render(list1=res[0], list2=res[1])


if __name__ == '__main__':
    app.run()