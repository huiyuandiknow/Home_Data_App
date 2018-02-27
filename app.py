from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from data import results #Importing the results function from data.py
from test import zillow_api
import usaddress
import zillow


app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user2db2:123456@67.215.253.70:3306/user2db2'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user1db1:123456@67.215.253.70:3306/user1db1'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user1db1:123456@localhost:8889/user1db1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
#For testing purposes, will be deleted later.
app.debug = True

# ====== ROUTES ====== ###


# Index Page
@app.route('/')
def index():
    return render_template('home.html')


# Results Page
# It requests a data from the form on the home page and renders a results page
# If user inputted any existing address(in our fake data), it displays a value from our fake data,
# Else --> a concatenated inputted data will display
@app.route('/results', methods=['GET', 'POST'])
def show_results():
    address = request.form['address']
    #address = '8105 SE Henderson St Portland, OR 97206'
    beds = request.form['beds'].replace('Bed: ', '')
    baths = request.form['baths'].replace('Bath: ', '')
    living = request.form['living']
    lot = request.form['lot']
    year = request.form['year']
    data = results(address, living, beds, baths, lot, year)
    if not isinstance(data, str):
        if data['model'] != '':
            return render_template('results.html', res=data['model']['val'], beds=data['model']['beds'],
                    baths=data['model']['baths'], source='model', address=address, lot=data['model']['lt'],
                    liv=data['model']['liv'], zipcode=data['model']['zipcode'], year=1959)
        elif not isinstance(data['zillow'], str):
            zil = data['zillow']['principal']
            res = zil.zestimate.amount
            source = 'zillow'
            beds = zil.extended_data.bedrooms
            lot = zil.extended_data.lot_size_sqft
            liv = zil.extended_data.finished_sqft
            year = zil.extended_data.year_built
            zipcode = zil.full_address.zipcode
            return render_template('results.html', res=res, beds=beds, baths=baths, source=source, address=address,
               lot=lot, liv=liv, zipcode=zipcode, year=year)
    return render_template('results.html', res='entered wrong data', beds=beds, baths=baths, source="None", address=address)


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