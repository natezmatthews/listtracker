from flask import render_template
from app import app
from app.Classes import SelectForm

@app.route('/')
@app.route('/index')
def index():
    ulists = ['List number one','List number 2','The third']
    return render_template('index.html',ulists=ulists,form=SelectForm())