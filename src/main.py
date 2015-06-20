#!/usr/bin/env python
#-*- coding: utf-8 -*-

import wx

from gui.MainFrame import MainFrame
from src.file_reader import FileReader


##############################################################################
class App(wx.App):
    def OnInit(self):
        self.frame = MainFrame()
        self.frame.Show()
        self.SetTopWindow(self.frame)
        file_reader = FileReader('../data/small_ethnic_data_lem.csv',
                             '../data/small_ethnic_data_no_lem.csv')
        gen = file_reader.GetTextGenerator(40)
        self.frame.PrintTextItem(gen.next())
        
        return True

    #-------------------------------------------------------------------------
    def OnExit(self):
        print "OnExit"
    
    #-------------------------------------------------------------------------
##############################################################################

#-----------------------------------------------------------------------------
if __name__ == "__main__":
    app = App()
    app.MainLoop()
    print "Done."