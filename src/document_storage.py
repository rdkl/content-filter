#!/usr/bin/env python
#-*- coding: utf-8 -*-

import cPickle

##############################################################################
class DocumentStorage(object):
    def __init__(self):
        self.dict = {}
    
    #-------------------------------------------------------------------------    
    def AddDocument(self, doc_id, text_item):
        self.dict[str(doc_id)] = text_item
        
    #-------------------------------------------------------------------------    
    def Save(self, filename="../data/saved_documents"):
        cPickle.dump(self.dict, open(filename, "wb"))
    
    #-------------------------------------------------------------------------    
    def Load(self, filename="../data/saved_documents"):
        print filename
        #self.dict = cPickle.load(open(filename, "rb"))
        #for item in sorted(self.dict.keys()):
        #     print self.dict[item]

    #-------------------------------------------------------------------------    
    def GetDocuments(self):
        # Should return matrix of features and labels (numpy matrix and array)
        pass
    
    #-------------------------------------------------------------------------
    def GetMaxId(self):
        return int(max(self.dict.keys() + ["0"]))    

    #-------------------------------------------------------------------------
##############################################################################