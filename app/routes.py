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
    if 'risutos' in session:
        risutos = [Risuto.fromjson(r) for r in session['risutos']]
        lookup = {r.name: r for r in risutos}
    else:
        risutos = []
    
    output = None
    form = ComparisonForm()

    if len(risutos) > 0:
        # Choices must be set after initiation of form
        choices = [(r.name,r.name) for r in risutos]
        form.risuto1.choices = choices
        form.risuto2.choices = choices[1:] + [choices[0]]

        if form.validate_on_submit():
            a = lookup[form.risuto1.data].risutoset
            b = lookup[form.risuto2.data].risutoset
        elif len(risutos) == 1:
            a = risutos[0].risutoset
            b = risutos[0].risutoset
        elif len(risutos) > 1:
            a = risutos[0].risutoset
            b = risutos[1].risutoset

        for setop in ('left','union','inters','right'):
            # Get the results of the set operations
            res = setoperation(a,b,setop)
            # Assign result counts
            setattr(form,setop + 'cnt',len(res))
            # Checks if button corresponding to this setop was pressed:
            if form.validate_on_submit() and getattr(form,setop).data:
                output = res
    else:
        choices = [(None,'Nothing yet')]
        form.risuto1.choices = choices
        form.risuto2.choices = choices
        if form.validate_on_submit():
            output = 'Enter a list for comparison'

    # The specified delimiter will be used for the display of the output.
    if form.validate_on_submit():
        delimiter = bytes(form.delimiter.data, "utf-8").decode("unicode_escape")
    else:
        delimiter = ','

    return render_template('index.html',risutos=risutos,
                                        output=output,
                                        delimitfunc=lambda x: delimiter.join(x),
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