#!/usr/bin/env python
#-*- coding: utf-8 -*-

import csv

##############################################################################
class FileReader(object):
    def __init__(self, filename):
        try:
            csvfile = open(filename, "rb")
            self.__reader = csv.reader(csvfile, delimiter=';', quotechar='"')
        except IOError:
            print "Please check the file", filename
            
    #-------------------------------------------------------------------------
    def __next(self):
        for items in self.__reader:
            yield [item.decode("cp1251") for item in items]
    
    #-------------------------------------------------------------------------
    def GetTextGenerator(self):
        # Skip first line.
        gen = self.__next()
        gen.next()
        return gen
    #-------------------------------------------------------------------------    
##############################################################################

if __name__ == "__main__":
    file_reader = FileReader('../data/small_ethnic_data_lem.csv')
    gen = file_reader.GetTextGenerator()
    print gen.next()
    print gen.next()