import threading
import time
from Queue import Queue
import cv2 # Import OpenCV2
#from opto import Opto # Import modules provided by optotune
import hamamatsu_camera as hc
import os
import numpy as np
import sys

#TRY TO REPLACE THREADING WITH PROCESS: http://stackoverflow.com/questions/323972/is-there-any-way-to-kill-a-thread-in-python
#Tested both, threading seems perfectly sufficient
# hcam object is ctypes so it's difficult to make a working module with multiprocessing

# Queue used to pass objects between threads
PreviewQueue = Queue(maxsize=0)
BufferQueue = Queue(maxsize=0)
WriteQueue = Queue(maxsize=0)

# Threading class that gets frames from camera and puts them into the Queue
class GrabFrames(threading.Thread):
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

#        self.cam.set(16, expos_time) # for OpenCV compatible cams
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
        try:
            fNum = 0
            self.hcam.startAcquisition()
            while time.time() < self.stop_time and end==0:
                
#               self.lens.focalpower( <<appropriate focal power>> )
                
                # << Modulo calculation to find the next focal power to adjust to according to focal_interval >>
                
                time.sleep(0.014) # Wait 14ms for the lens to adjust to the right focal power
             
                # <<** might be possible to lower this time because of small stack intervals 
                # and use larger wait times only when beginning the next stack!! ** >>
                [frame, dims] = self.hcam.getFrames()
                #print 'Read frame num ' + str(fNum)
                #***********************************************************************************
                ## >>> WHAT IF I JUST KEEP USING THIS FUNCTION BELOW TO GET IMAGES FROM TEH CAMERA????
                #**********************************************************************************
                grey_values = frame[0].getData()
                #indexed = np.array([grey_values, 1, 2])
                PreviewQueue.put(grey_values)
                fNum += 1
#            self.lens.close(soft_close=True)
            PreviewQueue.put('done')
            self.hcam.stopAcquisition()
            self.hcam.shutdown()
            
        except KeyboardInterrupt:
            end = 1
            raise
#            self.lens.close(soft_close=True)
       # except Exception as e:
            #logger.exception(str(e))
            #print "------- !! Something went wrong during acquisition, lens set back to rest position !! ---------"

# Live Preview class thread, recieves img from queue, displays, puts into another Queue that ImgPPE takes
class Preview(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        global PreviewQueue
        end = 0
        while end == 0:
            if PreviewQueue.not_empty:
                grey_values = PreviewQueue.get()
                print 'Preview Queue size is: ' + str(PreviewQueue.qsize())
                if str(grey_values) == 'done':
                    break
                img = np.reshape(grey_values, (2048, 2048))
                BufferQueue.put(img)
                cv2.namedWindow('Preview Window', cv2.WINDOW_NORMAL)
                cv2.resizeWindow('Preview Window', 1000, 1000)
                cv2.imshow('Preview Window', img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    cv2.destroyAllWindows()

# This takes grey values from the Queue and does PostProcessing & encodes Img into memory buffer
class ImgPPE(threading.Thread):
    def __init__(self, saveDir):
        threading.Thread.__init__(self)
        print " ----------- Starting Image Writer thread -------------"
        self.saveDir = saveDir
        self.imgNum = 0
        #fourcc = cv2.VideoWriter_fourcc(*'PIMJ')
        #fps = 5# int(1.0/(expos_time + .014))
        #self.out = cv2.VideoWriter(saveDir + 'out.avi', fourcc, fps, (2048,2048), False)
        self.buffer = []

    def run(self):
        global BufferQueue
        end=0
        while end==0:
            try:
                if BufferQueue.not_empty:
                    img = BufferQueue.get()
                    #print 'Buffer Queue size is: ' + str(BufferQueue.qsize())
                    if str(img) == 'done':
                        print ' >> ' + str(sys.getsizeof(self.buffer))
                        break
                    else:
                        #grey_values = camData[0].getData()
                        #print sys.getsizeof(grey_values)class gets an 8bit grayscale image and saves it to memory buffer   
                        imgB = (img/256).astype('uint8')

                        #cv2.imwrite(self.saveDir + '%05d.tif' % self.imgNum, imgB)
                        
                        
# >>>>>>>>>> ******** NEED TO LOOK INTO PYTHON MEM BUFFER HANDLING
                        rval, bufImg = cv2.imencode('.tif', imgB)
                        self.buffer.append(bufImg)
                        if self.imgNum % 1000 == 0:
                            pass
                        #>> ** SPAWN PROCESS, SUBPROCESS, OR THREAD TO WRITE THE 1GB IMAGE CHUNK
                        #>> ** AND CONTINUE WITH THE PROGRAM, IF USING THREAD DO NOT USE .join() METHOD
                            
                            
                        #self.out.write(colorImg)
                        BufferQueue.task_done()
                        #print "-> wrote frame to disk"
                        self.imgNum += 1
           # except Exception as e:
                ## >>>> DO SOMETHING HERE TO SAVE REMAINING BUFFER TO DISK!!!!! <<<<<<
               # logger.exception(str(e))
                #end=1
                #raise
            except:
                pass
                print "Something went wrong with writing or displaying a frame"

if __name__ == '__main__':
    acq_duration = 10
    expos_time = 0.01
    focal_start = 1
    focal_interval = 0.1
    saveDir ='D:\\Awesome_Imager_testing\\'
    
   # WriteImages = ImgPPE(saveDir)
    ########## >>> TRY CREATING WORKER POOL
    
    LivePreview = Preview()
    
    
    worker = [None] * 4
    for w in range(0,4):
        worker[w] = ImgPPE(saveDir + '\\' + str(w) + '\\')
        worker[w].start()
    
    LivePreview.start()
    Acquire = GrabFrames(acq_duration, expos_time, focal_start, focal_interval)
    
    #Acquire.setDaemon(True)
    #WriteImages.start()
    Acquire.start()
    #WriteImages.setDaemon(True)
    
   #WriteImages.join()
    #Acquire.join()
