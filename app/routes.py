from flask import render_template
from app import app
from app.Classes import ComparisonForm, Risuto

@app.route('/')
@app.route('/index')
def index():
    lists1 = ['X','Y','Z']
    lists2 = ['B','C','D','E']
    form = ComparisonForm()
    form.risuto.entries[0].choices = [(u,u) for u in lists1] # Choices must be set after initiation of form
    form.risuto.entries[1].choices = [(u,u) for u in lists2] # Choices must be set after initiation of form
    return render_template('index.html',ulists=lists1,form=form)