from flask import render_template, request

from data_handling import Results
from flask_config import get_app

app = get_app()
# ====== ROUTES ====== ###


# Index Page
@app.route('/')
def index():
    return render_template('home.html')


# Results Page
# It requests a data from the form on the home page and renders a results page
@app.route('/results', methods=['GET', 'POST'])
def show_results():
    zil = ""
    zil_home = ""
    address = request.form['address']
    #address = '8105 SE Henderson St Portland, OR 97206'
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
    return render_template('results.html', res=data.val, beds=data.beds,
                           baths=data.baths, source=source, address=address, lot=data.lot,
                           liv=data.living, zipcode=data.home_zip, year=data.year, zil=zil, zil_home=zil_home)


# About Page
@app.route('/about')
def about():
    return render_template('about.html')

# @app.route('/test')
# def test():
#
#     return render_template('home_test.html')
#
# @app.route('/test_results', methods=['GET', 'POST'])
# def test_res():
#     #address = '1309 Harrington Ave SE, Renton, WA 98058'
#     addr = request.form['address']
#     res = ''
#     #for key, val in addr[0].items():
#     #    if key == "ZipCode":
#     #        res = val
#
#     #return render_template('test_results.html', res=res)
#     return render_template('test_results.html', res=zillow_api(addr))

if __name__ == '__main__':
    app.run()