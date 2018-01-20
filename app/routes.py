from flask import render_template, session, redirect, url_for
from app import app
from app.Classes import ComparisonForm, RisutoForm, Risuto
from datetime import datetime as dt

@app.route('/clear')
def clear():
    print(session)
    session.clear()
    print(session)      
    return 'Done'

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = ComparisonForm()
    # Choices must be set after initiation of form
    if 'risutos' in session:
        risutos = [Risuto.fromjson(r) for r in session['risutos']]
        lookup = {r.name: r for r in risutos}
        choices = [(r.name,r.name) for r in risutos]
    else:
        form.risuto1.data = {}
        choices = [(None,'Nothing yet')]

    form.risuto1.choices = choices
    form.risuto2.choices = choices[1:] + [choices[0]]
    
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

    if 'risutos' in locals():
        return render_template('index.html',risutos=risutos,
                                            output=output,
                                            form=form)
    else:
        return render_template('index.html',output=output,
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
        
        # Text fields
        risuto.name = form.name.data
        risuto.text = form.text.data
        risuto.description = form.description.data
        
        # Separators
        if form.comma.data:
            risuto.addseparator(',')
        else:
            risuto.removeseparator(',')
        if form.newline.data:
            risuto.addseparator('\n')
            risuto.addseparator('\r')
        else:
            risuto.removeseparator('\n')
            risuto.removeseparator('\r')

        # Datetime
        risuto.created = dt.now()

        # Store it in session
        risutojson = risuto.tojson()
        if 'risutos' in session:
            # Appending directly didn't work; something about session?
            risutos = session['risutos']
            risutos.append(risutojson)
            session['risutos'] = risutos
        else:
            session['risutos'] = [risutojson]
        
        return redirect(url_for('index'))
    
    return render_template('create.html',form=form)