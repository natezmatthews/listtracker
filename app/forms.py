from flask_wtf import FlaskForm
from wtforms import SelectField,  \
                    FieldList,  \
                    SubmitField,  \
                    TextAreaField, \
                    StringField, \
                    BooleanField

class ComparisonForm(FlaskForm):
    dropdown1 = SelectField('Left List')
    dropdown2 = SelectField('Right List')
    
    left = SubmitField('Left')
    leftcnt = 0
    union = SubmitField('Union')
    unioncnt = 0
    inters = SubmitField('Intersection')
    interscnt = 0
    right = SubmitField('Right')
    rightcnt = 0

    delimiter = StringField('Delimiter for output: ',default=',')

class RisutoForm(FlaskForm):
    name = StringField('Name')
    text = TextAreaField('List')
    description = TextAreaField('Description')
    comma = BooleanField('Comma', default='true')
    newline = BooleanField('New Line', default='true')
    submit = SubmitField('Submit')
