#-*-coding: utf-8 -*-

import wx

##############################################################################
class MainFrame(wx.Frame):
    def __init__(self, title = 'GUI', size = (1366, 768)):
        wx.Frame.__init__(self, parent=None, id=-1, title=title, size=size)
        self.DoLayout()
            
    #-------------------------------------------------------------------------
    def MakeStaticText(self, text="Test text", label="Text label"):
        text_panel = wx.Panel(self, wx.ID_ANY)
        static_text = wx.StaticText(text_panel, wx.ID_ANY, text, 
                                  style=wx.TE_MULTILINE)
        staticbox = wx.StaticBox(self, wx.NewId(), label=label)
        staticbox_sizer = wx.StaticBoxSizer(staticbox, wx.HORIZONTAL)
        staticbox_sizer.Add(text_panel, proportion=1, flag=wx.EXPAND)
        
        return static_text, staticbox_sizer
        
    #-------------------------------------------------------------------------
    def DoLayout(self): 
        parent_sizer = wx.BoxSizer(wx.VERTICAL)
        texts_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
         
        self.text_info, sizer_info = self.MakeStaticText(
                                             text="Good news, everyone!", 
                                             label="Information")
        self.text_non_lemm, sizer_non_lemm = self.MakeStaticText(
                                             text="Non-lemm text\n", 
                                             label="Non lematized text")
        self.text_lemm, sizer_lemm = self.MakeStaticText(
                                             text="Lemm text\n", 
                                             label="Lematized text")
                
        texts_sizer.Add(sizer_info, proportion = 1)
        texts_sizer.Add(sizer_non_lemm, proportion = 1)
        texts_sizer.Add(sizer_lemm, proportion = 1)  
                
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
        #self.Bind(wx.EVT_BUTTON, self.OnButtonDisplayPressed, 
        #          self.button_display_mode)
        
        parent_sizer.Add(texts_sizer, flag=wx.EXPAND, proportion=1)
        parent_sizer.Add(button_sizer, flag=wx.EXPAND)
        self.SetSizer(parent_sizer)
        
        self.Layout()
        
        #self.PrintIntoStaticText(self.text_info, "- \n" * 100)
   
    #-------------------------------------------------------------------------
    def PrintIntoStaticText(self, static_text, string_to_write, 
                               rewrite = True):
        if rewrite:
            static_text.SetLabel(string_to_write)
            return
        
        displayed_string = static_text.GetLabelText()
        number_of_string = displayed_string.count("\n")
        if number_of_string > 5:
            to_display = displayed_string[displayed_string.find("\n") + 1:] +\
                            "\n" + string_to_write
        else:
            to_display = displayed_string + "\n" + string_to_write
        
        static_text.SetLabel(to_display)
        
    #-------------------------------------------------------------------------
    def OnButtonClosePressed(self, event):
        self.Close(True)
    
    #-------------------------------------------------------------------------
##############################################################################