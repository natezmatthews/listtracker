from flask import render_template, session, redirect, url_for
from app import app
from app.risuto import Risuto
from app.forms import ComparisonForm, RisutoForm
from datetime import datetime as dt

def loadrisutos():
    if 'risutos' in session:
        return [Risuto(r) for r in session['risutos']]
    else:
        return []

def setoperation(a, b, setop):
    if setop == 'left':
        return a - b
    elif setop == 'union':
        return a | b
    elif setop == 'inters':
        return a & b
    elif setop == 'right':
        return b - a

@app.route('/clear')
def clear():
    print(session)
    session.clear()
    print(session)      
    return 'Done'

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    risutos = loadrisutos()
    lookup = {r.name: r for r in risutos}
    output = None
    form = ComparisonForm()

    if len(risutos) > 0:
        # Choices must be set after initiation of form
        choices = [(r.name, r.name) for r in risutos]
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

        for setop in ('left', 'union', 'inters', 'right'):
            # Get the results of the set operations
            res = setoperation(a, b, setop)
            # Assign result counts
            setattr(form, setop + 'cnt', len(res))
            # Checks if button corresponding to this setop was pressed:
            if form.validate_on_submit() and getattr(form, setop).data:
                output = res
    else:
        choices = [(None, 'Nothing yet')]
        form.risuto1.choices = choices
        form.risuto2.choices = choices
        if form.validate_on_submit():
            output = 'Enter a list for comparison'

    # The specified delimiter will be used for the display of the output.
    if form.validate_on_submit():
        delimiter = bytes(form.delimiter.data, "utf-8").decode("unicode_escape")
    else:
        delimiter = ','

    return render_template('index.html',
                            risutos=risutos,
                            output=output,
                            delimitfunc=lambda x: delimiter.join(x),
                            form=form)

@app.route('/create',methods=['GET', 'POST'])
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
            risuto.add_separator(',')
        else:
            risuto.remove_separator(',')
        if form.newline.data:
            risuto.add_separator('\n')
            risuto.add_separator('\r')
        else:
            risuto.remove_separator('\n')
            risuto.remove_separator('\r')

        # Datetime
        risuto.created = dt.now()

        # Store it in session
        risutojson = risuto.to_json()
        if 'risutos' in session:
            # Appending directly didn't work; something about session?
            risutos = session['risutos']
            risutos.append(risutojson)
            session['risutos'] = risutos
        else:
            session['risutos'] = [risutojson]
        
        return redirect(url_for('index'))
    
    return render_template('create.html', form=form)
