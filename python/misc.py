#!/usr/bin/python


class KMG():
    def __init__(self, base):
        self.base = base

    @property
    def k(self):
        return self.base
        
    @property
    def m(self):
        return self.base * self.base
        
    @property
    def g(self):
        return self.base * self.base * self.base
        
    @property
    def t(self):
        return self.base * self.base * self.base * self.base
        
    @property
    def p(self):
        return self.base * self.base * self.base * self.base * self.base
