from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox,QApplication
import sys
from PyQt5.QtCore import pyqtSignal,QThread
import json
import requests
import shutil
import psutil
import os
import zipfile

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(412, 136)
        Form.setMinimumSize(QtCore.QSize(412, 136))
        Form.setMaximumSize(QtCore.QSize(412, 136))
        font = QtGui.QFont()
        font.setFamily("AcadEref")
        font.setPointSize(12)
        Form.setFont(font)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.progressBar = QtWidgets.QProgressBar(Form)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.progressBar.setFormat("")
        self.progressBar.setObjectName("progressBar")
        self.horizontalLayout.addWidget(self.progressBar)
        self.pushButton = QtWidgets.QPushButton(Form)
        font = QtGui.QFont()
        font.setFamily("AcadEref")
        font.setPointSize(12)
        self.pushButton.setFont(font)
        self.pushButton.setIconSize(QtCore.QSize(20, 20))
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "????????????"))
        self.label.setText(_translate("Form", "???????????????????????????ing..."))
        self.pushButton.setText(_translate("Form", "??????"))

class AppUI(QtWidgets.QWidget,Ui_Form):
    download_proess_signal = pyqtSignal(int)
    def __init__(self):
        super(AppUI,self).__init__()
        self.setupUi(self)
        self.thread = Thread()
        self.thread.start()
        self.thread.trigger.connect(self.refresh)
        self.thread.End_signal.connect(self.quit)
        self.thread.Error_signal.connect(self.quit)
        self.thread.Button_signal.connect(self.Button)
        self.thread.New_signal.connect(self.quit)
        self.pushButton.clicked.connect(self.closeEvent)

    def refresh(self,num):
        self.progressBar.setValue(num)

    def Button(self,flag):
        if flag:
            self.pushButton.setEnabled(False)
    def closeEvent(self,Event) -> None:
        sys.exit(app.exec_())

    def quit(self,num):
        if num == 1:
            QMessageBox.information(self,"??????","???????????????????????????",QMessageBox.Yes)
        elif num == 2:
            QMessageBox.warning(self, "??????", "??????????????????????????????", QMessageBox.Yes)
        elif num==3:
            QMessageBox.information(self,'??????','???????????????????????????', QMessageBox.Yes)
        self.close()

class Thread(QThread,Ui_Form):
    New_signal = pyqtSignal(int)
    trigger = pyqtSignal(int)
    End_signal = pyqtSignal(int)
    Error_signal = pyqtSignal(int)
    Button_signal = pyqtSignal(bool)
    def __init__(self):
        super(Thread,self).__init__()
        self.download_path = os.getcwd()
        self.latest_tag=None

    def run(self):
        try:
            download_url, file_size = self.check_latest()
            self.kill_process()
            self.download(download_url, file_size)
            self.Button_signal.emit(True)
            self.unzip()
            with open("softID.io", 'w') as f:
                f.write(self.latest_tag)
            self.End_signal.emit(1)
        except TypeError:
            self.Error_signal.emit(2)
    def check_latest(self):
        # ????????????????????????????????????
        params = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36",
            "Host": "api.github.com"}
        try:
            response = requests.get("https://api.github.com/repos/zhihao2020/Pomodoro/releases/latest", params=params)
            if response.status_code != 200:
                raise Exception("????????????")
            temp = json.loads(response.text)
            self.latest_tag = temp["tag_name"]
            print(self.latest_tag)
            if not os.path.exists("softID.io"):
                file = open("softID.io","w")
                file.close()
            with open("softID.io",'r') as f:
                previous_tag = f.readline()
            if self.latest_tag != previous_tag:
                download_url = temp["assets"][0]['browser_download_url']
                file_size = temp['assets'][0]['size']
                return download_url,file_size
            else:
                self.New_signal.emit(3)
        except requests.exceptions.ConnectionError:
            print("??????????????????")

    def kill_process(self):
        for proc in psutil.process_iter():
            if proc.name()=='Pomodoro.exe':
                proc.kill()            
                    
    def download(self,download_url,file_size):
        print("downloading ....")
        temp_file = os.path.join(self.download_path,'update.zip')
        params = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36"}
        with open(temp_file,'wb') as self.fileobj:
            f = requests.get(download_url,stream=True,params=params)
            offset = 0
            for chunk in f.iter_content(chunk_size=1024):
                if not chunk:
                    break
                self.fileobj.seek(offset)
                self.fileobj.write(chunk)
                offset = offset+len(chunk)
                proess = offset/int(file_size) * 100
                self.trigger.emit(int(proess))

    def unzip(self):
        self.kill_process()
        current_path = os.path.dirname(os.path.abspath(__file__))
        update_file_path = os.path.join(self.download_path, 'update.zip')
        with zipfile.ZipFile(update_file_path) as fd:
            for n in fd.namelist():
                try:
                    os.remove(n)
                except:
                    try:
                        shutil.rmtree(n)
                    except:
                        print(n)
        shutil.unpack_archive(
            filename=update_file_path,
            extract_dir=current_path
        )
        os.remove(update_file_path)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = AppUI()
    myWin.show()
    sys.exit(app.exec_())
