#!/usr/bin/env python
__author__ = 'HAMZA BOUGHRAIRA'

"""
This is the python file that you might run 
it contains one class for our main(parent) window
the GUI library used here is wxPython
"""

import wx #wxPython
from wx.lib import statbmp #a static bitmap for the video
import csv # the CSV module to store and read data from a CSV file
import cv2 # the popular computer vision library OpenCV
from serialmanager import Arduino #a class to handle the serial communication (see serialmanager.py) 
from plotmanager import Plotmanager, HistogramPlotManager, LivePlotManager # three classes to do everything related to plotting(see plotmanager.py)
from videomanager import VideoManager, Snapshot, VideoRecorder, VideoEditor #four classes to manage video (see videomanager.py)

class MainWindow(wx.Frame): # our main class
    def __init__(self):
        super(MainWindow, self).__init__(parent=None, title='THE SERIAL ROBOT')

        self.timer = wx.Timer(self, 1) # timer for data acquisition
        self.timer2 = wx.Timer(self) # timer for video acquisition
        self.initGUI() # the GUI
        self.port = Arduino(9600) #9600bps(bits per second)
        self.videoeffect = 'original'# the original effect of the video
        self.SetMinSize((1000, 680))
        self.Show(True)
        self.Center()

    def initGUI(self): # the GUI

        # sizers
        self.Vpnl = wx.Panel(self, size=(635, 475))
        self.Vpnl.SetBackgroundColour(wx.BLACK)
        pnl = wx.Panel(self)
        pnl1 = wx.Panel(self)
        vbox1 = wx.BoxSizer(wx.VERTICAL)
        vbox2 = wx.BoxSizer(wx.VERTICAL)
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox3 = wx.BoxSizer(wx.VERTICAL)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        grid1 = wx.GridSizer(3, 3, 5, 5)
        grid2 = wx.GridSizer(2, 2, 20, 10)
        grid3 = wx.GridSizer(1, 3, 5, 5)

        # widgets
        frwd = wx.BitmapButton(pnl, bitmap=wx.Bitmap('Icons/forward.png'))
        back = wx.BitmapButton(pnl, bitmap=wx.Bitmap('Icons/beckward.png'))
        stop = wx.BitmapButton(pnl, bitmap=wx.Bitmap('Icons/stop1.png'))
        left = wx.BitmapButton(pnl, bitmap=wx.Bitmap('Icons/left.png'))
        right = wx.BitmapButton(pnl, bitmap=wx.Bitmap('Icons/right.png'))
        self.connectbutton = wx.Button(pnl1, label='Connect', size=(100, 30))
        self.disconnectbutton = wx.Button(pnl1, label='Disconnect', size=(100, 30))

        camRight = wx.BitmapButton(pnl, bitmap=wx.Bitmap('Icons/camright.png'))
        camLeft = wx.BitmapButton(pnl, bitmap=wx.Bitmap('Icons/camleft.png'))
        camStop = wx.BitmapButton(pnl, bitmap=wx.Bitmap('Icons/camstop.png'))

        robotMovement = wx.StaticText(pnl, label='Robot Movement Control')
        camMovement = wx.StaticText(pnl, label='Camera Rotation Control')

        self.Temp = wx.StaticText(pnl1, label='Temp')
        self.Hum = wx.StaticText(pnl1, label='Humidity')
        self.Light = wx.StaticText(pnl1, label='Light')
        self.getWeather = wx.Button(pnl1, label='show weather plots')
        self.getLiveWeather = wx.Button(pnl1, label='show live weather plots')

        self.recordButton = wx.ToggleButton(pnl1, label='Record')
        self.snapButton = wx.Button(pnl1, label='Snapshot')
        self.editbutton = wx.Button(pnl1, label='Edit')
        self.histogrambutton = wx.Button(pnl1, label='Show Histograms')

        hLine = wx.StaticLine(pnl1, size=(650, 1), style=wx.LI_HORIZONTAL)

        weather = wx.StaticBox(pnl1, label='weather', size=(170, 110))
        video = wx.StaticBox(pnl1, label='video', size=(200, 110))
        Svbox1 = wx.StaticBoxSizer(weather, orient=wx.VERTICAL)
        Svbox2 = wx.StaticBoxSizer(video, orient=wx.VERTICAL)

        self.SB = self.CreateStatusBar(3)
        self.SB.SetStatusText('Robot Status:', 0)
        self.SB.SetStatusText('Camera Status:', 1)
        self.SB.SetStatusText('Connection Status: Disconnected', 2)
        self.SB.SetBackgroundColour('#FA0015')

        # putting widgets into sizers:
        grid1.AddMany([(wx.StaticText(self), 0, wx.EXPAND),
                      (frwd, 0, wx.EXPAND),
                      (wx.StaticText(self), 0, wx.EXPAND),
                      (left, 0, wx.EXPAND),
                      (stop, 0, wx.EXPAND),
                      (right, 0, wx.EXPAND),
                      (wx.StaticText(self), 0, wx.EXPAND),
                      (back, 0, wx.EXPAND),
                      (wx.StaticText(self), 0, wx.EXPAND)])

        grid3.AddMany([(camLeft, 0, wx.EXPAND),
                       (camStop, 0, wx.EXPAND),
                       (camRight, 0, wx.EXPAND)])

        vbox2.AddMany([(robotMovement, 0, wx.TOP | wx.ALIGN_CENTER_HORIZONTAL, 20),
                       (grid1, 0, wx.TOP, 15),
                       (camMovement, 0, wx.TOP | wx.ALIGN_CENTER_HORIZONTAL, 40),
                       (grid3, 0, wx.TOP, 15)])

        Svbox1.AddMany([(self.Temp, 0, wx.EXPAND),
                        (self.Hum, 0, wx.EXPAND),
                        (self.Light, 0, wx.EXPAND),
                        (self.getWeather, 0, wx.EXPAND),
                        (self.getLiveWeather, 0, wx.EXPAND)])

        grid2.AddMany([(self.editbutton, 0, wx.EXPAND),
                       (self.recordButton, 0, wx.EXPAND),
                       (self.histogrambutton, 0, wx.EXPAND),
                       (self.snapButton, 0, wx.EXPAND)])

        Svbox2.Add(grid2, flag=wx.EXPAND)

        vbox1.Add(self.connectbutton, proportion=0, flag=wx.BOTTOM | wx.ALIGN_CENTER_HORIZONTAL, border=10)
        vbox1.Add(self.disconnectbutton, proportion=0, flag=wx.ALIGN_CENTER_HORIZONTAL)


        hbox2.Add(Svbox2, proportion=0, flag=wx.RIGHT, border=40)
        hbox2.Add(Svbox1, proportion=0, flag=wx.RIGHT, border=40)
        hbox2.Add(vbox1, proportion=0, flag=wx.ALIGN_CENTER_VERTICAL)
        vbox3.Add(hLine, proportion=0, flag=wx.BOTTOM, border=5)
        vbox3.Add(hbox2, proportion=0, flag=wx.CENTER)
        pnl1.SetSizer(vbox3)

        hbox3.Add(self.Vpnl, proportion=1, flag=wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, border=50)
        pnl.SetSizer(vbox2)
        hbox3.Add(pnl, proportion=0)

        vbox.Add(hbox3, proportion=0, flag=wx.TOP | wx.ALIGN_CENTER_HORIZONTAL, border=20)
        vbox.Add(pnl1, proportion=1, flag=wx.TOP | wx.LEFT | wx.RIGHT | wx.ALIGN_CENTER_HORIZONTAL, border=20)

        self.SetSizer(vbox)

        # Menus:
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        filetem = fileMenu.Append(wx.ID_EXIT, 'Quit', 'quit application')
        menubar.Append(fileMenu, '&File')
        aboutMenu = wx.Menu()
        aboutitem = aboutMenu.Append(wx.ID_ABOUT, 'About the app', 'About the application')
        menubar.Append(aboutMenu, '&Help')
        self.SetMenuBar(menubar)
        self.Bind(wx.EVT_MENU, self.onclose, filetem)
        self.Bind(wx.EVT_CLOSE, self.onclose)
        self.Bind(wx.EVT_MENU, self.onabout, aboutitem)

    # events:
        frwd.Bind(wx.EVT_BUTTON, self.onforward)
        back.Bind(wx.EVT_BUTTON, self.onbackward)
        stop.Bind(wx.EVT_BUTTON, self.onstop)
        right.Bind(wx.EVT_BUTTON, self.onright)
        left.Bind(wx.EVT_BUTTON, self.onleft)
        camRight.Bind(wx.EVT_BUTTON, self.oncamright)
        camStop.Bind(wx.EVT_BUTTON, self.oncamstop)
        camLeft.Bind(wx.EVT_BUTTON, self.oncamleft)
        self.getWeather.Bind(wx.EVT_BUTTON, self.plots)
        self.getLiveWeather.Bind(wx.EVT_BUTTON, self.Liveplots)
        self.snapButton.Bind(wx.EVT_BUTTON, self.onsnapshot)
        self.recordButton.Bind(wx.EVT_TOGGLEBUTTON, self.onrecord)
        self.histogrambutton.Bind(wx.EVT_BUTTON, self.onHistogram)
        self.editbutton.Bind(wx.EVT_BUTTON, self.onEdit)
        self.connectbutton.Bind(wx.EVT_BUTTON, self.onconnect)
        self.disconnectbutton.Bind(wx.EVT_BUTTON, self.disconnect)
        self.disconnectbutton.Disable()
        self.getLiveWeather.Disable()
        self.getWeather.Disable()
        self.histogrambutton.Disable()
        self.recordButton.Disable()
        self.snapButton.Disable()
        self.editbutton.Disable()

    # event handlers:
    def ontimer(self, e):
            try:
                datastring = str(self.port.getdata())  #data from the robot
                data = datastring.split(';')
                self.hum = data[0]
                self.temp = data[1]
                self.light = data[2]
                self.count += 1

            except:
                return

            if self.count > 5:
                try:
                	#beginnig the data writing in the CSV after five seconds of connecting
                    row = [self.i, self.temp, self.hum, self.light]
                    self.writer.writerow(row)
                    self.i += 1
                except ValueError:
                    return

            try:
            	#displaying data in text widgets
                self.Hum.SetLabel(('Humidity................%s%s' % (self.hum, '%')))
                self.Temp.SetLabel('Temperature..........%sC' % self.temp)
                self.Light.SetLabel('Light.......................%s%s' % (self.light, '%'))
                self.port.Flush()
            except:
                return

    def ontimertwo(self, e):
    	#displaying video
        self.manager.nextframe(self.videoeffect)
        self.image = statbmp.GenStaticBitmap(self.Vpnl, wx.ID_ANY, self.manager.buffer)

    def ontimer3(self, e):
    	#recording + displaying video
        self.manager.nextframe(self.videoeffect)
        self.image = statbmp.GenStaticBitmap(self.Vpnl, wx.ID_ANY, self.manager.buffer)
        self.recorder.startrecording()

    def onconnect(self, e):
    	#when the connect button pressed
        self.port.connect()
        if self.port.isconnected():
            try:
                self.capture = cv2.VideoCapture(0)
                self.manager = VideoManager(None, self.capture, 8)
            except:
                pass
            self.image = statbmp.GenStaticBitmap(self.Vpnl, wx.ID_ANY, self.manager.buffer)
            self.timer.Start(1000)
            self.timer2.Start(1000/self.manager.fps)
            self.Bind(wx.EVT_TIMER, self.ontimertwo)
            self.count = 0
            self.Bind(wx.EVT_TIMER, self.ontimer, self.timer)
            self.SB.SetBackgroundColour('#26FCAC')
            self.SB.SetStatusText('Connection Status: Connected', 2)
            #creating the CSV file
            self.tab = open('Values/values.csv', 'w')
            self.writer = csv.writer(self.tab)
            head = ['i', 'Temperature', 'Humidity', 'Light']
            self.writer.writerow(head)
            self.i = 1
            self.connectbutton.Disable()
            self.disconnectbutton.Enable()
            self.getLiveWeather.Enable()
            self.getWeather.Enable()
            self.histogrambutton.Enable()
            self.recordButton.Enable()
            self.snapButton.Enable()
            self.editbutton.Enable()


    def disconnect(self, e):
    	#when disconnect pressed
        self.port.disconnect()
        if self.port.isdisconnected():
            self.timer.Stop()
            self.timer2.Stop()
            self.capture.release()
            self.SB.SetBackgroundColour('#FA0015')
            self.SB.SetStatusText('Connection Status: Disconnected', 2)
            self.connectbutton.Enable()
            self.disconnectbutton.Disable()
            self.getLiveWeather.Disable()
            self.getWeather.Disable()
            self.histogrambutton.Disable()
            self.recordButton.Disable()
            self.snapButton.Disable()
            self.editbutton.Disable()


    def plots(self, e):
    	#the static plot
        self.timer.Stop()
        self.tab.close()
        staticplot = Plotmanager(self, -1, 'the plot')
        staticplot.SetSize((1000, 550))
        self.Disable()
        staticplot.maketheplot('Values/values.csv')
        staticplot.Show(True)

    def onHistogram(self, e):
    	#the histogram plot
        histogram = HistogramPlotManager(self, title='Histogram plots')
        histogram.SetSize((1000, 600))
        histogram.plotHistograms(self.manager.frame)
        histogram.Show(True)    


    def Liveplots(self, e):
    	#the live plot(real time)
    	live = LivePlotManager(parent=self, title='Live weather plot')
    	live.SetSize((700, 750))
    	live.Show(True)  	


    def onEdit(self, e):
    	#when edit pressed
    	dialog = VideoEditor(self)
    	dialog.ShowModal()
    	self.videoeffect = dialog.effect

    def onforward(self, e):
        self.timer.Stop()
        self.port.send('f')
        self.timer.Start()
        if self.port.isconnected():
            self.SB.SetStatusText('Robot Status: moving forward', 0)

    def onbackward(self, e):
        self.port.send('b')
        if self.port.isconnected():
            self.SB.SetStatusText('Robot Status: moving backward', 0)

    def onstop(self, e):
        self.port.send('s')
        if self.port.isconnected():
            self.SB.SetStatusText('Robot Status: stopped', 0)

    def onright(self, e):
        self.port.send('r')
        if self.port.isconnected():
            self.SB.SetStatusText('Robot Status: turning right', 0)

    def onleft(self, e):
        self.port.send('l')
        if self.port.isconnected():
            self.SB.SetStatusText('Robot Status: turning left ', 0)

    def oncamright(self, e):
        self.timer.Stop()
        self.port.send('1')
        self.timer.Start()
        if self.port.isconnected():
            self.SB.SetStatusText('Camera Status: 90 degrees right', 1)

    def oncamstop(self, e):
        self.timer.Stop()
        self.port.send('0')
        self.timer.Start()
        if self.port.isconnected():
            self.SB.SetStatusText('Camera Status: middle(0 degrees)', 1)

    def oncamleft(self, e):
        self.timer.Stop()
        self.port.send('2')
        self.timer.Start()
        if self.port.isconnected():
            self.SB.SetStatusText('Camera Status: 90 degrees left', 1)

    def onsnapshot(self, e):
    	#when snapshot pressed
        try:
            modal = Snapshot(self)
            self.timer2.Stop()
            self.timer.Stop()
        except AttributeError:
            pass
        try:
            modal.Destroy()
        except UnboundLocalError:
            pass
        if self.port.isconnected():
            self.timer2.Start(1000/self.manager.fps)
            self.timer.Start(1000)
        else:
            pass

    def onrecord(self, e):
    	#when record pressed
        obj = e.GetEventObject()
        isPressed = obj.GetValue()

        if isPressed:
            if self.timer2.IsRunning():
                self.timer2.Stop()
                self.recorder = VideoRecorder(self)

                self.timer3 = wx.Timer(self)
                self.timer3.Start(1000/self.manager.fps)
                self.Bind(wx.EVT_TIMER, self.ontimer3)
                self.recordButton.SetLabel('Stop')


        else:
            self.timer3.Stop()
            self.timer2.Start()
            self.recordButton.SetLabel('Record')



    def onclose(self, e):
        dial = wx.MessageDialog(None, 'Are you sure you want to quit?', 'Exit', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        ret = dial.ShowModal()
        if ret == wx.ID_YES:
            try:
                self.timer.Stop()
                self.timer2.Stop()
                self.capture.release()
                self.Destroy()
            except AttributeError:
                self.Destroy()

    @staticmethod
    def onabout(e):
    	#the about dialog
        txtpath = 'About/Description.txt'
        licensepath = 'About/Licence.txt'
        iconpath = 'About/robot.png'
        with open(txtpath, 'r') as f:
            desc = f.read()

        with open(licensepath, 'r') as l:
        	license = l.read()

        info = wx.AboutDialogInfo()
        info.SetDescription(desc)
        info.SetLicense(license)
        info.SetName('THE SERIAL ROBOT')
        info.SetVersion('2.0')
        info.SetIcon(wx.Icon(iconpath, wx.BITMAP_TYPE_PNG))
        info.SetCopyright('(c)-2015 Hamza Boughraira')
        info.AddDeveloper('Hamza Boughraira')

        wx.AboutBox(info)

# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

def Main():
		#our root app
        root = wx.App()
        MainWindow()
        root.MainLoop()
if __name__ == '__main__':
    Main()
