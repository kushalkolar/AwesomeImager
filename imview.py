import pyqtgraph as pg

class ImageView(pg.imageview.ImageView):
    def __init__(self):
        pg.imageview.ImageView.__init__()

    def roiChanged(self):
        pass

    def roiClicked(self):
        if self.ui.roiBtn.isChecked():
            self.roi.show()
