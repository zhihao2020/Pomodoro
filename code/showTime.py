# -*- coding:utf-8 -*-
from UI.ticktock import Ui_Form
import time
import logging
import sys,os
from PyQt5 import QtGui
from PyQt5.QtSql import QSqlDatabase,QSqlQuery,QSqlError
from PyQt5.QtCore import QThread,pyqtSignal,QTimer
from pygame import mixer
from PyQt5.QtWidgets import QApplication,QWidget,QMessageBox
import datetime

logging.basicConfig(filename='ProgramLog.log',level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')
class reload_showTime(QWidget,Ui_Form):
    showWin = pyqtSignal(bool)
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
        self.id = self.time.setInterval(1000)
        self.time.timeout.connect(self.Refresh)
        self.readData()

        self.db = QSqlDatabase.addDatabase('QSQLITE', "db")
        self.db.setDatabaseName('data.db')


    def readData(self):
        with open("apam.io", 'r') as fd:
            self.line = fd.readline()
            self.work = int(self.line.split(',')[0]) *60
            self.relax = int(self.line.split(',')[1]) *60
            self.count = (self.work+self.relax)

    def labelTime(self,nowTime):
        self.label.setText(nowTime)

    def playMusic(self,endFlag,loops=1,start=0.0,value=1,flag=0):
        # 音乐初始化
        mixer.init()
        if flag == 1:
            mixer.music.load(r"1.mp3")
        else:
            mixer.music.load(r"2.mp3")
        if endFlag:
            mixer.music.play(loops=loops,start=start)
            mixer.music.set_volume(value)
        else:
            mixer.stop()

    def init_daojiui(self):
        self.readData()
        self.now = datetime.datetime.now()
        self.time.start()
        self.pushButton_3.setEnabled(False)
        try:
            self.db.open()
        except QSqlError.ConnectionError:
            logging.error("没有连接数据库")
        self.query = QSqlQuery(self.db)

    def Refresh(self):
        if self.count > self.relax :
            print(1)
            goalTime = (self.now + datetime.timedelta(minutes=(self.work)/60)).strftime("%Y-%m-%d %H:%M:%S")
            self.label_2.setText(r"目标时间：" + goalTime)
            self.lcdNumber.display(self.count-self.relax )
            self.count -= 1

        elif self.count == self.relax:
            print(2)
            self.playMusic(True,flag=1)
            self.time.stop()
            self.query.exec_("insert into 倒计时(日期,持续时间) values('%s','%s')"
                             % (datetime.datetime.today().strftime('%Y-%m-%d'), self.line.split(',')[0]))
            logging.info("insert into 倒计时(日期,持续时间) values('%s','%s')"
                         % (datetime.datetime.today().strftime('%Y-%m-%d'), self.line.split(',')[0]))
            replay = QMessageBox.information(self, '提示', '工作时间结束，现在是否休息？', QMessageBox.Yes | QMessageBox.No)
            if replay == QMessageBox.Yes:
                self.count = -1
                self.now = datetime.datetime.now()
                self.time.start()
            else:
                self.pushButton_3.setEnabled(True)


        elif self.relax > 0:
            print(3)
            self.pushButton_3.setEnabled(False)
            goalTime = (self.now + datetime.timedelta(minutes=(int(self.line.split(',')[1]) *60) / 60)).strftime(
                "%Y-%m-%d %H:%M:%S")
            self.label_2.setText(r"目标时间：" + goalTime)
            self.lcdNumber.display(self.relax)
            self.relax -= 1

        elif self.relax == 0:
            print(4)
            self.query.exec_("insert into 倒计时(日期,持续时间) values('%s','%s')" % (
            datetime.datetime.today().strftime('%Y-%m-%d'), self.line.split(',')[1]))
            logging.info("insert into 倒计时(日期,持续时间) values('%s','%s')"
                         % (datetime.datetime.today().strftime('%Y-%m-%d'), self.line.split(',')[1]))

            self.playMusic(True)
            self.time.stop()
            replay = QMessageBox.information(self,'提示','休息时间结束，现在是否工作？',QMessageBox.Yes|QMessageBox.No)
            if replay == QMessageBox.Yes:
                self.playMusic(False)
                self.work = int(self.line.split(',')[0]) * 60
                self.relax = int(self.line.split(',')[1]) * 60
                self.count = (self.work + self.relax)
                self.now = datetime.datetime.now()
                self.time.start()
            else:
                self.pushButton_3.setEnabled(True)

    def pauseTimer(self):
        self.time.stop()

    def closeTimer(self):
        reply = QMessageBox.warning(self, '警示', '你就要关闭倒计时', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            self.time.stop()
            self.close()
            self.lcdNumber.display(0)
            self.pushButton_3.setEnabled(True)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.lcdNumber.display(0)
        self.pushButton_3.setEnabled(True)
        self.showWin.emit(True)
        self.db.close()


class WorkThread(QThread,Ui_Form):
    trigger = pyqtSignal(str)
    def __init__(self):
        super(WorkThread,self).__init__()

    def run(self):
        while True:
            nowTime = str("现在时间："+ datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
            self.trigger.emit(nowTime)
            time.sleep(1)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = reload_showTime()
    myWin.show()
    sys.exit(app.exec_())
