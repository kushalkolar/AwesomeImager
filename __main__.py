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
import LivePreview
import ImageStack

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

        self.ui.sliderExposure.valueChanged.connect(self.update_preview)

    def update_preview(self):
        if isinstance(self.preview, LivePreview.Preview):
#            self.preview.expos_time.put(self.ui.sliderExposure.value() / 1000.0)
            self.preview.hcam.setPropertyValue("exposure_time", self.ui.sliderExposure.value() / 1000.0)

    def set_img_seq_save_path(self, path):
        pass

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

    def acquire_slot(self, ev):
        if ev:
            m = self.ui.spinBoxMinutesAcquisition.value()
            ms = m * 60
            s = self.ui.spinBoxSecondsAcquisition.value()
            acq_secs = s + ms
            exp = self.ui.sliderExposure.value()

            acq_settings = {'duration': acq_secs,
                            'exp':      exp,
                            'stims':    {},
                            }

            self.ui.btnPreview.setDisabled(True)
            self.ui.btnAcquire.setText('Abort')

        elif not ev:
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
