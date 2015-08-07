#!/usr/bin/env python
# *- coding: utf-8 -*-
import textwrap

states = {0 : "Ethnic", 1 : "Non-ethnic", 2 : "Controversial", 3 : "Undefined"}
states_rev = {value : key for key, value in states.items()}

##############################################################################
class TextItem(object):
    def __init__(self, id="-1", state=3,
                 text_lem="No text available",
                 text_full="No text available"):
        self.__id = id
        self.__text_lem = text_lem
        self.__text_full = text_full
        self.__state = state
    
    # ------------------------------------------------------------------------
    @property
    def id(self):
        return self.__id
        
    # ------------------------------------------------------------------------
    @property
    def state(self):
        return self.__state
    
    # ------------------------------------------------------------------------
    def set_state(self, state):
        if type(state) == int:
            if state in states.keys():
                self.__state = state
        else:
            if state in states_rev.keys():
                self.set_state(states_rev[state])
                return
            
            # str case.
            try:
                state = int(state)
                self.set_state(state)
            except:
                raise TypeError("Unknown state")
        
    # ------------------------------------------------------------------------
    @property
    def state_string(self):
        return states[self.__state]
        
    # ------------------------------------------------------------------------
    @property
    def text_lem(self):
        return self.__text_lem
        
    # ------------------------------------------------------------------------
    @property
    def text_full(self):
        return self.__text_full

    # ------------------------------------------------------------------------
    def __str__(self):
        res = "-" * 80 + "\n"
        res += "ID = " + str(self.id) + ", state="+ str(self.state) + "\n"
        res += "Full text: |" + textwrap.fill(self.text_full, 100) + "|\n"
        res += "=" * 80 + "\n"
        res += "Lemm text: |" + textwrap.fill(self.text_lem, 100) + "|\n"
        res += "\n" + "-" * 80 + "\n"
        return res
    
    # ------------------------------------------------------------------------
##############################################################################

# ----------------------------------------------------------------------------
if __name__ == "__main__":
    ti = TextItem("-1" , 3, "1", "1")
    print ti
    print ti.text_full