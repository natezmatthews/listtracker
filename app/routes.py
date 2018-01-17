from flask import render_template, session, redirect, url_for
from app import app
from app.Classes import ComparisonForm, RisutoForm, Risuto

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    print(session)
    form = ComparisonForm()
    # Choices must be set after initiation of form
    if 'risutos' in session:
        risutos = [Risuto.fromdict(r) for r in session['risutos']]
        choices = [(r,r.name) for r in risutos]
    else:
        choices = [(None,'Nothing yet')]

    form.risuto1.choices = choices
    form.risuto2.choices = choices
    
    if form.validate_on_submit():
        pass
    return render_template('index.html',form=form)

@app.route('/create',methods=['GET','POST'])
def create():
    form = RisutoForm()
    print(session)
    if form.validate_on_submit():
        print(form.risuto.data)
        risuto = Risuto()
        risuto.name = 'Name: ' + form.risuto.data[:5]
        risuto.description = 'Desc: ' + form.risuto.data[:5]
        risuto.risutotext = form.risuto.data

        risutodict = risuto.todict()
        if 'risutos' in session:
            risutos = session['risutos']
            risutos.append(risutodict)
            session['risutos'] = risutos
        else:
            session['risutos'] = [risutodict]
        
        return redirect(url_for('index'))
    
    return render_template('create.html',form=form)