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
    if 'risutos' in session:
        risutos = [Risuto.fromjson(r) for r in session['risutos']]
        lookup = {r.name: r for r in risutos}
        choices = [(r.name,r.name) for r in risutos]
    else:
        form.risuto1.data = {}
        choices = [(None,'Nothing yet')]

    # Choices must be set after initiation of form
    form.risuto1.choices = choices
    form.risuto2.choices = choices[1:] + [choices[0]]
    a = risutos[0].risutoset
    b = risutos[1].risutoset
    delimiter = ','
    output = None
    
    if form.validate_on_submit():
        a = lookup[form.risuto1.data].risutoset
        b = lookup[form.risuto2.data].risutoset
        delimiter = bytes(form.delimiter.data, "utf-8").decode("unicode_escape")
    
    for setop in ('left','union','inters','right'):
        # Get the results of the set operations
        res = setoperation(a,b,setop)
        # Create output to show
        if form.validate_on_submit() \
            and getattr(form,setop).data: # True if this button was just pressed
            # The split here is a workaround since HTML doesn't understand \n
            output = delimiter.join(res).split('\n')
        # Assign result counts
        setattr(form,setop + 'cnt',len(res))

    if 'risutos' in locals():
        return render_template('index.html',risutos=risutos,
                                            output=output,
                                            form=form)
    else:
        return render_template('index.html',output=output,
                                            form=form)

def setoperation(a,b,setop):
    if setop == 'left':
        return a - b
    elif setop == 'union':
        return a | b
    elif setop == 'inters':
        return a & b
    elif setop == 'right':
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