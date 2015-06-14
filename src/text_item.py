#!/usr/bin/env python
#-*- coding: utf-8 -*-
import textwrap


##############################################################################
class TextItem(object):
    def __init__(self, id="-1", name="Default TextItem", url="empty url",
                 date="", time="", text_lem="No text available", 
                 text_full="No text available"):
        self.__id = id
        self.__name = name
        self.__url = url
        self.__date = date
        self.__time = time
        self.__text_lem = text_lem
        self.__text_full = text_full
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