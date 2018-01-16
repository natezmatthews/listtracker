from flask import render_template, session, redirect, url_for
from app import app
from app.Classes import ComparisonForm, RisutoForm, Risuto

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    try:
        text = session['text']
    except:
        text = 'Default'
    lists1 = ['X','Y','Z']
    lists2 = ['B','C','D','E']
    form = ComparisonForm()
    form.risuto1.choices = [(u,u) for u in lists1] # Choices must be set after initiation of form
    form.risuto2.choices = [(u,u) for u in lists2] # Choices must be set after initiation of form
    if form.validate_on_submit():
        pass
    return render_template('index.html',text=text,form=form)

@app.route('/create',methods=['GET','POST'])
def create():
    form = RisutoForm()
    if form.validate_on_submit():
        print('Valid')
        print(form.risuto.data)
        session['text'] = form.risuto.data
        return redirect(url_for('index'))
    else:
        print ('inValid')
        print(form.risuto.data)
    return render_template('create.html',form=form)