# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_pytemplate.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_main(object):
    def setupUi(self, main):
        main.setObjectName("main")
        main.resize(831, 487)
        self.gridLayout_9 = QtWidgets.QGridLayout(main)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.groupBoxSaveOptions = QtWidgets.QGroupBox(main)
        self.groupBoxSaveOptions.setObjectName("groupBoxSaveOptions")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.groupBoxSaveOptions)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_4 = QtWidgets.QLabel(self.groupBoxSaveOptions)
        self.label_4.setMaximumSize(QtCore.QSize(84, 16777215))
        self.label_4.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.label_7 = QtWidgets.QLabel(self.groupBoxSaveOptions)
        self.label_7.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_4.addWidget(self.label_7)
        self.gridLayout_7.addLayout(self.horizontalLayout_4, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(129, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_7.addItem(spacerItem, 0, 1, 1, 1)
        self.sliderCompressionLevel = QtWidgets.QSlider(self.groupBoxSaveOptions)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sliderCompressionLevel.sizePolicy().hasHeightForWidth())
        self.sliderCompressionLevel.setSizePolicy(sizePolicy)
        self.sliderCompressionLevel.setMinimumSize(QtCore.QSize(319, 0))
        self.sliderCompressionLevel.setMaximum(9)
        self.sliderCompressionLevel.setPageStep(1)
        self.sliderCompressionLevel.setProperty("value", 3)
        self.sliderCompressionLevel.setOrientation(QtCore.Qt.Horizontal)
        self.sliderCompressionLevel.setObjectName("sliderCompressionLevel")
        self.gridLayout_7.addWidget(self.sliderCompressionLevel, 1, 0, 1, 3)
        self.lineEdSavePathImgSeq = QtWidgets.QLineEdit(self.groupBoxSaveOptions)
        self.lineEdSavePathImgSeq.setObjectName("lineEdSavePathImgSeq")
        self.gridLayout_7.addWidget(self.lineEdSavePathImgSeq, 2, 0, 1, 2)
        self.btnSavePathImgSeq = QtWidgets.QPushButton(self.groupBoxSaveOptions)
        self.btnSavePathImgSeq.setMinimumSize(QtCore.QSize(31, 26))
        self.btnSavePathImgSeq.setMaximumSize(QtCore.QSize(31, 26))
        self.btnSavePathImgSeq.setObjectName("btnSavePathImgSeq")
        self.gridLayout_7.addWidget(self.btnSavePathImgSeq, 2, 2, 1, 1)
        self.gridLayout_9.addWidget(self.groupBoxSaveOptions, 1, 3, 2, 4)
        self.groupBoxTimelapse = QtWidgets.QGroupBox(main)
        self.groupBoxTimelapse.setObjectName("groupBoxTimelapse")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBoxTimelapse)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.spinBoxMinutesAcquisition = QtWidgets.QSpinBox(self.groupBoxTimelapse)
        self.spinBoxMinutesAcquisition.setObjectName("spinBoxMinutesAcquisition")
        self.gridLayout_2.addWidget(self.spinBoxMinutesAcquisition, 0, 1, 1, 1)
        self.spinBoxSecondsAcquisition = QtWidgets.QSpinBox(self.groupBoxTimelapse)
        self.spinBoxSecondsAcquisition.setMaximum(59)
        self.spinBoxSecondsAcquisition.setProperty("value", 10)
        self.spinBoxSecondsAcquisition.setObjectName("spinBoxSecondsAcquisition")
        self.gridLayout_2.addWidget(self.spinBoxSecondsAcquisition, 1, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.groupBoxTimelapse)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 1, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.groupBoxTimelapse)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 0, 0, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 0, 1, 1)
        self.gridLayout_9.addWidget(self.groupBoxTimelapse, 1, 1, 2, 2)
        self.btnImportConfig = QtWidgets.QPushButton(main)
        self.btnImportConfig.setObjectName("btnImportConfig")
        self.gridLayout_9.addWidget(self.btnImportConfig, 3, 2, 1, 2)
        self.groupBoxStimuli = QtWidgets.QGroupBox(main)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBoxStimuli.sizePolicy().hasHeightForWidth())
        self.groupBoxStimuli.setSizePolicy(sizePolicy)
        self.groupBoxStimuli.setObjectName("groupBoxStimuli")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.groupBoxStimuli)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.label_8 = QtWidgets.QLabel(self.groupBoxStimuli)
        self.label_8.setObjectName("label_8")
        self.gridLayout_5.addWidget(self.label_8, 0, 0, 1, 1)
        self.lineEdStimName = QtWidgets.QLineEdit(self.groupBoxStimuli)
        self.lineEdStimName.setObjectName("lineEdStimName")
        self.gridLayout_5.addWidget(self.lineEdStimName, 0, 1, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.groupBoxStimuli)
        self.label_9.setObjectName("label_9")
        self.gridLayout_5.addWidget(self.label_9, 1, 0, 1, 1)
        self.spinBoxValveNum = QtWidgets.QSpinBox(self.groupBoxStimuli)
        self.spinBoxValveNum.setObjectName("spinBoxValveNum")
        self.gridLayout_5.addWidget(self.spinBoxValveNum, 1, 1, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout_5)
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_12 = QtWidgets.QLabel(self.groupBoxStimuli)
        self.label_12.setObjectName("label_12")
        self.gridLayout_4.addWidget(self.label_12, 0, 1, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.groupBoxStimuli)
        self.label_13.setObjectName("label_13")
        self.gridLayout_4.addWidget(self.label_13, 0, 2, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.groupBoxStimuli)
        self.label_10.setObjectName("label_10")
        self.gridLayout_4.addWidget(self.label_10, 1, 0, 1, 1)
        self.spinBoxStimStartMin = QtWidgets.QSpinBox(self.groupBoxStimuli)
        self.spinBoxStimStartMin.setObjectName("spinBoxStimStartMin")
        self.gridLayout_4.addWidget(self.spinBoxStimStartMin, 1, 1, 1, 1)
        self.spinBoxStimStartSec = QtWidgets.QSpinBox(self.groupBoxStimuli)
        self.spinBoxStimStartSec.setMaximum(59)
        self.spinBoxStimStartSec.setObjectName("spinBoxStimStartSec")
        self.gridLayout_4.addWidget(self.spinBoxStimStartSec, 1, 2, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.groupBoxStimuli)
        self.label_11.setObjectName("label_11")
        self.gridLayout_4.addWidget(self.label_11, 2, 0, 1, 1)
        self.spinBoxStimEndMin = QtWidgets.QSpinBox(self.groupBoxStimuli)
        self.spinBoxStimEndMin.setObjectName("spinBoxStimEndMin")
        self.gridLayout_4.addWidget(self.spinBoxStimEndMin, 2, 1, 1, 1)
        self.spinBoxStimEndSec = QtWidgets.QSpinBox(self.groupBoxStimuli)
        self.spinBoxStimEndSec.setMaximum(59)
        self.spinBoxStimEndSec.setObjectName("spinBoxStimEndSec")
        self.gridLayout_4.addWidget(self.spinBoxStimEndSec, 2, 2, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.btnDelStim = QtWidgets.QPushButton(self.groupBoxStimuli)
        self.btnDelStim.setObjectName("btnDelStim")
        self.horizontalLayout_5.addWidget(self.btnDelStim)
        self.btnAddStim = QtWidgets.QPushButton(self.groupBoxStimuli)
        self.btnAddStim.setObjectName("btnAddStim")
        self.horizontalLayout_5.addWidget(self.btnAddStim)
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)
        self.gridLayout_8.addLayout(self.verticalLayout_3, 0, 1, 1, 1)
        self.columnView = QtWidgets.QColumnView(self.groupBoxStimuli)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.columnView.sizePolicy().hasHeightForWidth())
        self.columnView.setSizePolicy(sizePolicy)
        self.columnView.setObjectName("columnView")
        self.gridLayout_8.addWidget(self.columnView, 0, 0, 2, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_8.addItem(spacerItem1, 1, 1, 1, 1)
        self.gridLayout_9.addWidget(self.groupBoxStimuli, 0, 1, 1, 6)
        self.groupBoxExposure = QtWidgets.QGroupBox(main)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBoxExposure.sizePolicy().hasHeightForWidth())
        self.groupBoxExposure.setSizePolicy(sizePolicy)
        self.groupBoxExposure.setMinimumSize(QtCore.QSize(245, 0))
        self.groupBoxExposure.setObjectName("groupBoxExposure")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.groupBoxExposure)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.sliderExposure = QtWidgets.QSlider(self.groupBoxExposure)
        self.sliderExposure.setMinimum(1)
        self.sliderExposure.setMaximum(5000)
        self.sliderExposure.setSingleStep(5)
        self.sliderExposure.setPageStep(25)
        self.sliderExposure.setProperty("value", 50)
        self.sliderExposure.setOrientation(QtCore.Qt.Horizontal)
        self.sliderExposure.setObjectName("sliderExposure")
        self.gridLayout_6.addWidget(self.sliderExposure, 1, 0, 1, 1)
        self.spinBoxExposure = QtWidgets.QSpinBox(self.groupBoxExposure)
        self.spinBoxExposure.setMinimumSize(QtCore.QSize(71, 0))
        self.spinBoxExposure.setMaximumSize(QtCore.QSize(71, 16777215))
        self.spinBoxExposure.setMinimum(1)
        self.spinBoxExposure.setMaximum(5000)
        self.spinBoxExposure.setSingleStep(25)
        self.spinBoxExposure.setProperty("value", 50)
        self.spinBoxExposure.setObjectName("spinBoxExposure")
        self.gridLayout_6.addWidget(self.spinBoxExposure, 0, 0, 1, 1)
        self.gridLayout_9.addWidget(self.groupBoxExposure, 2, 0, 2, 1)
        self.btnExportConfig = QtWidgets.QPushButton(main)
        self.btnExportConfig.setObjectName("btnExportConfig")
        self.gridLayout_9.addWidget(self.btnExportConfig, 3, 1, 1, 1)
        self.btnPreview = QtWidgets.QPushButton(main)
        self.btnPreview.setCheckable(True)
        self.btnPreview.setObjectName("btnPreview")
        self.gridLayout_9.addWidget(self.btnPreview, 3, 5, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(76, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_9.addItem(spacerItem2, 3, 4, 1, 1)
        self.groupBoxFocalLength = QtWidgets.QGroupBox(main)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBoxFocalLength.sizePolicy().hasHeightForWidth())
        self.groupBoxFocalLength.setSizePolicy(sizePolicy)
        self.groupBoxFocalLength.setMinimumSize(QtCore.QSize(0, 0))
        self.groupBoxFocalLength.setMaximumSize(QtCore.QSize(2450, 10000))
        self.groupBoxFocalLength.setObjectName("groupBoxFocalLength")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBoxFocalLength)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.groupBoxFocalLength)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.spinBoxUpperLimitFocal = QtWidgets.QDoubleSpinBox(self.groupBoxFocalLength)
        self.spinBoxUpperLimitFocal.setMinimum(-3.0)
        self.spinBoxUpperLimitFocal.setMaximum(3.0)
        self.spinBoxUpperLimitFocal.setSingleStep(0.25)
        self.spinBoxUpperLimitFocal.setObjectName("spinBoxUpperLimitFocal")
        self.horizontalLayout.addWidget(self.spinBoxUpperLimitFocal)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.groupBoxFocalLength)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.spinBoxLowerLimitFocal = QtWidgets.QDoubleSpinBox(self.groupBoxFocalLength)
        self.spinBoxLowerLimitFocal.setMinimum(-3.0)
        self.spinBoxLowerLimitFocal.setMaximum(3.0)
        self.spinBoxLowerLimitFocal.setSingleStep(0.25)
        self.spinBoxLowerLimitFocal.setObjectName("spinBoxLowerLimitFocal")
        self.horizontalLayout_2.addWidget(self.spinBoxLowerLimitFocal)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        self.sliderFocalLength = QtWidgets.QSlider(self.groupBoxFocalLength)
        self.sliderFocalLength.setMinimum(-300)
        self.sliderFocalLength.setMaximum(300)
        self.sliderFocalLength.setSingleStep(25)
        self.sliderFocalLength.setPageStep(50)
        self.sliderFocalLength.setOrientation(QtCore.Qt.Vertical)
        self.sliderFocalLength.setObjectName("sliderFocalLength")
        self.horizontalLayout_3.addWidget(self.sliderFocalLength)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        spacerItem4 = QtWidgets.QSpacerItem(20, 27, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem4)
        self.label_3 = QtWidgets.QLabel(self.groupBoxFocalLength)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.spinBoxCurrFocal = QtWidgets.QDoubleSpinBox(self.groupBoxFocalLength)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBoxCurrFocal.sizePolicy().hasHeightForWidth())
        self.spinBoxCurrFocal.setSizePolicy(sizePolicy)
        self.spinBoxCurrFocal.setMaximumSize(QtCore.QSize(50, 16777215))
        self.spinBoxCurrFocal.setMinimum(-3.0)
        self.spinBoxCurrFocal.setMaximum(3.0)
        self.spinBoxCurrFocal.setSingleStep(0.25)
        self.spinBoxCurrFocal.setObjectName("spinBoxCurrFocal")
        self.verticalLayout_2.addWidget(self.spinBoxCurrFocal)
        spacerItem5 = QtWidgets.QSpacerItem(20, 28, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem5)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)
        self.gridLayout.addLayout(self.horizontalLayout_3, 0, 0, 1, 1)
        self.gridLayout_9.addWidget(self.groupBoxFocalLength, 0, 0, 2, 1)
        self.btnAcquire = QtWidgets.QPushButton(main)
        self.btnAcquire.setCheckable(True)
        self.btnAcquire.setObjectName("btnAcquire")
        self.gridLayout_9.addWidget(self.btnAcquire, 3, 6, 1, 1)

        self.retranslateUi(main)
        self.sliderExposure.valueChanged['int'].connect(self.spinBoxExposure.setValue)
        self.spinBoxExposure.valueChanged['int'].connect(self.sliderExposure.setValue)
        self.sliderCompressionLevel.valueChanged['int'].connect(self.label_7.setNum)
        QtCore.QMetaObject.connectSlotsByName(main)

    def retranslateUi(self, main):
        _translate = QtCore.QCoreApplication.translate
        main.setWindowTitle(_translate("main", "Form"))
        self.groupBoxSaveOptions.setTitle(_translate("main", "Save options"))
        self.label_4.setStatusTip(_translate("main", "Higher value = more compression"))
        self.label_4.setText(_translate("main", "Compression: "))
        self.label_7.setToolTip(_translate("main", "Higher value = more compression"))
        self.label_7.setText(_translate("main", "3"))
        self.sliderCompressionLevel.setStatusTip(_translate("main", "Higher value = more compression"))
        self.lineEdSavePathImgSeq.setPlaceholderText(_translate("main", "File path"))
        self.btnSavePathImgSeq.setText(_translate("main", "..."))
        self.groupBoxTimelapse.setTitle(_translate("main", "Timelapse"))
        self.label_6.setText(_translate("main", "seconds"))
        self.label_5.setText(_translate("main", "minutes"))
        self.btnImportConfig.setText(_translate("main", "Import config"))
        self.groupBoxStimuli.setTitle(_translate("main", "Stimuli"))
        self.label_8.setText(_translate("main", "Name"))
        self.label_9.setText(_translate("main", "Valve"))
        self.label_12.setText(_translate("main", "Minute"))
        self.label_13.setText(_translate("main", "Second"))
        self.label_10.setText(_translate("main", "tStart"))
        self.label_11.setText(_translate("main", "tEnd"))
        self.btnDelStim.setText(_translate("main", "Delete"))
        self.btnAddStim.setText(_translate("main", "Add"))
        self.groupBoxExposure.setToolTip(_translate("main", "Set exposure duration"))
        self.groupBoxExposure.setTitle(_translate("main", "Exposure (ms)"))
        self.btnExportConfig.setText(_translate("main", "Export config"))
        self.btnPreview.setText(_translate("main", "Preview"))
        self.groupBoxFocalLength.setTitle(_translate("main", "Focal Length"))
        self.label.setText(_translate("main", "Upper Limit"))
        self.label_2.setText(_translate("main", "Lower Limit"))
        self.label_3.setText(_translate("main", "Current"))
        self.btnAcquire.setText(_translate("main", "Acquire"))

