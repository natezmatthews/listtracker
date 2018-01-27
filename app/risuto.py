from datetime import datetime as dt
from dateutil.parser import parse

class Risuto():
    def __init__(self, d=None):
        if d:
            self.name = d['name']
            self.description = d['description']
            self._separators = d['separators']
            self.created = parse(d['created'])
            self.text = d['text']
        else:
            self._name = None
            self._description = None
            self._separators = []
            self._created = None
            self._text = None
            self._risutoset = set()
    
    def _strvalidation(self, value, fieldname, maxlen=None):
        if not isinstance(value, str):
            raise TypeError("The {} must be a string.".format(fieldname))
        if maxlen and maxlen < len(value):
            raise ValueError("The {} must be ".format(fieldname) + \
                             "{} or fewer characters.".format(maxlen))
    
    ############################################################################
    # "Text", The original text of the list
    @property
    def text(self):
        return self._text
    
    @text.setter
    def text(self, value):
        self._strvalidation(value, fieldname='text')
        self._text = value
        self._risutoset_setter(value)
        
    @text.deleter
    def text(self, value):
        del self._text
        del self._risutoset

    ############################################################################
    # "Separators", what parts of the input text should be considered separators
    def add_separator(self, sep):
        self._strvalidation(sep, fieldname='separator')
        self._separators.append(sep)

    def remove_separator(self, sep):
        try:
            self._separators.remove(sep)
        except:
            pass
        
    ############################################################################
    # "Risuto Set", the uinque elements of the input list
    @property
    def risutoset(self):
        return self._risutoset
    
    def _risutoset_setter(self, value):
        newrisuto = [value]
        for sep in self._separators:
            oldrisuto = newrisuto
            newrisuto = []
            for elem in oldrisuto:
                newrisuto.extend(elem.split(sep))
        
        # The filter gets rid of the empty strings split creates 
        # when there are two or more delimiters in a row
        self._risutoset = set(filter(None, newrisuto))
    
    @risutoset.setter
    def risutoset(self, value):
        raise AttributeError('The item set must ' +\
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
    def name(self, value):
        self._strvalidation(value, fieldname='name', maxlen=80)
        self._name = value
        
    @name.deleter
    def name(self, value):
        del self._name
        
    ############################################################################
    # "Description", A longer description given to the list
    @property
    def description(self):
        return self._description
    
    @description.setter
    def description(self, value):
        self._strvalidation(value, fieldname='description', maxlen=280)
        self._description = value
        
    @description.deleter
    def description(self, value):
        del self._description

    ############################################################################
    # "Created", The date and time when the list was created
    @property
    def created(self):
        return self._created
    
    @created.setter
    def created(self, value):
        if isinstance(value, dt):
            self._created = value
        else:
            raise TypeError("The 'created' property must be a datetime object")
        
    @created.deleter
    def created(self, value):
        del self._created

    ############################################################################
    # JSON compatibility for the session
    def to_json(self):
        return {'text':self._text,
                 'name':self._name,
                 'description':self._description,
                 'separators':self._separators,
                 'created':self._created.isoformat()
                }
