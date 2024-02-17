import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from VideoPlayer import Ui_VideoPlayer
from ImagePlayer import Ui_ImagePlayer

class Page1(QWidget, Ui_VideoPlayer):
    def __init__(self):
        super(Page1, self).__init__()
        self.setupUi(self)
        self.menubar.menuImage_Player.clicked.connect(self.showPage2)

    def showPage2(self):
        self.page2 = Page2()
        self.page2.show()
        self.hide()

class Page2(QWidget, Ui_ImagePlayer):
    def __init__(self):
        super(Page2, self).__init__()
        self.setupUi(self)
        self.menubar.menuVideo_player.clicked.connect(self.showPage1)

    def showPage1(self):
        self.page1 = Page1()
        self.page1.show()
        self.hide()

