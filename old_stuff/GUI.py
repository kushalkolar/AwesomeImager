import Tkinter
import LivePreview
import ImageStack


#USE PROCESS QUEUE AND IF QUEUE IS EMPTY DIPSLAY PREVIEW, ELSE QUEUE.get() AND APPLY THOSE VARS!

#SliderVal = Queue(maxsize=0)

#class PreviewWindow(threading.Thread):
#    def __init_(self):
    
class guiMain():
    def __init__(self):
        self.master = Tkinter.Tk()
        self.exposure = 0
        self.UpperLimitVar = 0
        self.LowerLimitVar = 0
        self.currFoc = 0.0

    def updateFoc(self, udFoc):
        self.currFoc = self.FocSlider.get()
        print self.currFoc
    def SetStepSize(self,stepsize):
        self.FocSlider.config(resolution=float(self.StepSizeSlider.get()))
        self.FocSlider.config(from_=35, to=-35)
        
    def updateExpos(self, udExp):
        self.currExpos = float(self.ExposSlider.get()) / 1000
        if self.PreviewButton.cget('text') == "Close Preview":
            self.ShowPreview.expos_time.put(self.currExpos)
        print self.currExpos

    def OpenPreview(self):
        self.PreviewButton.configure(text='Close Preview', bg='red', activebackground='orange red', 
            command=self.ClosePreview)
        currFoc = self.currFoc
        
        self.ShowPreview = LivePreview.Preview(currFoc, self.currExpos)
        self.ShowPreview.start()
        print 'Opening preview, Waveform type is: ' + self.StackPattern.cget('text')
        
    def ClosePreview(self):
        self.PreviewButton.configure(text='Show Preview', bg='lawn green', activebackground='green yellow', 
            command=self.OpenPreview)
        self.ShowPreview.endPreview()
        print 'Closing preview'
        
    def SetUpperLimit(self):
        self.UpperLimit.configure(text=self.currFoc)
        print 'Upper Limit is ' + str(self.UpperLimit.cget('text'))
        
    def SetLowerLimit(self):
        self.LowerLimit.configure(text=self.currFoc)
        
        
    def CheckPattern(self, option):
        if option == 'No Stacks':
            self.SetUpperButton['state'] = 'disabled'
            self.SetLowerButton['state'] = 'disabled'
            self.prevLowerLim = self.LowerLimit.cget('text')
            self.prevUpperLim = self.UpperLimit.cget('text')
            self.LowerLimit.configure(text='N/A')
            self.UpperLimit.configure(text='N/A')
            self.stacks_state = 0

        elif self.stacks_state==0:
            self.SetUpperButton['state'] = 'normal'
            self.SetLowerButton['state'] = 'normal'
            self.LowerLimit.configure(text=self.prevLowerLim)
            self.UpperLimit.configure(text=self.prevUpperLim)
            self.stacks_state=1
    def CheckTimeLapse(self):
        if self.CheckVar.get() == 1:
            self.MinsEntry['state'] = 'normal'
            self.SecsEntry['state'] = 'normal'
            
        elif self.CheckVar.get() == 0:
            self.MinsEntry['state'] = 'disabled'
            self.SecsEntry['state'] = 'disabled'
    def Acquisition(self):
        self.AcquireButton.configure(text='Stop Acquisition', bg='red', activebackground='orange red',
            command=self.StopAcquisition)
        if self.PreviewButton.cget('text') == 'Close Preview':
            self.ClosePreview()
        self.PreviewButton['state'] = 'disabled'
        acq_duration = int(self.SecsEntry.get()) + 60 * (int(self.MinsEntry.get()))
        focal_start = 1
        focal_interval = 0.1
        saveDir ='D:\Awesome_Imager_testing2'
        
        WriteImages = ImageStack.ImageWriter(saveDir)
        Acquire = ImageStack.GetNextFrame(acq_duration, self.currExpos, focal_start, focal_interval)
        
        Acquire.start()
        WriteImages.start()
                    
        self.StopAcquisition()
            
    def StopAcquisition(self):
        self.AcquireButton.configure(text='Acquire', bg='dark turquoise', activebackground='turquoise',
            command=self.Acquisition)
        self.PreviewButton['state'] = 'normal'
        
        
    def main(self):
    # These below are the sliders
        self.FocSlider = Tkinter.Scale(self.master,from_=35, to=-35, orient=Tkinter.VERTICAL, sliderlength=10,
            label='Focal Length', length=150, command=self.updateFoc)
        self.FocSlider.grid(row=1, column=1)
        self.FocSlider.set(0)
        
        self.StepSizeSlider = Tkinter.Scale(self.master, from_=1, to=30, orient=Tkinter.HORIZONTAL, sliderlength = 10, 
            resolution=1, label="Step Size", length = 75, command=self.SetStepSize)
        self.StepSizeSlider.grid(row=2, column=1)
        self.StepSizeSlider.set(1)
        
        self.SetUpperButton = Tkinter.Button(self.master, text='Set Upper Limit', command=self.SetUpperLimit)
        self.SetUpperButton.grid(row=0, column=0, stick='S')
        
        self.UpperLimit = Tkinter.Label(self.master, text=0.0)
        self.UpperLimit.grid(row=1, column=0, stick='N')
        
        self.stacks_state = 1
        PatternList = ('Sawtooth Wave Stacks', 'Sine Wave Stacks', 'Triangle Wave Stacks', 'No Stacks')
        self.PatternListVar = Tkinter.StringVar()
        self.PatternListVar.set(PatternList[0])
        self.StackPattern = Tkinter.OptionMenu(self.master, self.PatternListVar, *PatternList, command=self.CheckPattern)
        self.StackPattern.grid(row=1,column=0, stick='E')
        
        
        self.LowerLimit = Tkinter.Label(self.master, text=0.0)
        self.LowerLimit.grid(row=1, column=0, stick = 'S')
        
        self.SetLowerButton = Tkinter.Button(self.master, text='Set Lower Limit', command=self.SetLowerLimit)
        self.SetLowerButton.grid(row=2, column=0, stick='N')
        
            
        self.ExposSlider = Tkinter.Scale(self.master, from_=1, to=500, orient=Tkinter.HORIZONTAL, sliderlength=10,
            length=200, label='Exposure', variable=self.exposure)
        self.ExposSlider.bind("<ButtonRelease-1>", self.updateExpos)
        self.ExposSlider.grid(row=3, column=0)
        self.ExposSlider.set(50)
        self.currExpos = 0.05
        
        self.CheckVar = Tkinter.IntVar()
        self.CheckVar.set(0)
        self.TimeLapseCheck = Tkinter.Checkbutton(self.master, variable=self.CheckVar, command=self.CheckTimeLapse)
        self.TimeLapseCheck.grid(row=4,column=0)
        
        self.TimeLapseLabel = Tkinter.Label(self.master, text='  Timelapse')
        self.TimeLapseLabel.grid(row=4,column=0,sticky='W')
        
        self.MinsEntry = Tkinter.Entry(self.master, width=10)
        self.MinsEntry['state'] = 'disabled'
        self.MinsEntry.grid(row=5, column=0)
        
        self.MinsLabel = Tkinter.Label(self.master, text='mins:')
        self.MinsLabel.grid(row=5, column=0, stick='W')
        
        self.SecsEntry = Tkinter.Entry(self.master, width=10)
        self.SecsEntry['state'] = 'disabled'
        self.SecsEntry.grid(row=6, column=0)
        
        self.SecsLabel = Tkinter.Label(self.master, text='secs:')
        self.SecsLabel.grid(row=6, column=0, stick='W')
        
        
        self.PreviewButton = Tkinter.Button(self.master, text='Show Preview', bg='lawn green', 
            activebackground='green yellow', command=self.OpenPreview)
        self.PreviewButton.grid(row=3, column=1)
        
        self.AcquireButton = Tkinter.Button(self.master, text='Acquire', bg='dark turquoise', 
            activebackground='turquoise', command=self.Acquisition)
        self.AcquireButton.grid(row=4, column=1)
            
        Tkinter.mainloop()
        
gui = guiMain()
gui.main()


#print gui.FocLenSlider.getvar()


#cam_ID = 0
#acq_duration = 10.0
#expos_time = 1.0
#focal_start = 1
#focal_interval = 0.1
#saveDir ='./tmp_images/'
#WriteImages = ImageStack.ImageWriter(saveDir)
#Acquire = ImageStack.GetNextFrame(cam_ID, acq_duration, expos_time, focal_start, focal_interval)
#
#Acquire.start()
#WriteImages.start()
#WriteImages.join()
#Acquire.join()