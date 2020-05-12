from UI.ticktock import Ui_Form
import time
from PyQt5.QtCore import QTimer

from PyQt5.QtWidgets import QWidget

class MyTimer(QWidget,Ui_Form):
    def __init__(self):
        super(MyTimer, self).__init__()
        self.setupUi(self)
        self.timer = QTimer()
        self.timer.timeout.connect(self.showTime)
        self.lcdNumber.setDigitCount(10)
        # 将按钮与对应函数绑定
        self.pushButton.clicked.connect(self.clearTimer)
        self.pushButton_2.clicked.connect(self.pauseTimer)
        self.pushButton_3.clicked.connect(self.startTimer)
        self.init()

    def init(self):
        self._start_time = 0
        self._pause_flag = False
        self._pause_time = 0
        self._restart_time = 0
        self._pause_total = 0
        self.lcdNumber.display(0)

    @property
    def _current_time(self):
        # 返回当前时间
        return time.time()

    def showTime(self):

        # 如果暂停标志为真，self._pause_total 属性要加上暂停时间
        # 并设置暂停标志为假
        if self._pause_flag:
            self._pause_total += self._restart_time - self._pause_time
            self._pause_flag = False
        # 计算运行时间
        run_time = self._current_time - self._pause_total - self._start_time
        self.lcdNumber.display(run_time)

    def startTimer(self):
        # 发出计时信号
        self.timer.start(0)
        # 如果 self._pause_flag 为真，更新开始时间
        # 否则，更新重启时间
        if not self._pause_flag:
            self._start_time = self._current_time
        else:
            self._restart_time = self._current_time

    def pauseTimer(self):
        self._pause_flag = True
        self._pause_time = self._current_time
        # 停止发送信号
        self.timer.stop()

    def clearTimer(self):
        # 还原至初始状态
        self.init()
        self.timer.stop()