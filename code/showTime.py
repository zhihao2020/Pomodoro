from UI.ticktock import Ui_Form
import time,os
import sys
import shelve
from PyQt5.QtCore import QThread,pyqtSignal
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
        print('hello')
        self.init_daojiui()

    def labelTime(self,nowTime):
        self.label.setText(nowTime)

    def playMusic(self,loops=50,start=0.0,value=1):
        mixer.init()
        mixer.muxic.load("../materials/alarm.wav")
        mixer.music.play(loops=loops,start=start)
        mixer.music.set_volume(value)

    def init_daojiui(self):
        try:
            s = shelve.open("../materials/apam.db")
            work = s['work']
            relax = s['relax']
            s.close()
            os.unlink("../materials/apam")
            self.dcjiui(work)
            print(work)
            reply = QMessageBox.information(self, '提示', '工作时间结束，是否开始休息？', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if reply==QMessageBox.Yes:
                self.dcjiui(relax)
                reply = QMessageBox.information(self, '提示', '休息时间结束，是否开始工作？', QMessageBox.Yes | QMessageBox.No,
                                                QMessageBox.Yes)
                if reply == QMessageBox.Yes:
                    pass
        except:print("No")
    def dcjiui(self,hour=0,mins=0,second=0):
        seconds = int(hour * 3600 + mins * 60 + second)
        goalTime = (datetime.datetime.now() + datetime.timedelta(minutes=mins)).strftime("%Y-%m-%d %H:%M:%S")
        self.label_2.setText(r"目标时间："+goalTime)
        for i in reversed(range(0, seconds)):
            self.lcdNumber.display(i)
            time.sleep(1)
        self.playMusic()
        time.sleep(0.2)


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