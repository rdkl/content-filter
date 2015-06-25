#-*-coding: utf-8 -*-

import wx
from text_item import states


##############################################################################
class MainFrame(wx.Frame):
    def __init__(self, handler, title = 'GUI', size = (1366, 768)):
        self.handler = handler
        wx.Frame.__init__(self, parent=None, id=-1, title=title, size=size)
        self.DoLayout()
                
    #-------------------------------------------------------------------------
    def MakeStaticText(self, 
                       text="Test text", 
                       label="Text label", 
                       size=(250, 250)):
        text_panel = wx.Panel(self, wx.ID_ANY)
    
        style = wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_RICH
        text_ctrl = wx.TextCtrl(text_panel, wx.ID_ANY, text, 
                                  style=style, 
                                  size=size)
        staticbox = wx.StaticBox(self, wx.NewId(), label=label)
        staticbox_sizer = wx.StaticBoxSizer(staticbox, wx.HORIZONTAL)
        staticbox_sizer.Add(text_panel, proportion=1, flag=wx.EXPAND|wx.ALL)
        
        return text_ctrl, staticbox_sizer
        
    #-------------------------------------------------------------------------
    def DoLayout(self): 
        parent_sizer = wx.BoxSizer(wx.VERTICAL)
        texts_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
         
        self.text_info, sizer_info = self.MakeStaticText(
                                             text="Good news, everyone!", 
                                             label="Information",
                                             size=(450, 700))
        self.text_non_lemm, sizer_non_lemm = self.MakeStaticText(
                                             text="Non-lemm text\n", 
                                             label="Non lematized text",
                                             size=(450, 700))
        self.text_lemm, sizer_lemm = self.MakeStaticText(
                                             text="Lemm text\n", 
                                             label="Lematized text",
                                             size=(450, 700))
                
        texts_sizer.Add(sizer_info)
        texts_sizer.Add(sizer_non_lemm)
        texts_sizer.Add(sizer_lemm)  
        
          
        self.button_save = wx.Button(self, wx.NewId(), "Save data")
        self.button_load = wx.Button(self, wx.NewId(), "Load data")
        self.button_settings = wx.Button(self, wx.NewId(), "Settings")
        self.button_close = wx.Button(self, wx.ID_EXIT)

        button_sizer.Add(self.button_save, proportion = 0, flag = wx.ALL, 
                         border = 4)
        button_sizer.Add(self.button_load, proportion = 0, flag = wx.ALL, 
                         border = 4)
        button_sizer.Add(wx.Size(10, 10), proportion = 1)
        button_sizer.Add(self.button_settings, proportion = 0, 
                         flag = wx.ALL, border = 4)
        button_sizer.Add(self.button_close, proportion = 0, flag = wx.ALL, 
                         border = 4)
        
        self.Bind(wx.EVT_BUTTON, self.OnButtonClosePressed, 
                  self.button_close)
        
        parent_sizer.Add(texts_sizer, flag=wx.EXPAND, proportion=1)
        parent_sizer.Add(button_sizer, flag=wx.EXPAND)
        self.SetSizer(parent_sizer)
        
        self.button_load.Bind(wx.EVT_BUTTON, self.OnKeyPressed)

        #self.PrintTextItem(self.handler.GetText())
        self.Layout()
        
    #-------------------------------------------------------------------------
    def PrintIformation(self, string):
        self.text_info.AppendText(string)
       
    #-------------------------------------------------------------------------
    def PrintTextItem(self, text_item):
        self.text_lemm.SetValue(text_item.text_lem)
        self.text_non_lemm.SetValue(text_item.text_full)
        
    #-------------------------------------------------------------------------
    def OnButtonClosePressed(self, event):
        self.Close(True)
    
    #-------------------------------------------------------------------------
    def OnKeyPressed(self, event):
        dlg = wx.SingleChoiceDialog(None,
        'Is document ethnic?',
        'Single Choice',
         states.values())
        
        if dlg.ShowModal() == wx.ID_OK:
            response = dlg.GetStringSelection()
        else:
            response = None
            # return
            
        dlg.Destroy()
        
        # response
        # Load next document and save info about that document.
        print response
        self.handler.SetState(response)
        self.PrintTextItem(self.handler.GetText())
        
    #-------------------------------------------------------------------------
##############################################################################