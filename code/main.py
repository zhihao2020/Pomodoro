# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import QApplication,QMainWindow,QSystemTrayIcon,QAction,QMenu,QMessageBox
from PyQt5.QtCore import Qt,pyqtSignal,QCoreApplication
import sys,os
from PyQt5 import QtGui
from PyQt5.QtGui import QIcon
import webbrowser
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

        self._rcwin = None

    def aboutMe(self):
        webbrowser.open_new_tab('https://zhihao2020.github.io/about/')

    #def moveMouse(self,Bool=False):
     #   while Bool:
     #       pyautogui.moveRel(0, -10000, duration=2)
     #       pyautogui.moveRel(0, 10, duration=2)

    def showData(self):
        pass

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
        reply = QMessageBox.warning(self, '警示', '你就关闭柠檬钟', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            QApplication.setQuitOnLastWindowClosed(True)
            self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    QApplication.setQuitOnLastWindowClosed(False)
    myWin = reload_mainWin()
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
