# -*- coding: utf-8 -*-

from __future__ import division
import pandas_market_calendars as mcal
import wx
import Binomial_Model
from Binomial_Model import *
import pandas_datareader as pdr
import numpy as np
import datetime

__author__ = 'Henry'
__date__ = '2017-11-20'


class PanelOne(wx.Panel):

    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent)
        #txt = wx.TextCtrl(self)

        bSizer1 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText7 = wx.StaticText( self, wx.ID_ANY, u"Option Style", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText7.Wrap( -1 )
        bSizer1.Add( self.m_staticText7, 0, wx.ALL, 5 )

        optionStyleChoices = [ u"European Call Option", u"European Put Option", u"American Call Option", u"American Put Option" ]
        self.optionStyle = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, optionStyleChoices, 0 )
        self.optionStyle.SetSelection( 0 )
        bSizer1.Add( self.optionStyle, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"Strike Pirce", wx.Point( -100,-100 ), wx.DefaultSize, 0 )
        self.m_staticText1.Wrap( -1 )
        bSizer1.Add( self.m_staticText1, 0, wx.ALL, 5 )

        self.strike = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer1.Add( self.strike, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"Volatility", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText2.Wrap( -1 )
        bSizer1.Add( self.m_staticText2, 0, wx.ALL, 5 )

        self.volatility = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer1.Add( self.volatility, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"Spot Pirce", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText3.Wrap( -1 )
        bSizer1.Add( self.m_staticText3, 0, wx.ALL, 5 )

        self.spot = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer1.Add( self.spot, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_staticText4 = wx.StaticText( self, wx.ID_ANY, u"Maturity", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText4.Wrap( -1 )
        bSizer1.Add( self.m_staticText4, 0, wx.ALL, 5 )

        self.maturity = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer1.Add( self.maturity, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_staticText5 = wx.StaticText( self, wx.ID_ANY, u"Dividend Rate", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText5.Wrap( -1 )
        bSizer1.Add( self.m_staticText5, 0, wx.ALL, 5 )

        self.dividend = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer1.Add( self.dividend, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_staticText6 = wx.StaticText( self, wx.ID_ANY, u"Risk Free  Interest Rate", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText6.Wrap( -1 )
        bSizer1.Add( self.m_staticText6, 0, wx.ALL|wx.EXPAND, 5 )

        self.interest = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer1.Add( self.interest, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_button1 = wx.Button( self, wx.ID_ANY, u"OK", wx.Point( -1,-1 ), wx.DefaultSize, 0 )
        bSizer1.Add( self.m_button1, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_staticText8 = wx.StaticText( self, wx.ID_ANY, u"Option Value", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText8.Wrap( -1 )
        bSizer1.Add( self.m_staticText8, 0, wx.ALL|wx.EXPAND, 5 )

        self.optionValue = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer1.Add( self.optionValue, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_staticText9 = wx.StaticText( self, wx.ID_ANY, u"Hedge Ratio", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText9.Wrap( -1 )
        bSizer1.Add( self.m_staticText9, 0, wx.ALL, 5 )

        self.m_textCtrl8 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer1.Add( self.m_textCtrl8, 0, wx.ALL|wx.EXPAND, 5 )

        self.SetSizer( bSizer1 )
        self.Layout()

        self.Centre( wx.BOTH )

        # Connect Events
        self.m_button1.Bind( wx.EVT_BUTTON, self.main_button_click )

    def __del__( self ):
        pass


    # Virtual event handler
    def main_button_click(self, event):
        strike = float(self.strike.GetValue())
        sigma = float(self.volatility.GetValue())
        spot = float(self.spot.GetValue())

        maturity = str(self.maturity.GetValue())
        nyse = mcal.get_calendar('NYSE')
        early = nyse.schedule(start_date = datetime.datetime.now().strftime('%Y-%m-%d'), end_date = maturity)
        ttm = len(early)/252

        d = float(self.dividend.GetValue())
        r = float(self.interest.GetValue())
        tSteps = 100

        if self.optionStyle.GetSelection() == 0:
            testTree = Binomial_Model.BinomialTree(spot, r, d, tSteps, ttm, sigma, JarrowRuddTraits, strike)
            testTree.roll_back()
            self.optionValue.SetValue(str(testTree.lattice[0][0]))

            tree = GetHedgeRatio(spot, r, d, tSteps, ttm, sigma, JarrowRuddTraits, strike)
            tree.build_node_euroCall()
            self.m_textCtrl8.SetValue(str('Stock:'+str(tree.stock[0][0])+'   Cash'+str(tree.cash[0][0])))

        elif self.optionStyle.GetSelection() == 1:
            testTree = Binomial_Model.BinomialTree(spot, r, d, tSteps, ttm, sigma, JarrowRuddTraits, strike)
            testTree.roll_back_put()
            self.optionValue.SetValue(str(testTree.lattice[0][0]))

            tree = GetHedgeRatio(spot, r, d, tSteps, ttm, sigma, JarrowRuddTraits, strike)
            tree.build_node_euroPut()
            self.m_textCtrl8.SetValue(str('Stock:'+str(tree.stock[0][0])+'   Cash'+str(tree.cash[0][0])))

        elif self.optionStyle.GetSelection() == 2:
            testTree = Binomial_Model.ExtendBinomialTree(spot, r, d, tSteps, ttm, sigma, JarrowRuddTraits, strike)
            testTree.roll_back_american()
            self.optionValue.SetValue(str(testTree.lattice[0][0]))

            tree = GetHedgeRatio(spot, r, d, tSteps, ttm, sigma, JarrowRuddTraits, strike)
            tree.build_node_amerCall()
            self.m_textCtrl8.SetValue(str('Stock:'+str(tree.stock[0][0])+'   Cash'+str(tree.cash[0][0])))

        elif self.optionStyle.GetSelection() == 3:
            testTree = Binomial_Model.ExtendBinomialTree(spot, r, d, tSteps, ttm, sigma, JarrowRuddTraits, strike)
            testTree.roll_back_american_put()
            self.optionValue.SetValue(str(testTree.lattice[0][0]))

            tree = GetHedgeRatio(spot, r, d, tSteps, ttm, sigma, JarrowRuddTraits, strike)
            tree.build_node_amerPut()
            self.m_textCtrl8.SetValue(str('Stock:'+str(tree.stock[0][0])+'   Cash'+str(tree.cash[0][0])))




########################################################################
class PanelTwo(wx.Panel):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent)

        bSizer2 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText9 = wx.StaticText( self, wx.ID_ANY, u"Option Style", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText9.Wrap( -1 )
        bSizer2.Add( self.m_staticText9, 0, wx.ALL, 5 )

        styleChoices = [ u"European Call Option", u"European Put Option", u"American Call Option", u"American Put Option" ]
        self.style = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, styleChoices, 0 )
        self.style.SetSelection( 0 )
        bSizer2.Add( self.style, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_staticText14 = wx.StaticText( self, wx.ID_ANY, u"Ticker", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText14.Wrap( -1 )
        bSizer2.Add( self.m_staticText14, 0, wx.ALL, 5 )

        self.ticker = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer2.Add( self.ticker, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_staticText6 = wx.StaticText( self, wx.ID_ANY, u"Strike", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText6.Wrap( -1 )
        bSizer2.Add( self.m_staticText6, 0, wx.ALL, 5 )

        self.strike = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer2.Add( self.strike, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_staticText10 = wx.StaticText( self, wx.ID_ANY, u"Maturity", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText10.Wrap( -1 )
        bSizer2.Add( self.m_staticText10, 0, wx.ALL, 5 )

        self.maturity = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer2.Add( self.maturity, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_staticText11 = wx.StaticText( self, wx.ID_ANY, u"Interest Rate", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText11.Wrap( -1 )
        bSizer2.Add( self.m_staticText11, 0, wx.ALL, 5 )

        self.interest = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer2.Add( self.interest, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_staticText7 = wx.StaticText( self, wx.ID_ANY, u"Forward Auunal Dividend Yield", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText7.Wrap( -1 )
        bSizer2.Add( self.m_staticText7, 0, wx.ALL, 5 )

        self.dividend = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer2.Add( self.dividend, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_button2 = wx.Button( self, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer2.Add( self.m_button2, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_staticText13 = wx.StaticText( self, wx.ID_ANY, u"Option Value", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText13.Wrap( -1 )
        bSizer2.Add( self.m_staticText13, 0, wx.ALL, 5 )

        self.optionValue = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer2.Add( self.optionValue, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_staticText13 = wx.StaticText( self, wx.ID_ANY, u"Hedge Ratio", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText13.Wrap( -1 )
        bSizer2.Add( self.m_staticText13, 0, wx.ALL, 5 )

        self.m_textCtrl7 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer2.Add( self.m_textCtrl7, 0, wx.ALL|wx.EXPAND, 5 )

        self.SetSizer( bSizer2 )
        self.Layout()

        self.Centre( wx.BOTH )

        # Connect Events
        self.m_button2.Bind( wx.EVT_BUTTON, self.main_button_click2 )

    def __del__( self ):
        pass

    # Virtual event handler
    def main_button_click2( self, event ):
        strike = float(self.strike.GetValue())

        maturity = str(self.maturity.GetValue())
        nyse = mcal.get_calendar('NYSE')
        early = nyse.schedule(start_date = datetime.datetime.now().strftime('%Y-%m-%d'), end_date = maturity)
        ttm = len(early)/252

        r = float(self.interest.GetValue())
        d = float(self.dividend.GetValue())
        ticker = str(self.ticker.GetValue())

        endDate = datetime.datetime.now().strftime('%Y-%m-%d')
        startDate = (datetime.datetime.now() - datetime.timedelta(days = 365)).strftime('%Y-%m-%d')
        hisData = pdr.get_data_yahoo(str(ticker), start=startDate, end = endDate)
        df = hisData['Adj Close']
        df = df.pct_change()
        sigma = df.std()*np.sqrt(len(df))

        spot = hisData['Adj Close'][-1]
        tSteps = 100

        if self.style.GetSelection() == 0:
            testTree = Binomial_Model.BinomialTree(spot, r, d, tSteps, ttm, sigma, JarrowRuddTraits, strike)
            testTree.roll_back()
            self.optionValue.SetValue(str(testTree.lattice[0][0]))

            tree = GetHedgeRatio(spot, r, d, tSteps, ttm, sigma, JarrowRuddTraits, strike)
            tree.build_node_euroCall()
            self.m_textCtrl7.SetValue(str('Stock:'+str(tree.stock[0][0])+'   Cash'+str(tree.cash[0][0])))

        elif self.style.GetSelection() == 1:
            testTree = Binomial_Model.BinomialTree(spot, r, d, tSteps, ttm, sigma, JarrowRuddTraits, strike)
            testTree.roll_back_put()
            self.optionValue.SetValue(str(testTree.lattice[0][0]))

            tree = GetHedgeRatio(spot, r, d, tSteps, ttm, sigma, JarrowRuddTraits, strike)
            tree.build_node_euroPut()
            self.m_textCtrl7.SetValue(str('Stock:'+str(tree.stock[0][0])+'   Cash'+str(tree.cash[0][0])))

        elif self.style.GetSelection() == 2:
            testTree = Binomial_Model.ExtendBinomialTree(spot, r, d, tSteps, ttm, sigma, JarrowRuddTraits, strike)
            testTree.roll_back_american()
            self.optionValue.SetValue(str(testTree.lattice[0][0]))

            tree = GetHedgeRatio(spot, r, d, tSteps, ttm, sigma, JarrowRuddTraits, strike)
            tree.build_node_amerCall()
            self.m_textCtrl7.SetValue(str('Stock:'+str(tree.stock[0][0])+'   Cash'+str(tree.cash[0][0])))

        elif self.style.GetSelection() == 3:
            testTree = Binomial_Model.ExtendBinomialTree(spot, r, d, tSteps, ttm, sigma, JarrowRuddTraits, strike)
            testTree.roll_back_american_put()
            self.optionValue.SetValue(str(testTree.lattice[0][0]))

            tree = GetHedgeRatio(spot, r, d, tSteps, ttm, sigma, JarrowRuddTraits, strike)
            tree.build_node_amerPut()
            self.m_textCtrl7.SetValue(str('Stock:'+str(tree.stock[0][0])+'   Cash'+str(tree.cash[0][0])))










