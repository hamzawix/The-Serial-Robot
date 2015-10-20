__author__ = 'HAMZA BOUGHRAIRA'

"""
this file contains three classes: 
the plotmanager class to plot data on a static plot
the histogramplotmanager to extract histograms from the video and plot them on a static plot
the liveplotmanager class to make a real time data visualisation on a dynamic plot"""

import matplotlib #the matplotlib library for plotting data
"""
matplotlib uses the Tkinter library by default as its GUI, 
we need to import extra packages to integrate matplotlib into wxPython""" 
matplotlib.use('WXAgg')#for wxPython
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg #the figure canavas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg# the toolbar in the bottom
from matplotlib.figure import Figure #the figure that contains the subplots
import wx # wxPython
import csv #the CSV module

class Plotmanager(wx.Frame):
    def __init__(self, *args, **kw):
        super(Plotmanager, self).__init__(*args, **kw)
        #creating the GUI to make a static plot
        self.figure = Figure()
        self.taxes = self.figure.add_subplot(131,
                                             title='Temperature-Plot',
                                             xlabel='Time(s)',
                                             ylabel='Temp(C)',
                                             ylim=([10, 80]))
        self.haxes = self.figure.add_subplot(132,
                                             title='Humidity-Plot',
                                             xlabel='Time(s)',
                                             ylabel=('Hum(%s)' % '%'),
                                             ylim=([10, 80]))
        self.laxes = self.figure.add_subplot(133,
                                             title='Light-Plot',
                                             xlabel='Time(s)',
                                             ylabel=('Light(%s)' % '%'),
                                             ylim=([0, 100]))

        self.taxes.grid()
        self.laxes.grid()
        self.haxes.grid()

        self.SetBackgroundColour(wx.NamedColour("WHITE"))
        self.canavas = FigureCanvasWxAgg(self, -1, self.figure)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canavas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.SetSizer(self.sizer)
        self.Fit()
        self.toolbar = NavigationToolbar2WxAgg(self.canavas)
        self.toolbar.Realize()
        if wx.Platform == '__WXMAC__':
        	#if you are on the MAC OSx
        	self.SetToolbar(self.toolbar)
        else:
        	#Linux and Windows
        	tw, th = self.toolbar.GetSizeTuple()
        	fw, fh = self.toolbar.GetSizeTuple()
        self.toolbar.SetSize(wx.Size(fw, th))
        self.sizer.Add(self.toolbar, 0, wx.LEFT | wx.EXPAND)
        self.toolbar.update()
        self.figure.tight_layout()
        self.figure.subplots_adjust()
        self.Bind(wx.EVT_CLOSE, self.whenclose)

    def maketheplot(self, name):
    	""" in this method we read from a CSV file our data and then we plot it"""
        i = []
        tvalues = []
        hvalues = []
        lvalues = []

        with open(name, 'r') as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                try:
                    i.append(int(row[0]))
                    tvalues.append(int(row[1]))
                    hvalues.append(int(row[2]))
                    lvalues.append(int(row[3]))
                except ValueError:
                    pass

        self.taxes.plot(i, tvalues, lw=2, color='r')
        self.haxes.plot(i, hvalues, lw=2, color='b')
        self.laxes.plot(i, lvalues, lw=2, color='y')


    def whenclose(self, e):
        self.GetParent().Enable()
        if not self.GetParent().timer.IsRunning():
            self.GetParent().timer.Start()
        self.Destroy()
        wx.MessageBox('To plot new values, please disconnect then reconnect the robot',
                      'Plotting',
                      wx.OK | wx.ICON_INFORMATION)


class HistogramPlotManager(wx.Frame):
    def __init__(self, *args, **kw):
        super(HistogramPlotManager, self).__init__(*args, **kw)
        #craeting the GUI to plot histograms

        self.figure = Figure()
        self.ImageDisplay = self.figure.add_subplot(221,
                                                    title='Image preview',
                                                    xticks=[],
                                                    yticks=[])
        self.blueAxes = self.figure.add_subplot(222,
                                                title='Blue')
        self.greenAxes = self.figure.add_subplot(223,
                                                 title='Green')
        self.redAxes = self.figure.add_subplot(224,
                                               title='Red')

        self.canavas = FigureCanvasWxAgg(self, 1, self.figure)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canavas, 1, wx.LEFT | wx.TOP | wx.GROW)

        self.SetSizer(self.sizer)
        self.Fit()
        self.toolbar = NavigationToolbar2WxAgg(self.canavas)
        self.toolbar.Realize()
        tw, th = self.toolbar.GetSizeTuple()
        fw, fh = self.toolbar.GetSizeTuple()
        self.toolbar.SetSize(wx.Size(fw, th))
        self.sizer.Add(self.toolbar, 0, wx.LEFT | wx.EXPAND)
        self.toolbar.update()
        self.figure.tight_layout()
        self.figure.subplots_adjust()

    def plotHistograms(self, image):
    	#extracting histograms and plotting them
        self.ImageDisplay.imshow(image)
        self.blueAxes.hist(image[..., 2].flatten(), 256, range=(0, 250), fc='b')
        self.greenAxes.hist(image[..., 1].flatten(), 256, range=(0, 250), fc='g')
        self.redAxes.hist(image[..., 0].flatten(), 256, range=(0, 250), fc='r')


class LivePlotManager(wx.Frame):
	def __init__(self, *args, **kw):
		super(LivePlotManager, self).__init__(*args, **kw)
		#creating the GUI fo the live plot

		self.SetBackgroundColour(wx.NamedColour("WHITE"))
		self.figure = Figure()
		self.laxes = self.figure.add_subplot(311)
		self.taxes = self.figure.add_subplot(312)
		self.haxes = self.figure.add_subplot(313)


		self.canavas = FigureCanvasWxAgg(self,1, self.figure)
		self.sizer = wx.BoxSizer(wx.VERTICAL)
		self.sizer.Add(self.canavas, 1, wx.LEFT | wx.TOP | wx.GROW)
		self.SetSizer(self.sizer)
		self.Fit()
		self.toolbar = NavigationToolbar2WxAgg(self.canavas)
		self.toolbar.Realize()
		#for Mac OS:
		if wx.Platform == '__WXMAC__':
			self.SetToolbar(self.toolbar)

		else:
			#for Linux and Windows:
			tw, th = self.toolbar.GetSizeTuple()
			fw, fh = self.canavas.GetSizeTuple()
			self.toolbar.SetSize(wx.Size(fw, th))
			self.sizer.Add(self.toolbar, 0, wx.LEFT | wx.EXPAND)

		self.toolbar.update()

		self.Larray = [0]*20
		self.Harray = [0]*20
		self.Tarray = [0]*20
		
		self.X = xrange(20)
		
		self.plotTimer = wx.Timer(self)# a timer for the live plot
		self.Bind(wx.EVT_TIMER, self.onPlotTimer, self.plotTimer)
		self.plotTimer.Start(700)

	def plotLive(self):
		#a method to plot live data
		self.Larray.append(int(self.GetParent().light))
		self.Harray.append(int(self.GetParent().hum))
		self.Tarray.append(int(self.GetParent().temp))

		del self.Larray[0]
		del self.Harray[0]
		del self.Tarray[0]

		self.laxes.clear()
		self.haxes.clear()
		self.taxes.clear()

		self.laxes.plot(self.X, self.Larray, lw=2, color='y')
		self.haxes.plot(self.X, self.Harray, lw=2, color='b')
		self.taxes.plot(self.X, self.Tarray, lw=2, color='r')

		self.taxes.set_title('Temperature Live Plot')
		self.haxes.set_title('Humidity Live Plot')
		self.laxes.set_title('Light Live Plot')

		self.taxes.set_ylim([0,80])
		self.haxes.set_ylim([0,80])
		self.laxes.set_ylim([0, 110])

		self.laxes.grid()
		self.taxes.grid()
		self.haxes.grid()
		self.canavas.draw()
		
	def onPlotTimer(self, e):
		self.plotLive()




