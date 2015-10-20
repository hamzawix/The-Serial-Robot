__author__ = 'HAMZA BOUGHRAIRA'

""" this file contains one class that allows us to examin the serial communication over the USB port"""

from serial import Serial, serialutil #the Serial class and the serialutil to handle connection errors
from wx import MessageBox, OK, ICON_ERROR, ICON_EXCLAMATION #GUI classes from wxPython

class Arduino(object):
    def __init__(self, baud):
        self.baudrate = baud 
        self.arduino = None

    def connect(self):
    	""" if you are on windows:
    		change the port parameter to the windows's COM por(ex: COM1)
    		if you are on MAC OSx:
    		change the port parameter to the one suitable with the mac(ex: /dev/cu.usbmodemfa1321)
    		"""
        try:
            self.arduino = Serial(port='/dev/ttyACM0', baudrate=self.baudrate)

        except serialutil.SerialException:
            try:
                self.arduino = Serial(port='/dev/ttyACM1', baudrate=self.baudrate)
            except serialutil.SerialException:
                try:
                    self.arduino = Serial(port='/dev/ttyACM2', baudrate=self.baudrate)
                except serialutil.SerialException:
                    self.arduino = False
                    MessageBox('Sorry! No devices found. \n '
                               'Check your connections again',
                               'Connection Error',
                               OK | ICON_ERROR)

    def isconnected(self):
    	#connection check
        if self.arduino is None:
            return False
        elif self.arduino is False:
            return False
        else:
            return True

    def isdisconnected(self):
    	#disconnection check
        return not self.arduino.isOpen()

    def send(self, data):
    	#data sending
        if self.isconnected() and not self.isdisconnected():
            self.arduino.write(data)
        else:
            MessageBox('Robot not connected!!! \n'
                       'Try to connect it first',
                       'Sending Error',
                       OK | ICON_EXCLAMATION)

    def disconnect(self):
        self.arduino.close()

    def getdata(self):
        if self.isconnected():
            return self.arduino.readline()

        else:
            return

    def Flush(self):
    	#to clear the serial buffer
        self.arduino.flushInput()

    def waiting(self):
        return self.arduino.inWaiting()
