from UI.ticktock import Ui_Form
import time
import sys
from PyQt5 import QtGui
from PyQt5.QtCore import QThread,pyqtSignal,QTimer
from pygame import mixer
from PyQt5.QtWidgets import QApplication,QWidget,QMessageBox
import datetime

class reload_showTime(QWidget,Ui_Form):

    def __init__(self):
        super(reload_showTime,self).__init__()
        self.setupUi(self)
        self.threads = WorkThread()
        self.threads.start()
        self.threads.trigger.connect(self.labelTime)
        self.pushButton_3.clicked.connect(self.init_daojiui)
        self.pushButton_2.clicked.connect(self.pauseTimer)
        self.pushButton.clicked.connect(self.closeTimer)
        self.time = QTimer(self)
        self.time.setInterval(1000)
        self.time.timeout.connect(self.Refresh)

    def labelTime(self,nowTime):
        self.label.setText(nowTime)

    def playMusic(self,loops=50,start=0.0,value=1):
        mixer.init()
        mixer.muxic.load("../materials/alarm.wav")
        mixer.music.play(loops=loops,start=start)
        mixer.music.set_volume(value)

    def Refresh(self):
        if self.count > self.relax :
            goalTime = (datetime.datetime.now() + datetime.timedelta(minutes=(self.count-self.relax)/60)).strftime("%Y-%m-%d %H:%M:%S")
            self.label_2.setText(r"目标时间：" + goalTime)
            self.lcdNumber.display(self.count-self.relax )
            self.count -= 1
        else:
            self.time.stop()
            self.pushButton_3.setEnabled(True)
            replay = QMessageBox.information(self,'提示','工作时间结束，现在是否休息？',QMessageBox.Yes|QMessageBox.No)
            if replay == QMessageBox.Yes:
                if self.relax > 0:
                    goalTime = (datetime.datetime.now() + datetime.timedelta(minutes=(self.relax) / 60)).strftime("%Y-%m-%d %H:%M:%S")
                    self.label_2.setText(r"目标时间：" + goalTime)
                    self.lcdNumber.display(self.relax)
                    self.relax -= 1
                else:
                    self.time.stop()
                    self.pushButton_3.setEnabled(True)
                    replay = QMessageBox.information(self, '提示', '休息时间结束，现在是否工作？', QMessageBox.Yes | QMessageBox.No)
                    if replay == QMessageBox.Yes:
                        self.work = int(self.line.split(',')[0]) * 60
                        self.relax = int(self.line.split(',')[1]) * 60
                        self.count = (self.work + self.relax)
                        self.Refresh()

    def init_daojiui(self):
        with open("../materials/apam.io", 'r') as fd:
            self.line = fd.readline()
            self.work = int(self.line.split(',')[0]) *60
            self.relax = int(self.line.split(',')[1]) *60
            #print(work, relax)
            self.count = (self.work+self.relax)
        self.time.start()
        self.pushButton_3.setEnabled(False)

    def pauseTimer(self):
        self.time.stop()

    def closeTimer(self):
        reply = QMessageBox.warning(self, '警示', '你就关闭柠檬钟', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            self.time.stop()
            self.close()
            self.lcdNumber.display(0)
            self.pushButton_3.setEnabled(True)


class WorkThread(QThread,Ui_Form):
    trigger = pyqtSignal(str)
    def __init__(self):
        super(WorkThread,self).__init__()

    def run(self):
        while True:
            nowTime = str("现在时间："+ datetime.datetime.today().strftime('%Y %B %dd %Hh %Mm %Ss'))
            self.trigger.emit(nowTime)
            time.sleep(1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = reload_showTime()
    myWin.show()
    sys.exit(app.exec_())