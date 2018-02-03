from flask import Flask, render_template
from data import Results #Importing data from data.py

app = Flask(__name__)

#Store results function from data.py
Results = Results()

#For testing purposes, will be deleted later.
app.debug = True


### ====== ROUTES ====== ###

#Index Page
@app.route('/')
def index():
    return render_template('home.html')

#About Plage
@app.route('/about')
def about():
    return render_template('about.html')

#Results Page
@app.route('/results')
def results():
    return render_template('results.html', results = Results)


if __name__ == '__main__':
    app.run()