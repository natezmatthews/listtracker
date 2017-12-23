
# coding: utf-8

import re

class UniqueList():
    def __init__(self):
        self._listtext = None
        self._name = None
        self._description = None
        self._separators = (("Commas",",",True),
                            ("Newlines","\n",True),
                            ("Semicolons",";",False))
        self._listset = set()
    
    def _strvalidation(self,value,maxlen=None):
        assert isinstance(value, str), "This field must be a string."
        assert value, "This field may not be an empty string."
        if maxlen:
            assert maxlen >= len(value), "This string is too long."
    
    @property
    def listtext(self):
        return self._listtext
    
    @listtext.setter
    def listtext(self,value):
        self._strvalidation(value)
        self._listtext = value
        self._listset_setter()
        
    @listtext.deleter
    def listtext(self,value):
        del self._listtext
        del self._listset
        
    @property
    def listset(self):
        return self._listset
    
    def _listset_setter(self):
        chars = ''
        for desc,char,yn in self._separators:
            if yn:
                chars += char
        self._listset = set(re.split('[{}]+'.format(chars),self._listtext))
    
    @listset.setter
    def listset(self,value):
        raise AttributeError('The item set must be initiated by creating an item list.')
    
    @listset.deleter
    def listset(self):
        del self._listset
        del self._listlist
    
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


instance = UniqueList()


instance.listtext = """A
bz,
DDD"""
instance.name = 'This is the most important list of alllll'

#### No errors ####
print(instance.listset)
print(instance.description)
print(instance.name)

#### Errors ###
# instance.listset = 'A,B,C'
# instance.name = 'x' * 91
# instance.description = 12
# instance.description = ''

