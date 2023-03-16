import base64
import sys

import cv2
import numpy as np
from PyQt5.QtCore import *
import PyQt5.QtGui as QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
import pynput



class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def run(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, cv_img = cap.read()
            if ret:
                self.change_pixmap_signal.emit(cv_img)

    def receive_frame(client_socket):
        BUFF_SIZE = 524288
        full_packet, _ = client_socket.recvfrom(BUFF_SIZE)
        udp_header = full_packet[:8]
        packet = full_packet[8:]
        data = base64.b64decode(packet, ' /')
        stringData = np.frombuffer(data, dtype=np.uint8)
        frame = cv2.imdecode(stringData, 1)
        return frame


class Window(QWidget):
    # states: 0=manual, 1=hand gesture, 2=object tracking, 3=temporary disable
    states = 0

    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 800, 600)
        self.display_width = 800
        self.display_height = 600

        grid = QGridLayout()

        self.button_emerg_stop = QPushButton()
        self.button_emerg_stop.setText("STOP")
        self.button_emerg_stop.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.button_emerg_stop.clicked.connect(self.emerg_stop)
        grid.addWidget(self.button_emerg_stop, 5, 5, 2, 2)

        self.buttonForward = QPushButton()
        self.buttonStop = QPushButton()
        self.buttonTurnLeft = QPushButton()
        self.buttonTurnRight = QPushButton()

        self.buttonForward.setText("Forward")
        self.buttonForward.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.buttonForward.clicked.connect(self.forward_was_clicked)
        grid.addWidget(self.buttonForward, 5, 2)
        self.buttonStop.setText("Stop")
        self.buttonStop.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.buttonStop.clicked.connect(self.stop_was_clicked)
        grid.addWidget(self.buttonStop, 6, 2)
        self.buttonTurnLeft.setText("Turn Left")
        self.buttonTurnLeft.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.buttonTurnLeft.clicked.connect(self.left_was_clicked)
        grid.addWidget(self.buttonTurnLeft, 5, 1, 2, 1)
        self.buttonTurnRight.setText("Turn Right")
        self.buttonTurnRight.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.buttonTurnRight.clicked.connect(self.right_was_clicked)
        grid.addWidget(self.buttonTurnRight, 5, 3, 2, 1)

        grid.addWidget(QLabel(), 4, 5, 1, 2)
        grid.addWidget(QLabel(), 5, 4, 2, 1)

        self.buttonModeManual = QPushButton()
        self.buttonModeTracking = QPushButton()
        self.buttonModeHand = QPushButton()

        self.buttonModeManual.setText("Manual Control")
        self.buttonModeManual.setEnabled(False)
        self.buttonModeManual.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        grid.addWidget(self.buttonModeManual, 1, 5, 1, 2)
        self.buttonModeManual.clicked.connect(self.switch_to_manual)
        self.buttonModeTracking.setText("Automatic Tracking ")
        self.buttonModeTracking.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        grid.addWidget(self.buttonModeTracking, 2, 5, 1, 2)
        self.buttonModeTracking.clicked.connect(self.switch_to_object)
        self.buttonModeHand.setText("Gesture Control")
        self.buttonModeHand.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        grid.addWidget(self.buttonModeHand, 3, 5, 1, 2)
        self.buttonModeHand.clicked.connect(self.switch_to_hand)

        self.thread = VideoThread()
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.start()

        self.setLayout(grid)

        self.image_label = QLabel(self)
        self.image_label.resize(self.display_width, self.display_height)

        grid.addWidget(self.image_label, 1, 1, 3, 3)
        self.setWindowTitle("Robot Remote Control")
        self.show()

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img):
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        frame = convert_to_Qt_format.scaled(self.display_width, self.display_height, Qt.AspectRatioMode.KeepAspectRatio)
        return QPixmap.fromImage(frame)


    def alert(self, msg):

        error = QErrorMessage(self)
        error.showMessage(msg)

    def forward_was_clicked(self):
        if Window.states == 0:
            keyboard = pynput.keyboard.Controller()
            keyboard.press('w')
            print('Forward ')
        elif Window.states == 3:
            print('On timeout')
        else:
            print('not in manual mode')

    def right_was_clicked(self):
        if Window.states == 0:
            keyboard = pynput.keyboard.Controller()
            keyboard.press('D')
            print('Right ')
        elif Window.states == 3:
            print('On timeout')
        else:
            print('not in manual mode')

    def left_was_clicked(self):
        if Window.states == 0:
            keyboard = pynput.keyboard.Controller()
            keyboard.press('A')
            print('Left ')
        elif Window.states == 3:
            print('On timeout')
        else:
            print('not in manual mode')

    def stop_was_clicked(self):
        if Window.states == 0:
            keyboard = pynput.keyboard.Controller()
            keyboard.press('X')
            print('Stop ')
        elif Window.states == 3:
            print('On timeout')
        else:
            print('not in manual mode')

    def emerg_stop(self):
        self.button_emerg_stop.setEnabled(False)
        keyboard = pynput.keyboard.Controller()
        keyboard.press('X')
        Window.states = 3
        loop = QEventLoop()
        QTimer.singleShot(5000, loop.quit)
        loop.exec_()
        Window.states = 0
        self.button_emerg_stop.setEnabled(True)
        print('EMERGENCY STOP')

    def switch_to_manual(self):
        if Window.states != 3:
            keyboard = pynput.keyboard.Controller()
            if Window.states == 1:
                print('hand to manual')
                self.buttonModeHand.setEnabled(True)
            elif Window.states == 2:
                print('object to manual')
                keyboard.press('p')
                self.buttonModeTracking.setEnabled(True)
            Window.states = 0
            keyboard.press('X')
            self.buttonModeManual.setEnabled(False)
        else:
            print('On timeout')

        print('manual')

    def switch_to_hand(self):
        if Window.states != 3:
            keyboard = pynput.keyboard.Controller()
            if Window.states == 0:
                print('manual to hand')
                self.buttonModeManual.setEnabled(True)
            elif Window.states == 2:
                print('object to hand')
                keyboard.press('p')
                self.buttonModeTracking.setEnabled(True)
            Window.states = 1
            keyboard.press('X')
            print('hand')
            self.buttonModeHand.setEnabled(False)
        else:
            print('On timeout')

    def switch_to_object(self):
        if Window.states != 3:
            keyboard = pynput.keyboard.Controller()
            if Window.states == 0:
                print('manual to object')
                self.buttonModeManual.setEnabled(True)
            elif Window.states == 1:
                print('hand to object')
                keyboard.press('p')
                self.buttonModeHand.setEnabled(True)
            Window.states = 2
            keyboard.press('X')
            print('object')
            self.buttonModeTracking.setEnabled(False)
        else:
            print('On timeout')




if __name__ == '__main__':
    App = QApplication(sys.argv)
    window = Window()

    sys.exit(App.exec())
