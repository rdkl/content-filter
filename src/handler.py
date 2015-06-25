#!/usr/bin/env python
#-*- coding: utf-8 -*-

from document_storage import DocumentStorage
from file_reader import FileReader

##############################################################################
class Handler(object):
    def __init__(self):
        self.__storage = DocumentStorage()
        self.__storage.Load()
        
        self.__reader = FileReader('../data/small_ethnic_data_lem.csv',
                                   '../data/small_ethnic_data_no_lem.csv')
        self.__gen = self.__reader.GetTextGenerator()
        self.__last_text_item = None
        
    #-------------------------------------------------------------------------
    def GetText(self):
        self.__last_text_item = self.__gen.next()
        return self.__last_text_item

    #-------------------------------------------------------------------------
    def SetState(self, state):
        self.__last_text_item.set_state(state)
        self.__storage.AddDocument(self.__last_text_item.id, 
                                   self.__last_text_item)
            
    #-------------------------------------------------------------------------
    def __del__(self):
        self.__storage.Save()

    #-------------------------------------------------------------------------            
##############################################################################

if __name__ == "__main__":
    file_reader = Handler()
    print file_reader.GetText()