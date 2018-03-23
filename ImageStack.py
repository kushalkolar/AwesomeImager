import threading
import time
from Queue import Queue
import cv2 # Import OpenCV2
import tifffile
#from opto import Opto # Import modules provided by optotune
import hamamatsu_camera as hc
import os
import numpy as np
import sys

#TRY TO REPLACE THREADING WITH PROCESS: http://stackoverflow.com/questions/323972/is-there-any-way-to-kill-a-thread-in-python

Stack = Queue(maxsize=0)

class GetNextFrame(threading.Thread):
    def __init__(self, acq_duration, expos_time, frame_rate, focal_start, focal_interval):
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
        self.hcam.setPropertyValue("internal_frame_rate", frame_rate)

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
        try:
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
                fNum += 1
#            self.lens.close(soft_close=True)
            Stack.put('done')
            self.hcam.stopAcquisition()
            self.hcam.shutdown()
            
        except KeyboardInterrupt:
            end = 1
            raise
#            self.lens.close(soft_close=True)
        except:
            print "------- !! Something went wrong during acquisition, lens set back to rest position !! ---------"

# This class writes frames in the Queue, runs on a seperate thread to not disturb the acquisition of stacks on the other thread
class ImageWriter(threading.Thread):
    def __init__(self, saveDir, compression_level):
        threading.Thread.__init__(self)
        print " ----------- Starting Image Writer thread -------------"
        self.saveDir = saveDir
        self.imgNum = 0
        #fourcc = cv2.VideoWriter_fourcc(*'PIMJ')
        #fps = 5# int(1.0/(expos_time + .014))
        #self.out = cv2.VideoWriter(saveDir + 'out.avi', fourcc, fps, (2048,2048), False)
        # self.buffer = []
        self.tiff_writer = tifffile.TiffWriter(saveDir, bigtiff=True, append=True)
        self.compression_level = compression_level
    def run(self):
        global Stack
        end = 0
        while end == 0:
            try:
                if Stack.not_empty:
                    camData = Stack.get()
                    print 'Queue size is: ' + str(Stack.qsize())
                    if str(camData) == 'done':
                        # print ' >> ' + str(sys.getsizeof(self.buffer))
                        ##########################################################
                        # >>>>>>>>>> TEST IF SHOWING IMAGES IS CRASHING THE THING
                        ##########################################################
#                        print camData
#                        cv2.destroyAllWindows()
#                        Stack.task_done()
                        #self.hcam.stopAcquisition()
                        #self.hcam.shutdown()
                        #self.out.release()
                        self.tiff_writer.close()
                        break
                    else:
                        #grey_values = camData[0].getData()
                        #print sys.getsizeof(grey_values)
                        img = np.reshape(camData, (2048, 2048))
                        imgB = (img/256).astype('uint8')
                        #colorImg = imgB# cv2.cvtColor(imgB,cv2.COLOR_GRAY2RGB)
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
                        #cv2.imwrite(self.saveDir + '%05d.tif' % self.imgNum, imgB)
                        # rval, bufImg = cv2.imencode('.tif', imgB)
                        # self.buffer.append(bufImg)
                        self.tiff_writer.save(imgB, compress=self.compression_level)
                        print 'Wrote frame num: ' + str(self.imgNum)
                        
                        #self.out.write(colorImg)
                        Stack.task_done()
                        #print "-> wrote frame to disk"
                        self.imgNum += 1
            except KeyboardInterrupt:
                end=1
                raise
            #except:
                #pass
                #print "Something went wrong with writing or displaying a frame"

if __name__ == '__main__':
    acq_duration = 10
    expos_time = 0.01
    focal_start = 1
    focal_interval = 0.1
    saveDir ='D:\\Awesome_Imager_testing\\'
    
   # WriteImages = ImageWriter(saveDir)
    ########## >>> TRY CREATING WORKER POOL
    
    worker = [None] * 3
    for w in range(0,3):
        worker[w] = ImageWriter(saveDir + '\\' + str(w) + '\\')
        worker[w].start()
       
    Acquire = GetNextFrame(acq_duration, expos_time, focal_start, focal_interval)
    
    #Acquire.setDaemon(True)
    #WriteImages.start()
    Acquire.start()
    #WriteImages.setDaemon(True)
    
   #WriteImages.join()
    #Acquire.join()
