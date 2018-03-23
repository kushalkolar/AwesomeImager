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
# import LivePreview
# import ImageStack
from functools import partial

class Main(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_main()
        self.ui.setupUi(self)

        self.ui.sliderFocalLength.valueChanged.connect(lambda v: self.ui.spinBoxCurrFocal.setValue(v/100.0))
        self.ui.btnSavePathImgSeq.clicked.connect(self.set_img_seq_save_path)
        self.ui.btnPreview.clicked.connect(self.preview_slot)
        self.ui.btnAcquire.clicked.connect(self.acquire_slot)
        self.ui.btnAddStim.clicked.connect(self.add_stim)
        self.ui.btnDelStim.clicked.connect(self.del_stim)

        self.ui.sliderExposure.valueChanged.connect(self.set_frame_rate_spinBox)
        self.ui.sliderExposure.valueChanged.connect(self.update_preview)

        self.ui.checkBoxMaxFrameRate.clicked.connect(self.set_frame_rate_spinBox)

    def set_frame_rate_spinBox(self, v):
        if type(v) is bool:
            v = self.ui.sliderExposure.value()
        self.ui.spinBoxFrameRate.setMaximum(1000.0 / v)
        if self.ui.checkBoxMaxFrameRate.isChecked():
            self.ui.spinBoxFrameRate.setValue(1000.0 / v)

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
            self.preview = LivePreview.Preview(0, exp)
            self.preview.start()

        elif not ev:
            self.preview.endPreview()
            self.preview = None
            print('closing preview')

    def update_preview(self, v):
        if not hasattr(self, 'preview'):
            return
        if isinstance(self.preview, LivePreview.Preview):
            #            self.preview.expos_time.put(self.ui.sliderExposure.value() / 1000.0)
            self.preview.hcam.setPropertyValue("exposure_time", v/1000.0)

    def acquire_slot(self, ev):
        if ev:
            m = self.ui.spinBoxMinutesAcquisition.value()
            ms = m * 60
            s = self.ui.spinBoxSecondsAcquisition.value()
            acq_secs = s + ms
            exp = self.ui.sliderExposure.value() / 1000.0
            frame_rate = self.ui.spinBoxFrameRate.value()
            compression = self.ui.sliderCompressionLevel.value()
            acq_settings = {'duration': acq_secs,
                            'exp':      exp,
                            'stims':    {},
                            }

            self.ui.btnPreview.setDisabled(True)
            self.ui.btnAcquire.setText('Abort')


            WriteImages = ImageStack.ImageWriter(self.ui.lineEdSavePathImgSeq.text(), compression)
            Acquire = ImageStack.GetNextFrame(acq_secs, exp, 0, 0)

            Acquire.start()
            WriteImages.start()

            self.StopAcquisition()

        self.ui.btnPreview.setEnabled(True)
        self.ui.btnAcquire.setText('Acquire')

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
    gui = Main()
    win.setCentralWidget(gui)
    win.show()
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtWidgets.QApplication.instance().exec_()
