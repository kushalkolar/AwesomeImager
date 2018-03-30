#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on March 22 2018

@author: kushal

Chatzigeorgiou Group
Sars International Centre for Marine Molecular Biology

GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007
"""
from __future__ import print_function
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from main_pytemplate import Ui_main
from functools import partial
from Queue import Queue
import numpy as np
import CameraInterfaces
import time
# from multiprocessing import Queue


class Main(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_main()
        self.ui.setupUi(self)

        self.ui.sliderFocalLength.valueChanged.connect(lambda v: self.ui.spinBoxCurrFocal.setValue(v / 100.0))
        self.ui.btnSavePathImgSeq.clicked.connect(self.set_img_seq_save_path)
        self.ui.btnPreview.clicked.connect(self.preview_slot)
        self.ui.btnAcquire.clicked.connect(self.acquire_slot)
        self.ui.btnAddStim.clicked.connect(self.add_stim)
        self.ui.btnDelStim.clicked.connect(self.del_stim)

        self.ui.sliderExposure.valueChanged.connect(self.update_preview)

        try:
            from subprocess import Popen, PIPE
            gitproc = Popen(['git', 'rev-parse', 'HEAD'], stdout=PIPE)
            (stdout, _) = gitproc.communicate()
            self.__version__ = stdout.strip().decode()
            print(self.__version__)
        except:
            self.__version__ = '4107ff58a0c3d4d5d3c15c3d6a69f8798a20e3de'
            print(self.__version__)

    def set_img_seq_save_path(self):
        path = QtWidgets.QFileDialog.getSaveFileName(self, 'Save Image Sequence as', '', '(*.tiff)')
        if path == '':
            return

        if path[0].endswith('.tiff') or path[0].endswith('.tif'):
            path = path[0]
        else:
            path = path[0] + '.tiff'

        self.ui.lineEdSavePathImgSeq.setText(path)

    def preview_slot(self, ev):
        print(ev)
        if ev:
            exp = self.ui.sliderExposure.value() / 1000.0
            params = {'exposure': exp}
            self.preview = CameraInterfaces.PreviewHamamatsu(**params)
            # self.preview = LivePreview.Preview(0, exp)
            self.preview.start()

        else:
            assert isinstance(self.preview, CameraInterfaces.PreviewHamamatsu)
            self.levels = self.preview.levels
            print(self.levels)
            mi = np.uint16(self.levels[0])
            mx = np.uint16(self.levels[1])
            self.levels = (mi, mx)
            print(type(self.levels[1]))
            self.preview.end()
            while self.preview.camera_open:
                time.sleep(0.01)
            self.preview = None
            print('closing preview')

    def update_preview(self, v):
        if not hasattr(self, 'preview'):
            return
        if isinstance(self.preview, CameraInterfaces.PreviewHamamatsu):
            self.preview.exposure = v / 1000.0

    def acquire_slot(self, ev):
        if ev:
            if (not self.ui.lineEdSavePathImgSeq.text().endswith('.tiff')) and \
                    (not self.ui.lineEdSavePathImgSeq.text().endswith('.tif')):
                QtWidgets.QMessageBox.warning(self, 'Invalid extension', 'Your must save your file with either an'
                                                                         ' .tiff or .tif extension!')
                self.ui.btnAcquire.setChecked(False)
                return

            if hasattr(self, 'preview'):
                if isinstance(self.preview, CameraInterfaces.PreviewHamamatsu):
                    self.preview_slot(False)

            m = self.ui.spinBoxMinutesAcquisition.value()
            ms = m * 60
            s = self.ui.spinBoxSecondsAcquisition.value()
            duration = s + ms
            exp = self.ui.sliderExposure.value() / 1000.0
            filename = self.ui.lineEdSavePathImgSeq.text()
            compression = self.ui.sliderCompressionLevel.value()

            params = {'exposure': exp,
                      'compression': compression,
                      'levels': self.levels,
                      'stims': {},
                      'version': self.__version__
                      }

            self.ui.progressBarWriter.setMaximum(int((duration * 1000) / self.ui.sliderExposure.value()) - 1)
            self.ui.btnPreview.setDisabled(True)
            self.ui.btnAcquire.setText('Abort')

            # q = Queue.Queue()
            q = Queue()

            writer = CameraInterfaces.WriterHamamatsu(q, filename, compression, self.levels, params)
            acquisition = CameraInterfaces.AcquireHamamatsu(params, q, duration)

            writer.start()
            acquisition.start()

            # WriteImages = ImageStack.ImageWriter(q, self, self.ui.lineEdSavePathImgSeq.text(), compression, exp, self.levels)
            # self.acquisition = ImageStack.GetNextFrame(q, duration, exp, 0, 0)
            # self.acquisition.start()
            # WriteImages.start()

        else:
            try:
                acquisition.end()
                if QtWidgets.QMessageBox.question(self, 'Stop writer?', 'Would you like to abort the writer as well?\n'
                                                                        'You will loose any frames that are currently '
                                                                        'in the queue', QtWidgets.QMessageBox.Abort,
                                                  QtWidgets.QMessageBox.No) == QtWidgets.QMessageBox.Abort:
                    writer.end()
                    # self.acquisition.end_acquisition()
            except:
                pass

        self.ui.btnPreview.setEnabled(True)
        self.ui.btnAcquire.setText('Acquire')
        self.ui.btnAcquire.setChecked(False)

    def set_frames_written_progressBar(self, fnum, qsize):
        self.ui.progressBarAcquisition.setValue(fnum)
        self.ui.labelQSize.setText(str(qsize))

    def add_stim(self):
        pass

    def del_stim(self):
        pass

    def export_config(self):
        pass

    def import_config(self):
        pass


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    win = QtWidgets.QMainWindow()
    win.setWindowTitle('Awesome Imager - because the other imager is not awesome')
    gui = Main()
    win.setCentralWidget(gui)
    win.show()
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtWidgets.QApplication.instance().exec_()
