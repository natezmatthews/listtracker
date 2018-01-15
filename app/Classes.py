from flask_wtf import FlaskForm
from wtforms import SelectField, FieldList

class Risuto():
    def __init__(self):
        self._risutotext = None
        self._name = None
        self._description = None
        self._separators = [",","\n"] # Default separators
        self._risutoset = set()
    
    def _strvalidation(self,value,maxlen=None):
        assert isinstance(value, str), "This field must be a string."
        assert value, "This field may not be an empty string."
        if maxlen:
            assert maxlen >= len(value), "This string must be {} or fewer characters.".format(maxlen)
    
    @property
    def risutotext(self):
        return self._risutotext
    
    @risutotext.setter
    def risutotext(self,value):
        self._strvalidation(value)
        self._risutotext = value
        self._risutoset_setter()
        
    @risutotext.deleter
    def risutotext(self,value):
        del self._risutotext
        del self._risutoset

    def addseparator(self,sep):
        self._strvalidation(sep)
        self._separators.append(sep)

    def removeseparator(self,sep):
        try:
            self._separators.remove(sep)
        except:
            pass
        
    @property
    def risutoset(self):
        return self._risutoset
    
    def _risutoset_setter(self):
        newrisuto = [self._risutotext]
        for sep in self._separators:
            oldrisuto = newrisuto
            newrisuto = []
            for elem in oldrisuto:
                newrisuto.extend(elem.split(sep))
        
        # The filter gets rid of the empty strings split creates when there are two or more delimiters in a row
        self._risutoset = set(filter(None,newrisuto))
    
    @risutoset.setter
    def risutoset(self,value):
        raise AttributeError('The item set must be initiated by creating an item list.')
    
    @risutoset.deleter
    def risutoset(self):
        del self._risutoset
        del self._risutotext
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self,value):
        self._strvalidation(value,80) # DEFAULT LENGTH FOR NOW
        self._name = value
        
    @name.deleter
    def name(self,value):
        del self._name
        
    @property
    def description(self):
        return self._description
    
    @description.setter
    def description(self,value):
        self._strvalidation(value,280) # DEFAULT LENGTH FOR NOW
        self._description = value
        
    @description.deleter
    def description(self,value):
        del self._description


class ComparisonForm(FlaskForm):
    risuto1 = SelectField('List to compare')
    risuto2 = SelectField('List to compare')
    # risuto = FieldList(SelectField('List to compare'),min_entries=2,max_entries=2)
