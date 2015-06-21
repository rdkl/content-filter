#!/usr/bin/env python
#-*- coding: utf-8 -*-
import textwrap
from numpy.random.mtrand import set_state

states = {0 : "Ethnic", 1 : "Non-ethnic", 2 : "Controversal", 3 : "Undefined"}
states_rev = {value : key for key, value in states.items()}

##############################################################################
class TextItem(object):
    def __init__(self, id="-1", state=3, name="Default TextItem", 
                 url="empty url",
                 date="", time="", text_lem="No text available", 
                 text_full="No text available"):
        self.__id = id
        self.__name = name
        self.__url = url
        self.__date = date
        self.__time = time
        self.__text_lem = text_lem
        self.__text_full = text_full
        self.__state = state
        if self.__name != "Default TextItem":
            self.__is_initialized = True
        else:
            self.__is_initialized = False
    
    #-------------------------------------------------------------------------
    @property
    def id(self):
        return self.__id
        
    #-------------------------------------------------------------------------
    @property
    def name(self):
        return self.__name
        
    #-------------------------------------------------------------------------
    @property
    def state(self):
        return self.__state
    
    #-------------------------------------------------------------------------
    def set_state(self, state):
        if type(state) == int:
            if state in states.keys():
                self.__state = state
        else:
            #print states_rev
            if state in states_rev.keys():
                #print states_rev[state], type(states_rev[state])
                self.set_state(states_rev[state])
                return
            
            # str case.
            try:
                state = int(state)
                self.set_state(state)
            except:
                raise TypeError("Unknown state")
        
    #-------------------------------------------------------------------------
    @property
    def state_string(self):
        return states[self.__state]
        
    #-------------------------------------------------------------------------
    @property
    def url(self):
        return self.__url
        
    #-------------------------------------------------------------------------
    @property
    def date(self):
        return self.__date
        
    #-------------------------------------------------------------------------
    @property
    def text_lem(self):
        return self.__text_lem
        
    #-------------------------------------------------------------------------
    @property
    def text_full(self):
        return self.__text_full

    #-------------------------------------------------------------------------
    def IsInitialized(self):
        return self.__is_initialized
    
    #-------------------------------------------------------------------------
    def __str__(self):
        res = "-" * 80 + "\n"
        res += "ID = " + self.id 
        res += ", user: |" + self.name + "| from |" + self.url + "|\n"
        res += "Full text: |" + textwrap.fill(self.text_full, 100) + "|\n"
        res += "=" * 80 + "\n"
        res += "Lemm text: |" + textwrap.fill(self.text_lem, 100) + "|\n"
        res += "Date: " + self.date + ", time = " + self.__time + "."
        res += "\n" + "-" * 80 + "\n"
        return res
    
    #-------------------------------------------------------------------------
##############################################################################

#-----------------------------------------------------------------------------
if __name__ == "__main__":
    ti = TextItem("-1", "name", "url", "date", "time", "1", "1")
    print ti
    print ti.text_full