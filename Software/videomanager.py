__author__ = 'HAMZA BOUGHRAIRA'

""" this file contains four classes to manage video
the VideoManager class reads frames from the camera and apply the appropriate effects on them 
the VideoRecorder class to record the video
the Snapshot class to take a snapshot
the VideoEditor class to prompt the user to use an effect to apply on the video"""

import cv2 #OpenCV
import wx #wxPython

class VideoManager(wx.Panel):
    def __init__(self, parent, capture, fps):
        super(VideoManager, self).__init__(parent)
        self.capture = capture
        self.fps = fps
        self.parent = parent
        self.timer = wx.Timer(self)


        ret, frame = self.capture.read()
        self.height, self.width = frame.shape[:2] #extracting the width and the height of the original frame
        """ NOTE: OpenCV reads video frames in the BGR format, to display the video we need to convert the colorspace
        		from BGR to RGB"""
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #convert
        self.buffer = wx.BitmapFromBuffer(self.width, self.height, frame) #a buffer to help the static bitmap displaying the video

    def nextframe(self, effect):

    	"""method to read frames and apply effects 
    	NOTE; effect here are based on chaging the colorspaces of a frame"""
        ret, self.orig_frame = self.capture.read()
        if ret:
            if effect == 'original':
                self.frame = cv2.cvtColor(self.orig_frame, cv2.COLOR_BGR2RGB)
                self.buffer.CopyFromBuffer(self.frame)

            elif effect == 'ubuntu':
                self.frame = cv2.cvtColor(self.orig_frame, cv2.COLOR_BGR2LAB)
                self.buffer.CopyFromBuffer(self.frame)

            elif effect == 'fedora':
                self.frame = cv2.cvtColor(self.orig_frame, cv2.COLOR_BGR2XYZ)
                self.buffer.CopyFromBuffer(self.frame)

            elif effect == 'suse':
                self.frame = cv2.cvtColor(self.orig_frame, cv2.COLOR_BGR2HLS)
                self.buffer.CopyFromBuffer(self.frame)

            elif effect == 'arch':
                self.frame = cv2.cvtColor(self.orig_frame, cv2.COLOR_BGR2LUV)
                self.buffer.CopyFromBuffer(self.frame)

            elif effect == 'debian':
                self.frame = cv2.cvtColor(self.orig_frame, cv2.COLOR_BGR2HSV)
                self.buffer.CopyFromBuffer(self.frame)

            else:
                pass


class Snapshot(wx.Dialog):
    def __init__(self, parent):
        super(Snapshot, self).__init__(parent)

        #a filedialog to extract the saving path
        fd = wx.FileDialog(self, "Chose a directory for the snapshot",
                           "",
                           "",
                           "JPG files(*.jpg)",
                           wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)

        if fd.ShowModal() == wx.ID_OK:
            self.savepath = fd.GetPath()
        try:
            if self.savepath[:-4].lower() != '.jpg':
                self.savepath += '.jpg'
        except AttributeError:
            pass

        cv2.imwrite(self.savepath, self.GetParent().manager.orig_frame)#taking snapshot
        self.EndModal(wx.SAVE)


class VideoRecorder(wx.Dialog):
    def __init__(self, parent):
        super(VideoRecorder, self).__init__(parent)
        fd = wx.FileDialog(self, "Chose a directory for the video", "", "", "AVI files(*.avi)",
                           wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)

        if fd.ShowModal() == wx.ID_OK:
            self.savepath = fd.GetPath()

        try:
            if self.savepath[:-4].lower() != '.avi':
                self.savepath += '.avi'
        except AttributeError:
            pass

        """the openCV's videowriter(output: .AVI video)  """  	
        self.output = cv2.VideoWriter(self.savepath, cv2.cv.CV_FOURCC('I', '4', '2', '0'), self.GetParent().manager.fps,
                                      (640, 480))
        self.EndModal(wx.SAVE)

    def startrecording(self):

        self.output.write(self.GetParent().manager.orig_frame)


class VideoEditor(wx.Dialog):
    def __init__(self, parent):
        super(VideoEditor, self).__init__(parent, title='Video Editor', size=(500,200))

        self.effect = self.GetParent().videoeffect#get the original effect
        self.returnVal = None

        #the GUI for the editor dialog
        pnl = wx.Panel(self)
        text = wx.StaticText(pnl, label='CHOOSE YOUR EFFECT')
        line = wx.StaticLine(pnl, size=(400, 1))

        self.ubuntu = wx.RadioButton(pnl, label='Ubuntu Effect', style=wx.RB_GROUP)
        self.original = wx.RadioButton(pnl, label='Original')
        self.suse = wx.RadioButton(pnl, label='openSUSE Effect')
        self.arch = wx.RadioButton(pnl, label='Arch Effect')
        self.debian = wx.RadioButton(pnl, label='Debian Effect')
        self.fedora = wx.RadioButton(pnl, label='Fesora Effect')

        okButton = wx.Button(pnl, label='OK')
        cancelButton = wx.Button(pnl, label='Cancel')

        vsizer = wx.BoxSizer(wx.VERTICAL)
        vsizer.Add(text, 0, wx.TOP | wx.ALIGN_CENTER_HORIZONTAL, 10)

        gsizer = wx.GridSizer(2, 3, 10, 10)
        gsizer.AddMany([(self.ubuntu, 0, wx.EXPAND),
                        (self.original, 0, wx.EXPAND),
                        (self.suse, 0, wx.EXPAND),
                        (self.arch, 0, wx.EXPAND),
                        (self.debian, 0, wx.EXPAND),
                        (self.fedora, 0, wx.EXPAND)])

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(cancelButton, 0, wx.ALIGN_RIGHT | wx.RIGHT, 10)
        hsizer.Add(okButton, 0, wx.RIGHT, 10)

        vsizer.Add(gsizer, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, 30)
        vsizer.Add(line, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, 20)
        vsizer.Add(hsizer, 0, wx.ALIGN_RIGHT | wx.TOP, 20)

        pnl.SetSizer(vsizer)

        self.ubuntu.Bind(wx.EVT_RADIOBUTTON, self.onRadio)
        self.original.Bind(wx.EVT_RADIOBUTTON, self.onRadio)
        self.suse.Bind(wx.EVT_RADIOBUTTON, self.onRadio)
        self.arch.Bind(wx.EVT_RADIOBUTTON, self.onRadio)
        self.debian.Bind(wx.EVT_RADIOBUTTON, self.onRadio)
        self.fedora.Bind(wx.EVT_RADIOBUTTON, self.onRadio)


        okButton.Bind(wx.EVT_BUTTON, self.onOk)
        cancelButton.Bind(wx.EVT_BUTTON, self.onCancel)


    def onRadio(self, e):
    	#method to extract effect from the radiobutton widgets
        if self.ubuntu.GetValue() == True:
            self.returnVal = 'ubuntu'

        elif self.original.GetValue() == True:
            self.returnVal = 'original'

        elif self.suse.GetValue() == True:
            self.returnVal = 'suse'

        elif self.arch.GetValue() == True:
            self.returnVal = 'arch'

        elif self.debian.GetValue() == True:
            self.returnVal = 'debian'

        elif self.fedora.GetValue() == True:
            self.returnVal = 'fedora'


    def onOk(self, e):
        self.effect = self.returnVal
        print 'the %s effect'% self.effect
        self.Destroy()

    def onCancel(self, e):
        self.Destroy()

