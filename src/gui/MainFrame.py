#-*-coding: utf-8 -*-
import os

import wx
import sys
import re
from src.text_item import states
from src.matcher import Matcher

##############################################################################
class MainFrame(wx.Frame):
    def __init__(self, handler, title = 'GUI', size = (1200, 700)):
        self.handler = handler
        self.matcher = Matcher()
        wx.Frame.__init__(self, parent=None, id=-1, title=title, size=size)
        self.DoLayout()

                
    #-------------------------------------------------------------------------
    def MakeStaticText(self, 
                       text="Test text", 
                       label="Text label", 
                       size=(250, 250)):
        text_panel = wx.Panel(self, wx.ID_ANY)
    
        style = wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_RICH2
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
        
        textbox_size = ((self.Size[0] - 40) / 3, self.Size[1] - 50)
        
        self.text_info, sizer_info = self.MakeStaticText(
                                            text="Good news, everyone!", 
                                            label="Information",
                                            size=(textbox_size[0] / 2, 
                                                  textbox_size[1]))
        self.text_non_lemm, sizer_non_lemm = self.MakeStaticText(
                                             text="Non-lemm text\n", 
                                             label="Non lematized text",
                                             size=textbox_size)
        self.text_lemm, sizer_lemm = self.MakeStaticText(
                                             text="Lemm text\n", 
                                             label="Lematized text",
                                             size=textbox_size)
        
        self.text_words, sizer_words = self.MakeStaticText(
                                             text="Found words\n", 
                                             label="Words from list",
                                             size=(textbox_size[0] / 2, 
                                                  textbox_size[1]))
                
        texts_sizer.Add(sizer_info)
        texts_sizer.Add(sizer_non_lemm)
        texts_sizer.Add(sizer_lemm) 
        texts_sizer.Add(sizer_words)
          
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

        self.PrintTextItem(self.handler.GetText())
        self.Layout()
        
    #-------------------------------------------------------------------------
    def PrintIformation(self, string):
        self.text_info.AppendText(string)
       
    #-------------------------------------------------------------------------
    def PrintTextItem(self, text_item):
        # UTF-8 positions, while text in textctrl is unicode.
        words_with_positions = \
            self.matcher.FindWordsInTextWithPositions(text_item.text_lem)

        self.text_lemm.SetValue(text_item.text_lem)
        text = text_item.text_lem.decode("utf-8")

        words = self.matcher.GetDict()
        for word_index in words_with_positions:
            word_len = len(words[word_index].decode("utf-8"))
            starts = [m.start()
                      for m in re.finditer(words[word_index].decode("utf-8"),
                                           text)]
            for start in starts:
                self.text_lemm.SetStyle(start,
                                        start + word_len,
                                        wx.TextAttr("black", "yellow"))

            #for position in words_with_positions[word_index]:
            #    self.text_lemm.SetStyle(get_position(position),
            #                            get_position(position + word_len),
            #                            wx.TextAttr("black", "yellow"))

        self.text_non_lemm.SetValue(text_item.text_full.decode("utf-8"))
        words = self.matcher.FindWordsInText(text_item.text_lem)
        all_words = self.matcher.GetDict()
        
        string = ""
        for item in words:
            string += "%.2d " % words[item] + all_words[item] + "\n"
        
        if len(words) == 0:
            string = "No words found"
            
        self.text_words.SetValue(string.decode("utf-8"))
        
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
        
        # Load next document and save info about that document.
        if response is not None:
            self.handler.SetState(response)

        self.PrintTextItem(self.handler.GetText())
        
    #---------------------------------------------------------------------------
################################################################################