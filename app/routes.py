from flask import render_template, session, redirect, url_for
from app import app
from app.Classes import ComparisonForm, RisutoForm, Risuto
import sqlite3

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if 'risutos' in session:
        risutos = [x.risutotext for x in session['risutos']]
    else:
        risutos = ['Nothing yet']
    lists1 = ['X','Y','Z']
    lists2 = ['B','C','D','E']
    form = ComparisonForm()
    form.risuto1.choices = [(u,u) for u in lists1] # Choices must be set after initiation of form
    form.risuto2.choices = [(u,u) for u in lists2] # Choices must be set after initiation of form
    if form.validate_on_submit():
        pass
    return render_template('index.html',risutos=risutos,form=form)

@app.route('/create',methods=['GET','POST'])
def create():
    form = RisutoForm()
    if form.validate_on_submit():
        risuto = Risuto()
        risuto.name = 'Name' + form.risuto.data[:5]
        risuto.description = 'Desc' + form.risuto.data[:5]
        risuto.risutotext = form.risuto.data
        if 'risutos' in session:
            session['risutos'].append(risuto)
        else:
            session['risutos'] = [risuto]
        return redirect(url_for('index'))
    return render_template('create.html',form=form)