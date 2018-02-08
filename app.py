from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from data import Results #Importing the results function from data.py

app = Flask(__name__)

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
def results():
    address = request.form['address']
    h_type = request.form['type']
    beds = request.form['beds']
    baths = request.form['baths']
    return render_template('results.html', res=Results(address, h_type, beds, baths))


# About Page
@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run()