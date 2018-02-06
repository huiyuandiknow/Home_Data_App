from flask import Flask, render_template, request
from data import Results #Importing data from data.py

app = Flask(__name__)

#Store results function from data.py
Results = Results()

#For testing purposes, will be deleted later.
app.debug = True

address = ""
# ====== ROUTES ====== ###

# Index Page
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/', methods=['POST'])
def form_index():
    global address
    address = request.form['address']
    return render_template('results.html', res=address)


# # Results Page
# @app.route('/results')
# def results():
#
#     return render_template('results.html', res=address)

# About Page
@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run()