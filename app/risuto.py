from datetime import datetime as dt
from dateutil.parser import parse

def showme(x,indent=''):
    try:
        print('{}Type: {}'.format(indent,str(type(x))))
    except:
        print('{}Type unknown'.format(indent))
    try:
        if isinstance(x,str):
            raise TypeError # Skip to the except
        for y in x:
            showme(y,indent + ' ')
    except: # Not iterable
        try:
            print('{}Thing: {}'.format(indent,str(x)))
        except:
            print('{}Thing unknown'.format(indent))

class Risuto():
    def __init__(self):
        self._text = None
        self._name = None
        self._description = None
        self._separators = []
        self._created = None
        self._risutoset = set()
    
    def _strvalidation(self,value,field,maxlen=None):
        assert isinstance(value, str), "The {} must be a string.".format(field)
        assert value, "The {} may not be an empty string.".format(field)
        if maxlen:
            assert maxlen >= len(value), \
                   "The {} must be {} or fewer characters.".format(field,maxlen)
    
    ############################################################################
    # "Text", The original text of the list
    @property
    def text(self):
        return self._text
    
    @text.setter
    def text(self,value):
        self._strvalidation(value,field='text')
        self._text = value
        self._risutoset_setter(value)
        
    @text.deleter
    def text(self,value):
        del self._text
        del self._risutoset

    ############################################################################
    # "Separators", what parts of the input text should be considered separators
    def add_separator(self,sep):
        self._strvalidation(sep,field='separator')
        self._separators.append(sep)

    def remove_separator(self,sep):
        try:
            self._separators.remove(sep)
        except:
            pass
        
    ############################################################################
    # "Risuto Set", the uinque elements of the input list
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
        del self._text
    
    ############################################################################
    # "Name", A short name given to the list
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
        
    ############################################################################
    # "Description", A longer description given to the list
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

    ############################################################################
    # "Created", The date and time when the list was created
    @property
    def created(self):
        return self._created
    
    @created.setter
    def created(self,value):
        assert isinstance(value, dt), "The created property must be a" +\
                                      " datetime object"
        self._created = value
        
    @created.deleter
    def created(self,value):
        del self._created

    ############################################################################
    # JSON compatibility for the session
    @classmethod
    def fromjson(cls,d):
        instance = cls()
        instance.name = d['name']
        instance.description = d['description']
        instance.created = parse(d['created'])
        instance._separators = d['separators']
        instance.text = d['text']
        return instance

    def tojson(self):
        d = {'text':self._text,
             'name':self._name,
             'description':self._description,
             'separators':self._separators,
             'created':self._created.isoformat()
            }
        return d
