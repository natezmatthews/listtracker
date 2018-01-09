
# coding: utf-8

import re

class UniqueList():
    def __init__(self):
        self._listtext = None
        self._name = None
        self._description = None
        self._separators = [",","\n","sep"] # Default separators
        self._listset = set()
    
    def _strvalidation(self,value,maxlen=None):
        assert isinstance(value, str), "This field must be a string."
        assert value, "This field may not be an empty string."
        if maxlen:
            assert maxlen >= len(value), "This string must be {} or fewer characters.".format(maxlen)
    
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

    def addseparator(self,sep):
        self._strvalidation(sep)
        self._separators.append(sep)

    def removeseparator(self,sep):
        try:
            self._separators.remove(sep)
        except:
            pass
        
    @property
    def listset(self):
        return self._listset
    
    def _listset_setter(self):
        newlist = [self._listtext]
        for sep in self._separators:
            oldlist = newlist
            newlist = []
            for elem in oldlist:
                newlist.extend(elem.split(sep))
        
        # The filter gets rid of the empty strings split creates when there are two or more delimiters in a row
        self._listset = set(filter(None,newlist))
    
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


instance.listtext = """Asepcsep
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

