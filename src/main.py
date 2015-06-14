#!/usr/bin/env python
#-*- coding: utf-8 -*-

import wx

from gui.MainFrame import MainFrame

##############################################################################
class App(wx.App):
    def OnInit(self):
        self.frame = MainFrame()
        self.frame.Show()
        self.SetTopWindow(self.frame)
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