# -*- coding: utf-8 -*-

import wx
from UIDesign import PanelOne, PanelTwo
#import Binomial_Model
#from Binomial_Model import *

__author__ = 'Henry'
__date__ = '2017-11-19'


class MainWindow(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY,
                          "Option Calculator")

        self.panel_one = PanelOne(self)
        self.panel_two = PanelTwo(self)
        self.panel_one.Hide()

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.panel_one, 1, wx.EXPAND)
        self.sizer.Add(self.panel_two, 1, wx.EXPAND)
        self.SetSizer(self.sizer)


        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        switch_panels_menu_item = fileMenu.Append(wx.ID_ANY,
                                                  "Switch Panels",
                                                  "Some text")
        self.Bind(wx.EVT_MENU, self.onSwitchPanels,
                  switch_panels_menu_item)
        menubar.Append(fileMenu, '&Tool')
        self.SetMenuBar(menubar)


    def onSwitchPanels(self, event):
        """"""
        if self.panel_one.IsShown():
            self.SetTitle("Panel Two Showing")
            self.panel_one.Hide()
            self.panel_two.Show()
        else:
            self.SetTitle("Panel One Showing")
            self.panel_one.Show()
            self.panel_two.Hide()
        self.Layout()


app = wx.App()
main_win = MainWindow()
main_win.Show()
app.MainLoop()