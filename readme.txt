BinomialOptnCal

This is an option price calculator based on binomial model with a simple UI design. This is the 0.1.0 version. There are two panels for users to use and develop. One is the calculator for real traded stock options based on market data from Yahoo Finance. The other is a more general calculator that users can input any parameter for option at will for practice. The intended users are undergraduate students who major in mathematical finance or financial engineering. 
I'm not a proficient programmer so there will certainly be some bugs within this package. Please let me know if you observe any of them. henryguoziheng@gmail.com

For further version, the UI will be promoted and there will be more entry points.

Thanks to Kelvin Xue in DataYes for his basic idea in building binomial model.
Thanks to Peter Yu for providing program structure and data crawler.

Install

pip install BinomialOptCal


Usage

After installation, run the following code:

import wx
from BinomialOptnCal import Main

app = wx.App()
main_win = Main.MainWindow()
main_win.Show()
app.MainLoop()