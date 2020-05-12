from PyQt5.QtWidgets import QApplication,QMainWindow
from PyQt5.QtCore import Qt,pyqtSignal
import sys
import shelve
import time
import webbrowser
from UI.start import Ui_MainWindow
from code.showTime import reload_showTime
from code.Myjishiqi import MyTimer
import logging

class reload_mainWin(QMainWindow,Ui_MainWindow):
    daojishiSignal = pyqtSignal(list)
    def __init__(self):
        super(reload_mainWin,self).__init__()
        self.setupUi(self)

        self.action_3.triggered.connect(self.aboutMe)
        self.action.triggered.connect(self.showData)
        self.action_2.triggered.connect(self.jiShi)
        self.pushButton.clicked.connect(self.dcjiui)
        self.timer = MyTimer()
        self.a =reload_showTime()

    def aboutMe(self):
        webbrowser.open_new_tab('https://zhihao2020.github.io/about/')

    def showData(self):
        pass

    def dcjiui(self):
        reload_showTime()
        with shelve.open("../materials/apam") as db:
            db['work'] = self.spinBox.value()
            db['relax'] = self.spinBox_2.value()
        self.a.show()

    def jiShi(self):
        self.timer.setWindowModality(Qt.ApplicationModal)
        self.timer.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = reload_mainWin()

    myWin.show()
    sys.exit(app.exec_())
