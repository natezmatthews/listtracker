from flask import render_template, session, redirect, url_for
from app import app
from app.Classes import ComparisonForm, RisutoForm, Risuto

#session.clear()

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = ComparisonForm()
    # Choices must be set after initiation of form
    if 'risutos' in session:
        risutos = [Risuto.fromdict(r) for r in session['risutos']]
        lookup = {r.name: r for r in risutos}
        choices = [(r.name,r.name) for r in risutos]
    else:
        form.risuto1.data = {}
        choices = [(None,'Nothing yet')]

    form.risuto1.choices = choices
    form.risuto2.choices = choices
    
    if form.left.data or form.union.data or form.inters.data or form.right.data:
        setop = setoperation(lookup[form.risuto1.data],
                             lookup[form.risuto2.data],
                             form.left.data,
                             form.union.data,
                             form.inters.data,
                             form.right.data)
        output = ','.join(list(setop))
    else:
        output = None
    return render_template('index.html',risutos=risutos,
                                        output=output,
                                        form=form)

def setoperation(risuto1,risuto2,left,union,inters,right):
    a = risuto1.risutoset
    b = risuto2.risutoset
    if left:
        return a - b
    elif union:
        return a | b
    elif inters:
        return a & b
    elif right:
        return b - a

@app.route('/create',methods=['GET','POST'])
def create():
    form = RisutoForm()
    if form.validate_on_submit():
        risuto = Risuto()
        risuto.name = 'Name: ' + form.risuto.data[:5]
        risuto.description = 'Desc: ' + form.risuto.data[:5]
        risuto.text = form.risuto.data

        risutodict = risuto.todict()
        if 'risutos' in session:
            # Appending directly didn't work; something about session?
            risutos = session['risutos']
            risutos.append(risutodict)
            session['risutos'] = risutos
        else:
            session['risutos'] = [risutodict]
        
        return redirect(url_for('index'))
    
    return render_template('create.html',form=form)