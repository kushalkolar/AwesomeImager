import cv2
import numpy as np
import time
import threading
import hamamatsu_camera as hc
from Queue import Queue

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
        self.expos_time = Queue(maxsize=0)
        self.hcam.setPropertyValue("defect_correct_mode", "OFF")
        self.hcam.setPropertyValue("exposure_time", first_expos)
        self.hcam.setPropertyValue("subarray_hsize", cam_x)
        self.hcam.setPropertyValue("subarray_vsize", cam_y)
        self.hcam.setPropertyValue("binning", "1x1")
        self.hcam.setPropertyValue("readout_speed", 2)
        self.show = True
        
    def run(self):
        #global KillPreview
        self.hcam.startAcquisition()
        #try:
        while self.show == True:
            if self.expos_time.qsize() > 0:
                self.hcam.setPropertyValue("exposure_time", self.expos_time.get())
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
                start = time.clock()
                img = np.reshape(grey_values, (2048, 2048))
                cv2.namedWindow('Preview Window', cv2.WINDOW_NORMAL)
                cv2.resizeWindow('Preview Window', 1000, 1000)
                cv2.imshow('Preview Window', img)
                if cv2.waitKey(1) & 0xFF == ord('q'): 
                    self.show = False
                stop = time.clock()
                print stop - start
            except:
                pass
        cv2.destroyAllWindows()
        self.hcam.stopAcquisition()
        self.hcam.shutdown()
        

#           self.lens.close(soft_close=True)
        #except:
            #self.hcam.stopAcquisition()
            #self.hcam.shutdown()
            #print 'Something went wrong with showing the preview window'
    def endPreview(self): 
        cv2.destroyAllWindows()
        self.show = False
        
if __name__ == "__main__":
    #KillPreview = False
    first_expos = 0.01
    currFoc = 0
    ShowPreview = Preview(currFoc, first_expos)
    ShowPreview.start()
    #ShowPreview.join()