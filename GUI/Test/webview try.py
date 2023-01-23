import sys
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QDir, Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget 
from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, QTableWidget, QVBoxLayout, QTableWidgetItem, QHBoxLayout, QSplitter, QGroupBox)
from PyQt5.QtWebKit import *
from PyQt5.QtWebKitWidgets import *

class Window(QWidget):
    def __init__(self,):
        super().__init__()
        
        self.v_layout=QVBoxLayout(self)
        self.splitter=QSplitter(QtCore.Qt.Horizontal)
        self.left=QGroupBox('Left')
        self.table1=QTableWidget()
        self.table1.setRowCount(2)
        self.table1.setColumnCount(2)
        self.table1.setItem(0,0,QTableWidgetItem("Camera 1 (1,1)"))
        self.table1.setItem(0,1,QTableWidgetItem("Camera 2 (1,2)"))
        self.table1.setItem(1,0,QTableWidgetItem("TeamViewer (2,1)"))
        self.table1.setItem(1,1,QTableWidgetItem("Blank (2,2)"))
        
        self.left_layout=QVBoxLayout(self.left)
        self.left_layout.addWidget(self.table1)
        
        self.right=QGroupBox('Right')
        self.VideoWidget=QVideoWidget()
        
        self.player=QMediaPlayer(None,QMediaPlayer.VideoSurface)
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile("")))
        self.player.play()
        self.player.setVideoOutput(self.VideoWidget)
        
        self.webview=QWebView()
        url="https://www.google.com"
        self.webview.load(QUrl(url))
        
        self.right_layout=QVBoxLayout(self.right)
        self.right_layout.addWidget(self.webview)
        
        self.right_layout.addWidget(self.VideoWidget)
        self.splitter.addWidget(self.left)
        self.splitter.addWidget(self.right)
        
        self.v_layout.addWidget(self.splitter)
        
        self.resize(840,680)
        self.show()
        
if __name__ == '__main__':
    app=QApplication(sys.argv)
    window=Window()
    
    app.exec_()
        
