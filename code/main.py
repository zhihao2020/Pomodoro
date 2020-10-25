# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import QApplication,QMainWindow,QSystemTrayIcon,QAction,QMenu,QMessageBox
from PyQt5.QtCore import Qt,pyqtSignal
import sys
from PyQt5 import QtGui
from PyQt5.QtGui import QIcon
import logging
import webbrowser
from UI.start import Ui_MainWindow
from showTime import reload_showTime
from Myjishiqi import MyTimer
import subprocess
logging.basicConfig(filename='ProgramLog.log',level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
class reload_mainWin(QMainWindow,Ui_MainWindow):
    daojishiSignal = pyqtSignal(list)

    def __init__(self):
        super(reload_mainWin,self).__init__()
        self.setupUi(self)
        QApplication.setQuitOnLastWindowClosed(False)
        self.action_3.triggered.connect(self.aboutMe)
        self.action.triggered.connect(self.showData)
        self.action_2.triggered.connect(self.jiShi)
        self.pushButton.clicked.connect(self.dcjiui)
        self.timer = MyTimer()
        self.a =reload_showTime()
        self.timer.showWin.connect(self.show)
        self.a.showWin.connect(self.show)
        self._rcwin = None
        self.action_4.triggered.connect(self.IDupdate)

    def IDupdate(self):
        reply = QMessageBox.information(self,"提示","是否升级该软件？",QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
        if reply == QMessageBox.Yes:
                #运行update.exe
                subprocess.call("update.exe",shell=True)

    def aboutMe(self):
        webbrowser.open_new_tab('https://xuzhihao.top/about/')

    def showData(self):
        QMessageBox.information(self,"提示","数据统计下一版本更新")

    def dcjiui(self):
        with open("apam.io",'w') as fd:
            if self.radioButton.isChecked():
                fd.write("%s,%s,%d"%(self.spinBox.value(),self.spinBox_2.value(),1))
            else:
                fd.write("%s,%s,%d" % (self.spinBox.value(), self.spinBox_2.value(), 0))
        self.a.show()
        self.hide()

    def jiShi(self):
        self.timer.setWindowModality(Qt.ApplicationModal)
        self.timer.show()
        self.hide()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        reply = QMessageBox.warning(self, '警示', '你打算关闭柠檬钟？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            QApplication.setQuitOnLastWindowClosed(True)
            self.close()

    def quit_app(self):
        re = QMessageBox.question(self, "提示", "退出系统", QMessageBox.Yes |
                                  QMessageBox.No, QMessageBox.No)
        if re == QMessageBox.Yes:
            sys.exit(app.exec_())

    def trayIcon(self):
        tp = QSystemTrayIcon(self)
        tp.setIcon(QIcon(r'F:\Pomodoro\materials\lemon.ico'))
        a1 = QAction('&显示(Show)', triggered=self.show)
        a2 = QAction('&退出(Exit)', triggered=self.quit_app)  # 直接退出可以用qApp.quit

        tpMenu = QMenu()
        tpMenu.addAction(a1)
        tpMenu.addAction(a2)
        tp.setContextMenu(tpMenu)
        # 不调用show不会显示系统托盘
        tp.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    myWin = reload_mainWin()
    myWin.setWindowOpacity(0.9)
    myWin.show()
    sys.exit(app.exec_())
