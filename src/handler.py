#!/usr/bin/env python
#-*- coding: utf-8 -*-

import random

from document_storage import DocumentStorage
from file_reader import FileReader


##############################################################################
class Handler(object):
    def __init__(self, prefix="./"):
        self.__storage = DocumentStorage()
        print prefix + "../data/saved_documents"
        self.__storage.Load(prefix + "../data/saved_documents")
        
        #self.__reader = FileReader(prefix + '../data/small_ethnic_data_lem.csv',
        #                           prefix + '../data/small_ethnic_data_no_lem.csv')
        self.__reader = FileReader('/media/rdkl/data/ethnic_data/lem.csv',
                                   '/media/rdkl/data/ethnic_data/no_lem.csv')
        
        print self.__storage.GetMaxId()
        self.__gen = self.__reader.GetTextGenerator(2)
                        #self.__storage.GetMaxId() + 2 + random.randint(0, 40))
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
        #self.__storage.Save()
        pass

    #-------------------------------------------------------------------------            
##############################################################################

if __name__ == "__main__":
    file_reader = Handler()
    print file_reader.GetText()