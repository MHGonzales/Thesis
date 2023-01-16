from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setGeometry(200, 200, 300, 300)
        self.setWindowTitle("RIAL-3-2021-4")
        self.initUI()
    def initUI(self): #access anywhere
        self.label = QtWidgets.QLabel(self)
        self.label.setText("HIIII")
        self.label.move(50,50)

        self.b1 = QtWidgets.QPushButton(self)
        self.b1.setText("Oless")
        self.b1.clicked.connect(self.clicked)
        
        self.label.setText("buoooom")
    def clicked(self):
        self.label.setText("button pressed")
        self.update()
    def update(self):
        self.label.adjustSize()

def window():
    app = QApplication(sys.argv)
    win = MyWindow()
    
    win.show()
    sys.exit(app.exec_())

window()