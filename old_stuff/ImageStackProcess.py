import threading
import time
from Queue import Queue
import cv2 # Import OpenCV2
#from opto import Opto # Import modules provided by optotune
import hamamatsu_camera as hc
import os
import numpy as np

import multiprocessing

#TRY TO REPLACE THREADING WITH PROCESS: http://stackoverflow.com/questions/323972/is-there-any-way-to-kill-a-thread-in-python


class GetNextFrame(threading.Thread):
    def __init__(self, acq_duration, expos_time, focal_start, focal_interval):
        threading.Thread.__init__(self) #initialize this class on a new thread for fastest possible capture of stacks
        print " ----------- Starting Acquisition thread ------------- "
        print "--> Initializing Camera Parameters"
        self.hcam = hc.HamamatsuCameraMR(0)
# Set camera parameters.
        cam_offset = 100
        cam_x = 2048
        cam_y = 2048
        self.hcam.setPropertyValue("defect_correct_mode", "OFF")
        self.hcam.setPropertyValue("exposure_time", expos_time)
        self.hcam.setPropertyValue("subarray_hsize", cam_x)
        self.hcam.setPropertyValue("subarray_vsize", cam_y)
        self.hcam.setPropertyValue("binning", "1x1")
        self.hcam.setPropertyValue("readout_speed", 2)

#        self.cam.set(16, expos_time) # Exposure propID# is 16 Exposure as appropriate for the fluorescence intensity
#        print "--> Initializing OptoTune Lens"
#        self.lens = Opto(port='/dev/cu.usbmodem1411') # Initialize the optotune lens
#        self.focal_interval = focal_interval
#        self.lens.connect()
#        self.lens.focalpower(focal_start) # Set the lens focal power to focus onto the top most z-plane
        self.stop_time = time.time() + acq_duration
        
        ########################################################################
        #                                                                      #
        #   Possibly implement sinusoidal travelling through the planes too    #
        #                                                                      #
        ########################################################################

    # This function actually captures the stacks, it has its own thread to run as fast as possible line - to - line
    def run(self):
        global Stack
        print "----> Starting acquisition"
        end = 0
        self.hcam.startAcquisition()
        #try:
        fNum = 0
        while time.time() < self.stop_time and end==0:
            
#               self.lens.focalpower( <<appropriate focal power>> )
            
            # This puts the frame into the Queue, and another thread takes care of it 
            # so that the program proceeds as fast as possible to the next step
            
            # << Modulo calculation to find the next focal power to adjust to according to focal_interval >>
            
            time.sleep(0.014) # Wait 14ms for the lens to adjust to the right focal power
         
            # <<** might be possible to lower this time because of small stack intervals 
            # and use larger wait times only when beginning the next stack!! ** >>
            [frame, dims] = self.hcam.getFrames()
            print 'Read frame num ' + str(fNum)
            #***************************************************************************
            ## >>> WHAT IF I JUST KEEP USING THIS FUNCTION BELOW TO GET IMAGES FROM TEH CAMERA????
            #***************************************************************************
            grey_values = frame[0].getData()
            Stack.put(grey_values)
            print type(grey_values)
            fNum += 1
#            self.lens.close(soft_close=True)
        Stack.put('done')
        self.hcam.stopAcquisition()
        self.hcam.shutdown()
            
        #except KeyboardInterrupt:
         #   end = 1
          #  raise
           # self.lens.close(soft_close=True)
        #except:
         #   print "------- !! Something went wrong during acquisition, lens set back to rest position !! ---------" 
            
# This class writes frames in the Queue, runs on a seperate thread to not disturb the acquisition of stacks on the other thread
class ImageWriter(multiprocessing.Process):
    def __init__(self, saveDir):
        multiprocessing.Process.__init__(self)
        print " ----------- Starting Image Writer thread -------------"
        self.saveDir = saveDir
        self.imgNum = 0

    def run(self):
        global Stack
        print "blaaaaaaah"
        end=0
        while end==0:
            #try:
            if not Stack.empty():
                grey_values = Stack.get()
                print 'Queue size is: ' + str(Stack.qsize())
                if str(grey_values) == 'done':
                    ##########################################################
                    # >>>>>>>>>> TEST IF SHOWING IMAGES IS CRASHING THE THING
                    ##########################################################
#                        print camData
#                        cv2.destroyAllWindows()
#                        Stack.task_done()
                    #self.hcam.stopAcquisition()
                    #self.hcam.shutdown()
                    break
                else:
                    #grey_values = camData[0].getData()
                    img = np.reshape(grey_values, (2048, 2048))
                    imgB = (img/256).astype('uint8')
                ##########################################################
                # >>>>>>>>>> TEST IF SHOWING IMAGES IS CRASHING THE THING
                ##########################################################
#                        cv2.namedWindow('Preview Window', cv2.WINDOW_NORMAL)
#                        cv2.resizeWindow('Preview Window', 1000, 1000)
#                        cv2.imshow('Preview Window', img)
#                        if cv2.waitKey(1) & 0xFF == ord('q'):
#                            cv2.destroyAllWindows()
#                            self.hcam.stopAcquisition()
#                            self.hcam.shutdown()
#                            break
                cv2.imwrite(self.saveDir + '%05d.tif' % self.imgNum, imgB)
                print "-> wrote frame to disk"
                self.imgNum += 1
#            except KeyboardInterrupt:
#                end=1
#                raise
            #except:
                #pass
                #print "Something went wrong with writing or displaying a frame"

# For testing this module by itself
if __name__ == '__main__':
    Stack = Queue(maxsize=0)
    # Test parameters
    acq_duration = 1
    expos_time = 0.01
    focal_start = 1
    focal_interval = 0.1
    saveDir ='D:\\Awesome_Imager_testing2\\'
    
    WriteImagesA = ImageWriter(saveDir)

    ########## >>> TRY CREATING WORKER POOL
    
    #worker = [None] * 5
    #for w in range(0,4):
    #    worker[w] = ImageWriter(saveDir)
    #    worker[w].run()
        
    Acquire = GetNextFrame(acq_duration, expos_time, focal_start, focal_interval)
    
    #Acquire.setDaemon(True)
    Acquire.start()
    #WriteImages.setDaemon(True)
    WriteImagesA.start()
    #WriteImages.join()
    #Acquire.join()
