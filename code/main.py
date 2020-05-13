# -*- coding:utf-8 -*-
import PyQt5.QtCore
from PyQt5.QtWidgets import QApplication,QMainWindow,QSystemTrayIcon,QAction,QMenu,QMessageBox
from PyQt5.QtCore import Qt,pyqtSignal,QCoreApplication
import sys,os
import matplotlib.pyplot as plt
from PyQt5 import QtGui
from PyQt5.QtGui import QIcon
import webbrowser
import pyautogui
from PyQt5.QtSql import QSqlDatabase,QSqlQuery
from UI.start import Ui_MainWindow
from showTime import reload_showTime
from Myjishiqi import MyTimer

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
        self.timer.showWin.connect(self.show)
        self.a.showWin.connect(self.show)
        self._rcwin = None
        #self.radioButton.toggled.connect(lambda:self.moveMouse(self.radioButton))

        self.db = QSqlDatabase.addDatabase('QSQLITE', "db2")
        self.db.setDatabaseName('data.db')
        self.db.open()

        if self.db.open() is None:
            print(QMessageBox.critical(self, "警告", "数据库连接失败，请查看数据库配置", QMessageBox.Yes))
        self.query = QSqlQuery(self.db)

    def aboutMe(self):
        webbrowser.open_new_tab('https://zhihao2020.github.io/about/')

    def moveMouse(self,Bool=False):
        while Bool:
            pyautogui.moveRel(0, -1, duration=2)
            pyautogui.moveRel(0, 1, duration=2)

    def showData(self):
        d = {}
        x = []
        y = []
        self.query.exec_("SELECT * from 倒计时 ")
        while (self.query.next()):
            keys = str(self.query.value(0))
            d[keys]=  int(self.query.value(1)) + int(d.get(keys,'0'))
            print(d[keys])
        for key in d.keys():
            x.append(key)
            y.append(d[key])
        print("数据加载完毕")
        plt.rcParams['font.family'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
        plt.xlabel("日期（天）")
        plt.ylabel("时间（min)")
        plt.ylim(ymin=0)
        plt.plot(x,y)
        plt.show()

    def dcjiui(self):
        with open("apam.io",'w') as fd:
            fd.write("%s,%s"%(self.spinBox.value(),self.spinBox_2.value()))
        #self.moveMouse(self.radioButton.isChecked())
        self.a.show()
        self.hide()

    def jiShi(self):
        self.timer.setWindowModality(Qt.ApplicationModal)
        self.timer.show()
        self.hide()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        reply = QMessageBox.warning(self, '警示', '你就关闭柠檬钟', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            QApplication.setQuitOnLastWindowClosed(True)
            self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    QApplication.setQuitOnLastWindowClosed(False)
    myWin = reload_mainWin()
    myWin.setWindowOpacity(0.9)
    myWin.show()
    tp = QSystemTrayIcon(myWin)
    tp.setIcon(QIcon(r'F:\Pomodoro\materials\lemon.ico'))
    a1 = QAction('&显示(Show)', triggered=myWin.show)

    def quitApp():
        myWin.show()  # w.hide() #隐藏
        re = QMessageBox.question(myWin, "提示", "退出系统", QMessageBox.Yes |
                                  QMessageBox.No, QMessageBox.No)
        if re == QMessageBox.Yes:
            QCoreApplication.instance().quit()
            tp.setVisible(False)

    a2 = QAction('&退出(Exit)', triggered=quitApp)  # 直接退出可以用qApp.quit

    tpMenu = QMenu()
    tpMenu.addAction(a1)
    tpMenu.addAction(a2)
    tp.setContextMenu(tpMenu)
    # 不调用show不会显示系统托盘
    tp.show()

    tp.showMessage('tp', 'tpContent', icon=0)


    sys.exit(app.exec_())
