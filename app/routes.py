from flask import render_template
from app import app
from app.Classes import ComparisonForm, Risuto

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    lists1 = ['X','Y','Z']
    lists2 = ['B','C','D','E']
    form = ComparisonForm()
    form.risuto1.choices = [(u,u) for u in lists1] # Choices must be set after initiation of form
    form.risuto2.choices = [(u,u) for u in lists2] # Choices must be set after initiation of form
    if form.validate_on_submit():
        print('Valid')
        print(form.left.data)
    else:
        print('inValid')
        print(form.left.data)
    return render_template('index.html',ulists=lists1,form=form)