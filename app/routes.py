from flask import render_template
from app import app
from app.Classes import SelectForm, Risuto

@app.route('/')
@app.route('/index')
def index():
    ulists = ['X','Y','Z']
    form = SelectForm()
    form.risuto.choices = [(u,u) for u in ulists]
    return render_template('index.html',ulists=ulists,form=form)