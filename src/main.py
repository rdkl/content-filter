#!/usr/bin/env python
# *- coding: utf-8 -*-

import os
import sys
import wx

project_path = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) +
                               "/../")

sys.path.append(project_path)

from src.gui.MainFrame import MainFrame
from src.handler import Handler


##############################################################################
class App(wx.App):
    def OnInit(self):
        self.handler = Handler()
        self.frame = MainFrame(self.handler)
        self.frame.Show()
        self.SetTopWindow(self.frame)        
        return True

    # ------------------------------------------------------------------------
    def OnExit(self):
        del self.handler
        print "OnExit"
    
    # ------------------------------------------------------------------------
##############################################################################

# ----------------------------------------------------------------------------
if __name__ == "__main__":
    sys.path.append("..")
    app = App()
    app.MainLoop()
    
    print "Done."