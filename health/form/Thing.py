'''
Created on Jun 3, 2011

@author: song10
'''

class Thing (object):
    pass

#    def __unicode__ (self):
#        return "%s(%r)"%(self.__class__, self.__dict__)

#    def __repr__ (self):
#        if hasattr(self, 'name'):
#            return "%s %s"%(self.__class__, self.name or "''")
#        return "%s"%(self.__class__)

    #required iterate-able elements
    def __iter__ (self):
        return self.__dict__.__iter__()
    
    def __len__ (self):
        return len(self.__dict__)
    
    def __contains__ (self, v):
        return v in self.__dict__
    
    def __getitem__ (self, v):
        return self.__dict__[v]

    def __setitem__(self, key, value):
        self.__dict__[key] = value
    
    def __delitem__(self, key):
        del self.__dict__[key]

    def setdefault (self, name, value):
        if not hasattr(self, name):
            setattr(self, name, value)
        return getattr(self, name)

    def set (self, name, value):
        setattr(self, name, value)
        return getattr(self, name)

    def get (self, name, *value):
        if not hasattr(self, name) and 1 == len(value):
            return value[0]
        return getattr(self, name)

    def delete (self, name):
#        if not hasattr(self, name):
#            return
        del self.__dict__[name]
