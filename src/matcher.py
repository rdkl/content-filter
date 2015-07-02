#!/usr/bin/env python
#-*- coding: utf-8 -*-

try:
	import libs.AhoCorasick64 as AhoCorasick
except:
	print "Test"
	
##############################################################################
class Matcher(object):
    """ 
    A wrapper for Aho-Corasick from libs.
    """
    def __init__(self, filename="../data/ethnic_words.txt"):
        self.__matcher = AhoCorasick.Matcher()
        self.__matcher.Init(filename)
        self.__dict = {}
        self.__ReadWords(filename)
        
    #-------------------------------------------------------------------------    
    def __ReadWords(self, filename):
        with open(filename, "r") as f:
            word_number = 0
            for line in f.readlines():
                # First line has length ~5.
                if len(line) > 5:
                    self.__dict[word_number] = line[:-1]
                    word_number += 1
                    
    #-------------------------------------------------------------------------    
    def FindWordsInText(self, text):
        return self.__matcher.FindWordsInText(" " + text + " ")
    
    #-------------------------------------------------------------------------
    def GetDict(self):
        return self.__dict
    
    #-------------------------------------------------------------------------
##############################################################################

if __name__ == "__main__":
    m = Matcher()
    a =  m.FindWordsInText("абориген полуюжноафриканцы тат")
    dict = m.GetDict()
    print len("абориген"), len(dict[0])
    for item in a:
        print dict[item], a[item]
    