#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import wx

from gui.MainFrame import MainFrame
from handler import Handler


##############################################################################
class App(wx.App):
    def OnInit(self):
        self.handler = Handler()
        self.frame = MainFrame(self.handler)
        self.frame.Show()
        self.SetTopWindow(self.frame)        
        return True

    #-------------------------------------------------------------------------
    def OnExit(self):
        del self.handler
        print "OnExit"
    
    #-------------------------------------------------------------------------
##############################################################################

#-----------------------------------------------------------------------------
if __name__ == "__main__":
    sys.path.append("..")
    app = App()
    app.MainLoop()
    
    print "Done."