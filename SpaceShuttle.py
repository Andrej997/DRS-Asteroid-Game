from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QGraphicsTransform
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, QBasicTimer, QRectF
from PyQt5.QtWidgets import QLabel, QApplication, QGridLayout, QWidget, QVBoxLayout, QGraphicsView, QGraphicsScene
from PyQt5.QtGui import QPixmap, QTransform
from math import cos, sin, radians
from Bullet import Bullet
from PauseWindow import *
import Server
import math

rocketsList = ['Images/rocketship.png', 'Images/rocketship (1).png', 'Images/rocketship (3).png',
               'Images/rocketship (4).png', 'Images/rocketship (5).png', 'Images/rocketship (6).png',
               'Images/rocketship (7).png', 'Images/rocketship (8).png', 'Images/rocketship (9).png',
               'Images/rocketship (10).png', 'Images/rocketship (11).png', 'Images/rocketship (12).png',
               'Images/rocketship (13).png', 'Images/rocketship (14).png', 'Images/rocketship (15).png',
               'Images/rocketship (16).png', 'Images/rocketship (17).png', 'Images/rocketship (18).png',
               'Images/rocketship (19).png', 'Images/rocketship (20).png', 'Images/rocketship (21).png',
               'Images/rocketship (2).png', 'Images/rocketship (22).png', 'Images/rocketship (23).png',
               'Images/rocketship (24).png', 'Images/rocketship (25).png', 'Images/rocketship (26).png',
               'Images/rocketship (27).png', 'Images/rocketship (28).png', 'Images/rocketship (29).png',
               'Images/rocketship (30).png', 'Images/rocketship (31).png', 'Images/rocketship (32).png',
               'Images/rocketship (33).png', 'Images/rocketship (34).png', 'Images/rocketship (35).png',
               'Images/rocketship (36).png', 'Images/rocketship (37).png', 'Images/rocketship (38).png',
               'Images/rocketship (39).png', 'Images/rocketship (40).png', 'Images/rocketship (41).png',
               'Images/rocketship (42).png', 'Images/rocketship (43).png', 'Images/rocketship (44).png',
               'Images/rocketship (45).png', 'Images/rocketship (46).png', 'Images/rocketship (47).png',
               'Images/rocketship (48).png', 'Images/rocketship (49).png', 'Images/rocketship (50).png',
               'Images/rocketship (51).png', 'Images/rocketship (52).png', 'Images/rocketship (53).png',
               'Images/rocketship (54).png', 'Images/rocketship (55).png', 'Images/rocketship (56).png',
               'Images/rocketship (56).png', 'Images/rocketship (57).png', 'Images/rocketship (58).png',
               'Images/rocketship (59).png', 'Images/rocketship (60).png', 'Images/rocketship (61).png',
               'Images/rocketship (62).png', 'Images/rocketship (63).png', 'Images/rocketship (64).png',
               'Images/rocketship (65).png', 'Images/rocketship (66).png', 'Images/rocketship (67).png',
               'Images/rocketship (68).png', 'Images/rocketship (69).png', 'Images/rocketship (70).png',
               'Images/rocketship (71).png']
paused = 1
counter = 0


class SpaceShuttle(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.w = 600
        self.h = 500
        self.rect().center()
        self.setFixedSize(self.w, self.h)
        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(QRectF(0, -220, 590, 490))
        self.setScene(self.scene)
        #self.mover = Mover(270, 0, self.scene)
        self.mover = Mover(270, 0)
        self.labels = QLabel()
        self.pixmap = QPixmap('Images/img.png')
        self.labels.setPixmap(self.pixmap)
        self.labels.resize(600, 500)
        self.labels.move(-5,-225)
        #self.label.show()
        self.scene.addWidget(self.labels)
        self.scene.addWidget(self.mover)
        #self.mover.setPixmap(QPixmap('Images/img.png'))
        self.init()

    def init(self):
        self.mover.initialize()
        self.show()
    
    def keyPressEvent(self, event):
        self.mover.KeyPressEvent(event, self.scene)
    

class Mover(QtWidgets.QLabel):
    moveImg = pyqtSignal(QGraphicsScene)

    def __del__(self):
        print("Mover deleted")

    def __init__(self, w, h, player):
        super().__init__()
        global rocketsList
        self.i = 1
        self.myLives = 3
        self.score = 0
        self.meci = []
        self.moveX = float(0)
        self.moveY = float(1)
        self.xFull = float(w)
        self.yFull = float(h)
        self.angle = 90
        self.move(w, h)
        self.setPixmap(QPixmap('Images/img.png'))
        if player == 1:
            self.moveImg.connect(self.KeyPressEvent1)
        else:
            self.moveImg.connect(self.KeyPressEvent2)
        self.setStyleSheet("background-color: transparent")
        self.timer = QBasicTimer()
        self.timer.start(30, self)
        self.setMoverImage(rocketsList[self.i])
        self.pause = PauseWindow(self)        
        

    def setMoverImage(self, param):
        self.setPixmap(QtGui.QPixmap(param))

    def KeyPressEvent1(self, event, q: QGraphicsScene):
        global rocketsList
        global paused

        xxx = int(round(self.x()))
        yyy = int(round(self.y()))
        Server.initialize()
        print(Server.rocket1IsDestroyed)
        
        Server.rocket1xCoordinates = xxx
        Server.rocket1yCoordinates = yyy

        print(Server.rocket1xCoordinates)
        print(Server.rocket1yCoordinates)

        if event.key() == QtCore.Qt.Key_Left:
            self.i = (self.i + 1) % 72
            self.setMoverImage(rocketsList[self.i])
            self.angle = self.angle + 5
            self.moveX = cos(radians(self.angle))
            self.moveY = sin(radians(self.angle))
        elif event.key() == QtCore.Qt.Key_Right:
            self.i = (self.i - 1) % 72
            self.angle = self.angle - 5
            self.setMoverImage(rocketsList[self.i])
            self.moveX = cos(radians(self.angle))
            self.moveY = sin(radians(self.angle))
        elif event.key() == QtCore.Qt.Key_Up:
            self.yFull = float(self.yFull).__sub__(self.moveY * 5)
            self.xFull = float(self.xFull).__add__(self.moveX * 5)
            # round(self.geometry().x(),2) + round(self.moveX,2)
            # round(self.geometry().y(),2) - round(self.moveY,2)
            self.move(self.xFull, self.yFull)
#            print(self.xFull, self.yFull)
            if (math.floor(self.yFull) <= -250):
                self.yFull = (self.yFull * -1) - 1.0
            elif (math.floor(self.yFull) >= 250):
                self.yFull = (self.yFull * -1) + 1.0
            elif (math.floor(self.xFull) <= -22):
                self.xFull = 559
            elif (math.floor(self.xFull) >= 560):
                self.xFull = -21.0
            # ovde treba za gas logika
        elif event.key() == QtCore.Qt.Key_0:
            metak = Bullet(self.x(), self.y(), self.angle, i, q)
            self.meci.append(metak)
        elif event.key() == QtCore.Qt.Key_Escape:
            self.hide()
            self.pause.show()
        else:
            QtWidgets.QLabel.keyPressEvent(self, event)
        self.update()
    
    def KeyPressEvent2(self, event, q: QGraphicsScene):
        global rocketsList
        global paused

        xxx = int(round(self.x()))
        yyy = int(round(self.y()))
        Server.initialize()
        print(Server.rocket1IsDestroyed)
        
        Server.rocket1xCoordinates = xxx
        Server.rocket1yCoordinates = yyy

        print(Server.rocket1xCoordinates)
        print(Server.rocket1yCoordinates)

        if event.key() == QtCore.Qt.Key_A:
            self.i = (self.i + 1) % 72
            self.setMoverImage(rocketsList[self.i])
            self.angle = self.angle + 5
            self.moveX = cos(radians(self.angle))
            self.moveY = sin(radians(self.angle))
        elif event.key() == QtCore.Qt.Key_D:
            self.i = (self.i - 1) % 72
            self.angle = self.angle - 5
            self.setMoverImage(rocketsList[self.i])
            self.moveX = cos(radians(self.angle))
            self.moveY = sin(radians(self.angle))
        elif event.key() == QtCore.Qt.Key_W:
            self.yFull = float(self.yFull).__sub__(self.moveY * 5)
            self.xFull = float(self.xFull).__add__(self.moveX * 5)
            # round(self.geometry().x(),2) + round(self.moveX,2)
            # round(self.geometry().y(),2) - round(self.moveY,2)
            self.move(self.xFull, self.yFull)
#            print(self.xFull, self.yFull)
            if (math.floor(self.yFull) <= -250):
                self.yFull = (self.yFull * -1) - 1.0
            elif (math.floor(self.yFull) >= 250):
                self.yFull = (self.yFull * -1) + 1.0
            elif (math.floor(self.xFull) <= -22):
                self.xFull = 559
            elif (math.floor(self.xFull) >= 560):
                self.xFull = -21.0
            # ovde treba za gas logika
        elif event.key() == QtCore.Qt.Key_G:
            metak = Bullet(self.x(), self.y(), self.angle, i, q)
            self.meci.append(metak)
        elif event.key() == QtCore.Qt.Key_Escape:
            self.hide()
            self.pause.show()
        else:
            QtWidgets.QLabel.keyPressEvent(self, event)
        self.update()

    def timerEvent(self, a0: 'QTimerEvent'):
        global Server
        if len(self.meci) > 0:
            for metak in self.meci:
                metak.kreni.emit()
        #if (Server.rocket1IsDestroyed == 2):
         #   self.hide()  
         #   del self.meci
        #    del self     
            
            
            
            