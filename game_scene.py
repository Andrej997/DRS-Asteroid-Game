from SpaceShuttle import *
from Asteroid import *
from bonus import *
from game_over_scene import *
from welcome_scene import *
from main import *
from PyQt5.QtCore import pyqtSignal, QBasicTimer, QRectF, QPoint, QTimerEvent, Qt, pyqtSlot
import multiprocessing as mp
from threading import Thread
import time
import random
from key_notifier import KeyNotifier
#from checker import Checker

activeBigAsteroids = []
activeMediumAsteroids = []
activeSmallAsteroids = []


class GameScene(QGraphicsScene):
    create_signal = pyqtSignal("""int""")

    def __init__(self, parent, width, height, num_of_players):
        super().__init__(parent)
        global activeBigAsteroids
        global activeMediumAsteroids
        global activeSmallAsteroids
        self.create_signal = pyqtSignal("""int""")
        self.width = width
        self.height = height
        self.setSceneRect(0, 0, self.width-2, self.height-2)
        self.sceneParent = parent#
        self.players_number = num_of_players
        self.queue = mp.Queue()
        self.firstrelease = False
        self.keyList = []
        self.timer = QBasicTimer()
        self.timer.start(2000, self)

        self.key_notifier = KeyNotifier()
        self.key_notifier.key_signal.connect(self.__update_position__)
        self.key_notifier.start()

        self.label = QLabel()
        self.pixmap = QPixmap('Images/img.png')
        self.label.setPixmap(self.pixmap)
        self.label.resize(600, 500)
        self.addWidget(self.label)

        # self.bonus = None

        self.rocketnumber1 = SpaceShuttle(self.width, self.height, self, 1)
        self.rocketnumber1.resize(60, 50)#slika je 50x50 ali se glupo okrece tako da je bolje ovako da bi se uvek videla cela
        self.rocketnumber1.setStyleSheet("background:transparent")
        self.addWidget(self.rocketnumber1)

        if self.players_number == 2:
            self.rocketnumber2 = SpaceShuttle(self.width, self.height, self, 2)
            self.rocketnumber2.resize(60,
                                      50)  # slika je 50x50 ali se glupo okrece tako da je bolje ovako da bi se uvek videla cela
            self.rocketnumber2.setStyleSheet("background:transparent")
            self.addWidget(self.rocketnumber2)


        self.queue.put('go')
        self.createAsteroids()

        """tt = Thread(target=self.checkAstDickt)
        tt.daemon = True
        tt.start()"""

        #self.asteroidChecker = Checker()

        print("DONE")

        self.label2 = QLabel(
            "Player1 lives--->[" + Server.player1Lives.__str__() + "] score--->[" + Server.player1Score.__str__() + "]")
        self.label2.resize(400, 30)
        self.label2.move(5, 440)
        self.label2.setStyleSheet("font: 12pt; color: #f03a54; font:bold; background-color: transparent; ")
        self.addWidget(self.label2)

        self.label3 = QLabel(
            "Player2 lives--->[" + Server.player2Lives.__str__() + "] score--->[" + Server.player2Score.__str__() + "]")
        self.label3.resize(400, 30)
        self.label3.move(5, 470)
        self.label3.setStyleSheet("font: 12pt; color: yellow; font:bold; background-color: transparent; ")
        self.addWidget(self.label3)

        self.label4 = QLabel("Level : " + Server.level.__str__())
        self.label4.resize(400, 30)
        self.label4.move(500, 10)
        self.label4.setStyleSheet("font: 12pt; color: white; font: bold; background-color: transparent;")
        self.addWidget(self.label4)


    def createAsteroids(self):
        o = Server.activeAsteroids.__len__()
        for o in range(Server.level):
            self.asteroid_0 = Asteroid(self.width, self.height, self, o.__str__())
            self.asteroid_0.setFocus()  # mozda i ne mora posto je timer tamo
            self.asteroid_0.setStyleSheet("background:transparent")
            self.asteroid_0.resize(60, 50)
            self.addWidget(self.asteroid_0)
            activeBigAsteroids.append(self.asteroid_0)
            Server.activeAsteroids[o.__str__()] = 0

    def game_is_over(self):#ako je game over
        self.gameOverScene = GameOver(self, self.width, self.height)
        self.gameOverScene.returnBtn.clicked.connect(self.menus)
        self.sceneParent.setScene(self.gameOverScene)

    def menus(self):
        self.sceneParent.ExitGame()


    def checkAstDickt(self):
        while True:
            time.sleep(0.5)
            if Server.activeAsteroids.__len__() > 0:
                counterActAst = 0
                for ast in Server.activeAsteroids:
                    if (Server.activeAsteroids[ast] == 1):
                        counterActAst = counterActAst + 1
                if counterActAst == Server.activeAsteroids.__len__():
                    Server.level = Server.level + 1
                    Server.create = True
                else :
                    Server.create = False
            if (Server.create == True):
                for ast in Server.activeAsteroids:
                    Server.activeAsteroids[ast.__str__()] = 0
                o = Server.activeAsteroids.__len__()
                Server.activeAsteroids.clear()
                print(Server.activeAsteroids.__str__())
                #self.createAsteroids()
                """for o in range(Server.level):
                    self.asteroid_0 = Asteroid(self.width, self.height, self, o.__str__())
                    self.asteroid_0.setFocus()  # mozda i ne mora posto je timer tamo
                    self.asteroid_0.setStyleSheet("background:transparent")
                    self.asteroid_0.resize(60, 50)
                    print("OVDE PUKNEM")
                    self.addWidget(self.asteroid_0)
                    activeBigAsteroids.append(self.asteroid_0)
                    Server.activeAsteroids[o.__str__()] = 0"""
                #Server.create = False

    def keyPressEvent(self, event):
        self.key_notifier.add_key(event.key())

    def keyReleaseEvent(self, event):
        self.key_notifier.rem_key(event.key())

    def __update_position__(self, key):
        # time.sleep(1)
        #print("MARKO test")
        if key == Qt.Key_W and self.players_number == 2:
            self.rocketnumber2.upRocket2.emit()
        elif key == Qt.Key_A and self.players_number == 2:
            self.rocketnumber2.leftRocket2.emit()
        elif key == Qt.Key_D and self.players_number == 2:
            self.rocketnumber2.rightRocket2.emit()
        elif key == Qt.Key_S and self.players_number == 2:
            self.rocketnumber2.fireRocket2.emit()
        elif key == Qt.Key_Up:
            self.rocketnumber1.upRocket1.emit()
        elif key == Qt.Key_Right:
            self.rocketnumber1.rightRocket1.emit()
        elif key == Qt.Key_Left:
            self.rocketnumber1.leftRocket1.emit()
        elif key == Qt.Key_Space:
            self.rocketnumber1.fireRocket1.emit()

    def timerEvent(self, a0: 'QTimerEvent'):#timer je na 2 sekunde gore, zato su ove provere, tako da se na svakih 30 sekundi stvori bonus i da igrac ima 2 sekunde da stane na njega pa se vrsi provera i resetuje se
        if Server.bonus_time < 15:
            Server.bonus_time = Server.bonus_time + 1
        elif Server.bonus_time == 15:
            Server.bonus_x_coordinate = random.randrange(0, 500)
            Server.bonus_y_coordinate = random.randrange(0, 450)
            Server.bonus_x_expanded.clear()
            Server.bonus_y_expanded.clear()
            tmpXX = 0
            for tmpXX in range(50):
                Server.bonus_x_expanded.append(tmpXX + Server.bonus_x_coordinate)#prosirivanje koordinata bonusa
            tmpYY = 0
            for tmpYY in range(50):
                Server.bonus_y_expanded.append(tmpYY + Server.bonus_y_coordinate)#prosirivanje koordinata bonusa
            self.bonus = Bonus(self.width, self.height, Server.bonus_x_coordinate, Server.bonus_y_coordinate, self)
            self.bonus.setStyleSheet("background:transparent")
            self.addWidget(self.bonus)
            Server.bonus_time = Server.bonus_time + 1
        elif Server.bonus_time == 16:
            if (any(checkXCords in Server.bonus_x_expanded for checkXCords in Server.coordinatesOfRocketsX) and any(
                    checkYCords in Server.bonus_y_expanded for checkYCords in Server.coordinatesOfRocketsY)):
                    Server.player1Lives = Server.player1Lives + 1
                    self.label2.setText("Player1 lives--->[" + Server.player1Lives.__str__() + "] score--->[" + Server.player1Score.__str__() + "]")
            self.bonus.hide()
            self.bonus.move(1234, 1234)
            Server.bonus_time = 0