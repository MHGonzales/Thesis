import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import cv2

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.VBL = QVBoxLayout(self)
        self.splitter=QSplitter(Qt.Horizontal)
        
        self.camera1=QGroupBox('Camera 1')
        self.Worker1 = Worker1()
        self.Worker1.start()
        self.Worker1.ImageUpdate1.connect(self.ImageUpdateSlot)
        self.cam1_layout=QVBoxLayout(self.camera1)
        # self.cam1_layout.addWidget(self.Worker1)
        
        self.camera2=QGroupBox('Camera 2')
        self.Worker2 = Worker2()
        self.Worker2.start()
        self.Worker2.ImageUpdate2.connect(self.ImageUpdateSlot)
        self.cam2_layout=QVBoxLayout(self.camera2)
        # self.cam2_layout.addWidget(self.Worker2)
                
        self.FeedLabel = QLabel()
        self.VBL.addWidget(self.FeedLabel)

        self.CancelBTN = QPushButton("Cancel")
        self.CancelBTN.clicked.connect(self.CancelFeed)
        self.VBL.addWidget(self.CancelBTN)



        self.setLayout(self.VBL)

    def ImageUpdateSlot(self, Image):
        self.FeedLabel.setPixmap(QPixmap.fromImage(Image))

    def CancelFeed(self):
        self.Worker1.stop()

class Worker1(QThread):
    ImageUpdate1 = pyqtSignal(QImage)
    def run(self):
        self.ThreadActive1 = True
        Capture1 = cv2.VideoCapture(0)
        while self.ThreadActive1:
            ret, frame1 = Capture1.read()
            if ret:
                Image1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
                FlippedImage1 = cv2.flip(FlippedImage1, 1)
                ConvertToQtFormat1 = QImage(FlippedImage1.data, FlippedImage1.shape[1], FlippedImage1.shape[0], QImage.Format_RGB888)
                Pic1 = ConvertToQtFormat1.scaled(640, 480, Qt.KeepAspectRatio)
                self.ImageUpdate1.emit(Pic1)
    def stop(self):
        self.ThreadActive1 = False
        self.quit()

class Worker2(QThread):
    ImageUpdate2 = pyqtSignal(QImage)
    def run(self):
        self.ThreadActive2 = True
        Capture2 = cv2.VideoCapture(0)
        while self.ThreadActive2:
            ret, frame2 = Capture2.read()
            if ret:
                Image2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
                FlippedImage2 = cv2.flip(Image2, 1)
                ConvertToQtFormat2 = QImage(FlippedImage2.data, FlippedImage2.shape[1], FlippedImage2.shape[0], QImage.Format_RGB888)
                Pic2 = ConvertToQtFormat2.scaled(640, 480, Qt.KeepAspectRatio)
                self.ImageUpdate2.emit(Pic2)
    def stop(self):
        self.ThreadActive2 = False
        self.quit()

if __name__ == "__main__":
    App = QApplication(sys.argv)
    Root = MainWindow()
    Root.show()
    sys.exit(App.exec())