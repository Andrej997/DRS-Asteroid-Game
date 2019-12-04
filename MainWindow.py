from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor
import sys
import multiprocessing as mp
import time

def changeWindow(w1, w2):
        w2.show()
        w1.hide()

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        
        self.newGameWindow = NewGameWindow()
        #self.setStyleSheet("background-image: url(C:\\Users\\Mistra\\Desktop\\Pajton\\vjezba\\asteroid.jpg)")
        self.setStyleSheet("background-color:black")
        self.setWindowTitle("Asteroids")
        self.setGeometry(300, 150, 600, 500)
        
        mainLabel = QLabel("ASTEROIDS", self)
        mainLabel.resize(200,100)
        mainLabel.setStyleSheet("color: white; font-size:32px; font:bold")
        mainLabel.move(200, 0)

        
        newGameBtn = QPushButton("New Game", self)
        newGameBtn.setStyleSheet("color: white; background-color: transparent; font:bold; border-style: outset; border-width: 2px; border-color: white")
        newGameBtn.resize(100, 50)
        newGameBtn.move(250, 100)
        newGameBtn.clicked.connect(self.startNewGameWindow)

        aboutGameBtn = QPushButton("About game", self)
        aboutGameBtn.setStyleSheet("color: white; background-color: transparent; font:bold; border-style: outset; border-width: 2px; border-color: white")
        aboutGameBtn.resize(100, 50)
        aboutGameBtn.move(250, 165)

        exitBtn = QPushButton("Exit game", self)
        exitBtn.setStyleSheet("color: white; background-color: transparent; font:bold; border-style: outset; border-width: 2px; border-color: white")
        exitBtn.resize(100, 50)
        exitBtn.move(250, 230)
        exitBtn.clicked.connect(self.close)
     
        # The `Qt` namespace has a lot of attributes to customise
        # widgets. See: http://doc.qt.io/qt-5/qt.html
        #label.setAlignment(Qt.AlignCenter)

        # Set the central widget of the Window. Widget will expand
        # to take up all the space in the window by default.
        #self.setCentralWidget(label)

    def close(self):
        app.closeAllWindows()

    def startNewGameWindow(self):
        changeWindow(window, window1)
        
    
class NewGameWindow(QMainWindow):
    def __init__(self):
        super(NewGameWindow, self).__init__()
        self.setStyleSheet("background-color:black")
        self.setWindowTitle("Asteroids")
        self.setGeometry(300, 150, 600, 500)

        mainLabel = QLabel("Chose game mode", self)
        mainLabel.resize(300, 100)
        mainLabel.setStyleSheet("color: white; font-size:32px; font:bold")
        mainLabel.move(150, 0)

        singlPlyBtn = QPushButton("Single player", self)
        singlPlyBtn.setStyleSheet("color: white; background-color: transparent; font:bold; border-style: outset; border-width: 2px; border-color: white")
        singlPlyBtn.resize(100, 50)
        singlPlyBtn.move(250, 100)

        multiPlyBtn = QPushButton("Multiplayer", self)
        multiPlyBtn.setStyleSheet("color: white; background-color: transparent; font:bold; border-style: outset; border-width: 2px; border-color: white")
        multiPlyBtn.resize(100, 50)
        multiPlyBtn.move(250, 165)
        
        returnBtn = QPushButton("Return", self)
        returnBtn.setStyleSheet("color: white; background-color: transparent; font:bold; border-style: outset; border-width: 2px; border-color: white")
        returnBtn.resize(100, 50)
        returnBtn.move(250, 230)

        returnBtn.clicked.connect(self.returnToMain)

    def returnToMain(self):
        changeWindow(window1, window)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window1 = NewGameWindow()
    app.exec_()