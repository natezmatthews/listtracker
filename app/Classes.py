from flask_wtf import FlaskForm
from wtforms import SelectField, FieldList, SubmitField,  StringField

class Risuto():
    def __init__(self):
        self._risutotext = None
        self._hashid = None
        self._name = None
        self._description = None
        self._separators = [",","\n"] # Default separators
        self._risutoset = set()
    
    def _strvalidation(self,value,field,maxlen=None):
        assert isinstance(value, str), "The {} must be a string.".format(field)
        assert value, "The {} may not be an empty string.".format(field)
        if maxlen:
            assert maxlen >= len(value), \
                   "The {} must be {} or fewer characters.".format(field,maxlen)
    
    @property
    def risutotext(self):
        return self._risutotext
    
    @risutotext.setter
    def risutotext(self,value):
        self._strvalidation(value,field='text')
        self._risutotext = value
        self._risutoset_setter(value)
        
    @risutotext.deleter
    def risutotext(self,value):
        del self._risutotext
        del self._risutoset

    def addseparator(self,sep):
        self._strvalidation(sep,field='separator')
        self._separators.append(sep)

    def removeseparator(self,sep):
        try:
            self._separators.remove(sep)
        except:
            pass
        
    @property
    def risutoset(self):
        return self._risutoset
    
    def _risutoset_setter(self,value):
        newrisuto = [value]
        for sep in self._separators:
            oldrisuto = newrisuto
            newrisuto = []
            for elem in oldrisuto:
                newrisuto.extend(elem.split(sep))
        
        # The filter gets rid of the empty strings split creates 
        # when there are two or more delimiters in a row
        self._risutoset = set(filter(None,newrisuto))
    
    @risutoset.setter
    def risutoset(self,value):
        raise AttributeError('The item set must' +\
                                'be initiated by creating an item list.')
    
    @risutoset.deleter
    def risutoset(self):
        del self._risutoset
        del self._risutotext
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self,value):
        self._strvalidation(value,field='name',maxlen=80) # TODO: MAXLEN
        self._name = value
        
    @name.deleter
    def name(self,value):
        del self._name
        
    @property
    def description(self):
        return self._description
    
    @description.setter
    def description(self,value):
        self._strvalidation(value,field='description',maxlen=280) # TODO: MAXLEN
        self._description = value
        
    @description.deleter
    def description(self,value):
        del self._description

    @classmethod
    def fromdict(cls,d):
        instance = cls()
        for field in ['text','name','description']:
            if field in d:
                setattr(instance,field,d[field])
        return instance

    def todict(self):
        d = {'text':self._risutotext,
             'name':self._name,
             'description':self._description
            }
        return d

class ComparisonForm(FlaskForm):
    risuto1 = SelectField('Left List')
    risuto2 = SelectField('Right List')
    left = SubmitField('Left')
    union = SubmitField('Union')
    inters = SubmitField('Intersection')
    right = SubmitField('Right')

class RisutoForm(FlaskForm):
    risuto = StringField('Input')
    submit = SubmitField('Submit')
