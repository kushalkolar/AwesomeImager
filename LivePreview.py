import cv2
import numpy as np
import time
import threading
import hamamatsu_camera as hc
from Queue import Queue
import pyqtgraph as pg

#TRY TO REPLACE THREADING WITH PROCESS: http://stackoverflow.com/questions/323972/is-there-any-way-to-kill-a-thread-in-python


class Preview(threading.Thread):
    def __init__(self, currFoc, first_expos):
        threading.Thread.__init__(self)
        print " ----------- Starting Preview thread ------------- "
        print "--> Initializing Camera Parameters"
        self.hcam = hc.HamamatsuCameraMR(0)
# Set camera parameters.
        cam_offset = 100
        cam_x = 2048
        cam_y = 2048
#        self.expos_time = Queue(maxsize=0)
        self.hcam.setPropertyValue("defect_correct_mode", "OFF")
        self.hcam.setPropertyValue("exposure_time", first_expos)
        self.hcam.setPropertyValue("subarray_hsize", cam_x)
        self.hcam.setPropertyValue("subarray_vsize", cam_y)
        self.hcam.setPropertyValue("binning", "1x1")
        self.hcam.setPropertyValue("readout_speed", 2)
        self.show = True
        
        self.iv = pg.imageview.ImageView()
        
        colors = [
                (0, 0, 0),
                (7, 0, 220),
                (236, 0, 134),
                (246, 246, 0),
                (255, 255, 255),
                (0, 255, 0)
                ]
#        
        cmap = pg.ColorMap(pos=np.linspace(0.0, 1.0, 6), color=colors)
        self.iv.setColorMap(cmap)
        self.iv.setLevels(0,65535)
        self.hist = self.iv.getHistogramWidget()
        self.hist.vb.enableAutoRange(self.hist.vb.YAxis, False)
        self.iv.show()


    def run(self):
        #global KillPreview
        self.hcam.startAcquisition()
        first_img = True
        #try:
        while self.show == True:
#            if self.expos_time.qsize() > 0:
#                self.hcam.setPropertyValue("exposure_time", self.expos_time.get())
#           self.lens.focalpower( <<appropriate focal power>> )
            
            # This puts the frame into the Queue, and another thread takes care of it 
            # so that the program proceeds as fast as possible to the next step
            
            # << Modulo calculation to find the next focal power to adjust to according to focal_interval >>
            
            #time.sleep(0.014) # Wait 14ms for the lens to adjust to the right focal power
         
            # <<** might be possible to lower this time because of small stack intervals 
            # and use larger wait times only when beginning the next stack!! ** >>
            [frame, dims] = self.hcam.getFrames() # Grab the frame from the camera
            
            try:
                grey_values = frame[0].getData()
#                start = time.clock()
                img = np.reshape(grey_values, (2048, 2048))
#                img = (img/255).astype(np.uint8)
                self.iv.setImage(img, autoRange=False, autoLevels=False, autoHistogramRange=False)
                
                if first_img:
                    self.iv.autoLevels()
                    first_img = False
                self.levels = self.hist.getLevels()
                # img = cv2.equalizeHist((img/255).astype(np.uint8))
#                if self.brightness != 0:
#                    try:
#                        np.add(img, self.brightness, img)
#                    except:
#                        pass
#                    
##                img = self.adjust_gamma(img)
##                img = self.adjust_contrast(img)
#
#                cv2.namedWindow('Preview Window', cv2.WINDOW_NORMAL)
#                cv2.resizeWindow('Preview Window', 1000, 1000)
#                cv2.imshow('Preview Window', img)
#                if cv2.waitKey(1) & 0xFF == ord('q'): 
#                    self.show = False
#                stop = time.clock()
#                print stop - start
            except Exception as e:
                print e
        self.hcam.stopAcquisition()
        self.hcam.shutdown()

#           self.lens.close(soft_close=True)
        #except:
            #self.hcam.stopAcquisition()
            #self.hcam.shutdown()
            #print 'Something went wrong with showing the preview window'
            
    def endPreview(self): 
        self.show = False

if __name__ == "__main__":
    #KillPreview = False
    first_expos = 0.01
    currFoc = 0
    ShowPreview = Preview(currFoc, first_expos)
    ShowPreview.start()
    #ShowPreview.join()