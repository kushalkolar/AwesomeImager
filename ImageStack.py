import threading
import multiprocessing
import time
# from Queue import Queue
import cv2 # Import OpenCV2
import tifffile
#from opto import Opto # Import modules provided by optotune
import hamamatsu_camera as hc
import os
import numpy as np
import sys
import json
import datetime
import pyqtgraph as pg

class GetNextFrame(threading.Thread):
    def __init__(self, q, acq_duration, expos_time, focal_start, focal_interval):
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
        # self.hcam.setPropertyValue("internal_frame_rate", frame_rate)
        self.q = q

#        self.cam.set(16, expos_time) # Exposure propID# is 16 Exposure as appropriate for the fluorescence intensity
#        print "--> Initializing OptoTune Lens"
#        self.lens = Opto(port='/dev/cu.usbmodem1411') # Initialize the optotune lens
#        self.focal_interval = focal_interval
#        self.lens.connect()
#        self.lens.focalpower(focal_start) # Set the lens focal power to focus onto the top most z-plane
        self.stop_time = time.time() + acq_duration
        
    def run(self):
        # global Stack
        print "----> Starting acquisition"
        self.acquire = True
        self.hcam.startAcquisition()
        try:
            fNum = 0
            while time.time() < self.stop_time and self.acquire:
                
#               self.lens.focalpower( <<appropriate focal power>> )

                # << Modulo calculation to find the next focal power to adjust to according to focal_interval >>
                
                # time.sleep(0.014) # Wait 14ms for the lens to adjust to the right focal power
             
                # <<** might be possible to lower this time because of small stack intervals 
                # and use larger wait times only when beginning the next stack!! ** >>

                [frame, dim] = self.hcam.getFrames()
                print 'Read frame num ' + str(fNum)
                grey_values = frame[0].getData()
                self.q.put(grey_values)
                fNum += 1

            self.hcam.stopAcquisition()
            self.hcam.shutdown()
            self.q.put('done')

        except KeyboardInterrupt:
            acquire = False
            raise
#            self.lens.close(soft_close=True)
        except:
            print "------- !! Something went wrong during acquisition, lens set back to rest position !! ---------"

    def end_acquisition(self):
        self.acquire = False


class ImageWriter(threading.Thread):
    def __init__(self, q, parent, saveDir, compression_level, exp, levels):
        threading.Thread.__init__(self)
        print " ----------- Starting Image Writer Process -------------"
        self.saveDir = saveDir
        self.imgNum = 0
        self.tiff_writer = tifffile.TiffWriter(saveDir, bigtiff=True, append=True)
        self.compression_level = compression_level
        self.q = q
        self.parent = parent
        self.exp = exp
        self.levels = levels
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
        self.iv.setLevels(self.levels[0], self.levels[1])
        hist = self.iv.getHistogramWidget()
        hist.vb.enableAutoRange(hist.vb.YAxis, False)
        self.iv.show()
        
    def lut_8b(self, image):
        image.clip(self.levels[0], self.levels[1], out=image)
        image -= self.levels[0]
        np.floor_divide(image, (self.levels[1] - self.levels[0] + 1) / 256,
                        out=image, casting='unsafe')
        return image.astype(np.uint8)

    def set_lut(self, image) :
        lut = np.arange(65536, dtype=np.uint16)
        lut = self.lut_8b(lut)
        return np.take(lut, image).astype(np.uint8)

    def run(self):
        print 'Running Image Writer process'
        first_img = True
        while True:
            try:
                if self.q.not_empty:

                    camData = self.q.get()

                    if str(camData) == 'done':
                        break

                    else:
                        img = np.reshape(camData, (2048, 2048))
                        try:
                            self.iv.setImage(img, autoRange=False, autoLevels=False, autoHistogramRange=False, levels=self.levels)
                        except:
                            pass

                        img = self.set_lut(img)
                        self.tiff_writer.save(img, compress=self.compression_level)
                        print 'qsize is: ' + str(self.q.qsize())
                        print 'wrote ImgNum: ' + str(self.imgNum)
#                        self.parent.set_frames_written_progressBar(self.imgNum, self.q.qsize())
                        
                        self.q.task_done()
                        self.imgNum += 1

            except KeyboardInterrupt:
                break
        self.tiff_writer.close()
        # cv2.destroyAllWindows()
        self.parent.acquire_slot(False)

        date = datetime.datetime.fromtimestamp(time.time())
        ymd = date.strftime('%Y%m%d')
        hms = date.strftime('%H%M%S')

        metadata = {'exposure': self.exp,
                    'source': 'AwesomeImager',
                    'version': self.parent.__version__,
                    'date': ymd,
                    'time': hms,
                    'stims': None}
        
        if self.saveDir.endswith('.tiff'):
            json_file = self.saveDir[:-5] + '.json'
        elif self.saveDir.endswith('.tif'):
            json_file = self.saveDir[:-4] + '.json'
            
        with open(json_file, 'w') as f:
            json.dump(metadata, f)


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
