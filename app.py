from flask import Flask, render_template, request
from data import Results #Importing data from data.py

app = Flask(__name__)

#For testing purposes, will be deleted later.
app.debug = True

# ====== ROUTES ====== ###


# Index Page
@app.route('/')
def index():
    return render_template('home.html')


# Results Page
@app.route('/results', methods=['GET', 'POST'])
def results():
    address = request.form['address']
    h_type = request.form['type']
    beds = request.form['beds']
    baths = request.form['baths']
    res = Results(address, h_type, beds, baths)
    return render_template('results.html', res=res)


# About Page
@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run()