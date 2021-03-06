#!/usr/bin/env python
# *- coding: utf-8 -*-

import csv
import sys

from text_item import TextItem

csv.field_size_limit(sys.maxsize)

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
                                        self.reencode(open(filename_non_lem, 
                                                           "rb")), 
                                        delimiter=';', 
                                        quotechar='"')
        except IOError:
            print "Please check the file with non-lematized texts", \
                filename_non_lem

    # ------------------------------------------------------------------------
    def reencode(self, file_lines):
        # Default encoding for csv made on win.
        for line in file_lines:
            yield line.decode('windows-1251', errors='ignore').encode('utf-8')

    # ------------------------------------------------------------------------    
    def __next_lem(self):
        for items in self.__reader_lem:
            yield items
    
    # ------------------------------------------------------------------------
    def __next_non_lem(self):
        for items in self.__reader_non_lem:
            yield items
    
    # ------------------------------------------------------------------------
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
            
            if list_lem[0] != list_non_lem[0]:
                print "Error: ids are not the same!" 
                print "Lem id =", list_lem[0]
                print "Non-lem id = ", list_non_lem[0] 
                yield TextItem(text_full="Ids are not the same")
                continue
                
            # Last one is empty.       
            if len(list_lem) != 7:
                yield TextItem()
            else:
                yield TextItem(id=list_lem[0], 
                               state=3,
                               text_lem=list_lem[1],
                               text_full=list_non_lem[1])
                
    # ------------------------------------------------------------------------
##############################################################################

if __name__ == "__main__":
    file_reader = FileReader('../data/small_ethnic_data_lem.csv',
                             '../data/small_ethnic_data_no_lem.csv')
    gen = file_reader.GetTextGenerator()
    print gen.next()
    print gen.next()
