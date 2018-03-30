import cv2 # Import OpenCV2
#from opto import Opto # Import modules provided by optotune
import numpy as np
import sys
import multiprocessing

class ImageWriterProcess(multiprocessing.Process):
    def __init__(self, saveDir):
        multiprocessing.Process.__init__(self)
        print " ----------- Starting Image Writer thread -------------"
        self.saveDir = saveDir
        self.imgNum = 0
        #fourcc = cv2.VideoWriter_fourcc(*'PIMJ')
        #fps = 5# int(1.0/(expos_time + .014))
        #self.out = cv2.VideoWriter(saveDir + 'out.avi', fourcc, fps, (2048,2048), False)
        self.buffer = []

    def run(self):
        global Stack
        end=0
        while end==0:
            try:
                if Stack.not_empty:
                    camData = Stack.get()
                    print 'Queue size is: ' + str(Stack.qsize())
                    if str(camData) == 'done':
                        print ' >> ' + str(sys.getsizeof(self.buffer))
                        ##########################################################
                        # >>>>>>>>>> TEST IF SHOWING IMAGES IS CRASHING THE THING
                        ##########################################################
#                        print camData
#                        cv2.destroyAllWindows()
#                        Stack.task_done()
                        #self.hcam.stopAcquisition()
                        #self.hcam.shutdown()
                        #self.out.release()
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
                        rval, bufImg = cv2.imencode('.tif', imgB)
                        self.buffer.append(bufImg)
                        
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