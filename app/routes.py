from flask import render_template, session, redirect, url_for
from app import app, db
from app.models import Risuto, Separator, Item
from app.lista import Lista
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

def set_operation(a, b, setop):
    if setop == 'left':
        return set(a) - set(b)
    elif setop == 'union':
        return set(a) | set(b)
    elif setop == 'inters':
        return set(a) & set(b)
    elif setop == 'right':
        return set(b) - set(a)

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
    risuto_items = lambda x: [i.item for i in Item.query.filter_by(risuto=x).all()]
    if submitted_yn:
        a = risuto_items(Risuto.query.filter_by(nacme=submited_name1))
        b = risuto_items(Risuto.query.filter_by(name=submitted_name2))
    elif len(risutos) == 1:
        a = risuto_items(risutos[0])
        b = risuto_items(risutos[0])
    elif len(risutos) > 1:
        a = risuto_items(risutos[0])
        b = risuto_items(risutos[1])
    return (a, b)

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    risutos = Risuto.query.all()
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
            res = set_operation(a, b, setop)
            # Assign result counts
            setattr(form, setop + 'cnt', len(res))
            # Checks if button corresponding to this setop was pressed:
            if not form.validate_on_submit() and getattr(form, setop).data:
                output = res
            else:
    else:
        if form.validate_on_submit():
            output = 'Enter a list for comparison'

    return render_template('index.html',
                            risutos=risutos,
                            output=output,
                            delimitfunc=lambda x: delimiter.join(x),
                            form=form)

def extract_items(text,separators):
    newlista = [text]
    for sep in separators:
        oldlista = newlista
        newlista = []
        for elem in oldlista:
            newlista.extend(elem.split(sep))
    
    # The filter gets rid of the empty strings split creates 
    # when there are two or more delimiters in a row
    return set(filter(None, newlista))

@app.route('/create',methods=['GET', 'POST'])
def create():
    form = RisutoForm()
    if form.validate_on_submit():
        risuto = Risuto(name=form.name.data,
                        description=form.description.data)
        separators = []
        # Separators
        if form.comma.data:
            separators.append(',')
        if form.newline.data:
            separators.append('\n')
            separators.append('\r')

        db.session.add(risuto)
        for s in separators:
            db.session.add(Separator(separator=s,risuto=risuto))
        for item in extract_items(form.text.data,separators):
            db.session.add(Item(item=item,risuto=risuto))
        db.session.commit()

        return redirect(url_for('index'))
    
    return render_template('create.html', form=form)
