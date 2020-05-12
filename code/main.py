from PyQt5.QtWidgets import QApplication,QMainWindow
from PyQt5.QtCore import Qt,pyqtSignal
import sys
import shelve
import time
import pyautogui
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

        self._rcwin = None

    def aboutMe(self):
        webbrowser.open_new_tab('https://zhihao2020.github.io/about/')

    def moveMouse(self,Bool=False):
        while Bool:
            pyautogui.moveRel(0, -10000, duration=2)
            pyautogui.moveRel(0, 10, duration=2)

    def showData(self):
        pass

    def dcjiui(self):
        with open("../materials/apam.io",'w') as fd:
            fd.write("%s,%s"%(self.spinBox.value(),self.spinBox_2.value()))
        #self.moveMouse(self.radioButton.isChecked())
        self.a.show()
        self.showMinimized()

    def jiShi(self):
        self.timer.setWindowModality(Qt.ApplicationModal)
        self.timer.show()
        self.showMinimized()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = reload_mainWin()
    myWin.show()
    sys.exit(app.exec_())
