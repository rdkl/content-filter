#!/usr/bin/env python
#-*- coding: utf-8 -*-

import csv
import io

from text_item import TextItem


##############################################################################
class FileReader(object):
    def __init__(self, filename_lem, filename_non_lem):        
        try:
            self.__reader_lem = csv.reader(
                                   self.reencode(open(filename_lem, "rb")), 
                                   delimiter=';', 
                                   quotechar='"')
        except IOError:
            print "Please check the file with lematized texts", filename_lem
        
        try:
            self.__reader_non_lem = csv.reader(
                                        self.reencode(open(filename_non_lem, "rb")), 
                                        delimiter=';', 
                                        quotechar='"')
        except IOError:
            print "Please check the file with non-lematized texts", \
                filename_non_lem
            
    #-------------------------------------------------------------------------
    def reencode(self, file_lines):
            for line in file_lines:
                yield line.decode('windows-1251').encode('utf-8')
    
    #-------------------------------------------------------------------------    
    def __next_lem(self):
        for items in self.__reader_lem:
            yield items
    
    #-------------------------------------------------------------------------
    def __next_non_lem(self):
        for items in self.__reader_non_lem:
            yield items
    
    #-------------------------------------------------------------------------
    def GetTextGenerator(self, lines_skipped_from_start=1):
        # Skip first line.
        gen_lem = self.__next_lem()
        gen_non_lem = self.__next_non_lem()
        for _ in xrange(lines_skipped_from_start):
            gen_lem.next()
            gen_non_lem.next()
        
        while(True):
            list_lem = gen_lem.next()
            list_non_lem = gen_non_lem.next()
     
            # Last one is empty.       
            if len(list_lem) != 7:
                yield TextItem()
            else:
                yield TextItem(list_lem[0], list_lem[2], list_lem[3], 
                               list_lem[4], list_lem[5],
                               list_lem[1], list_non_lem[1]) 
    #-------------------------------------------------------------------------
##############################################################################

if __name__ == "__main__":
    file_reader = FileReader('../data/small_ethnic_data_lem.csv',
                             '../data/small_ethnic_data_no_lem.csv')
    gen = file_reader.GetTextGenerator()
    print gen.next()
    print gen.next()
    