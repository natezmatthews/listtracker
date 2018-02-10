from flask import render_template, session, redirect, url_for
from app import app, db
from app.risuto import Risuto
from app.forms import ComparisonForm, RisutoForm
from datetime import datetime as dt

@app.route('/clear')
def clear():
    print(session)
    session.clear()
    print(session)      
    return 'Done'

def load_risutos():
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

def get_choices(risutos):
    if len(risutos) > 1:
        return [(r.name, r.name) for r in risutos]
    else:
        return [(None, 'Nothing yet')]

def get_delimiter(submitted_yn,submission):
    # The specified delimiter will be used for the display of the output.
    if submitted_yn:
        return bytes(submission, "utf-8").decode("unicode_escape")
    else:
        return ','

def get_sets_for_operation(submitted_yn, risutos,
                           submitted_name1, submitted_name2):
    lookup = {r.name: r for r in risutos}
    if submitted_yn:
        a = lookup[submitted_name1].risutoset
        b = lookup[submitted_name2].risutoset
    elif len(risutos) == 1:
        a = risutos[0].risutoset
        b = risutos[0].risutoset
    elif len(risutos) > 1:
        a = risutos[0].risutoset
        b = risutos[1].risutoset
    
    return (a, b)

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    risutos = load_risutos()
    form = ComparisonForm()
    output = None

    choices = get_choices(risutos)
    form.dropdown1.choices = choices
    form.dropdown2.choices = choices[1:] + [choices[0]]

    delimiter = get_delimiter(form.validate_on_submit(),form.delimiter.data)

    if len(risutos) > 0:
        
        a, b = get_sets_for_operation(form.validate_on_submit(), risutos,
                                      form.dropdown1.data, form.dropdown2.data)
        
        for setop in ('left', 'union', 'inters', 'right'):
            # Get the results of the set operations
            res = setoperation(a, b, setop)
            # Assign result counts
            setattr(form, setop + 'cnt', len(res))
            # Checks if button corresponding to this setop was pressed:
            if form.validate_on_submit() and getattr(form, setop).data:
                output = res
    else:
        if form.validate_on_submit():
            output = 'Enter a list for comparison'

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
