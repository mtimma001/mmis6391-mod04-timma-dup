from flask import render_template
from . import app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shop')
def shop():
    return render_template('shop.html')

@app.route('/adoption')
def adoption():
    return render_template('adoption.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

