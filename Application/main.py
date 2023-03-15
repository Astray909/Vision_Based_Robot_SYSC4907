import sys
import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import*
from PyQt5.QtWidgets import *
import pynput
from time import sleep

class Window(QWidget):
      #states: 0=manual, 1=hand gesture, 2=object tracking, 3=temporary diasble
      states=0

      def __init__(self):
         super().__init__()




         self.setGeometry(100,100,800,600)

         grid = QGridLayout()


         buttonEmergStop = QPushButton()
         buttonEmergStop.setText("STOP")
         buttonEmergStop.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Expanding)
         buttonEmergStop.clicked.connect(self.emerg_stop)
         grid.addWidget(buttonEmergStop,5,5,2,2)




         buttonForward = QPushButton()
         buttonStop = QPushButton()
         buttonTurnLeft = QPushButton()
         buttonTurnRight = QPushButton()

         buttonForward.setText("Forward")
         buttonForward.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
         buttonForward.clicked.connect(self.forward_was_clicked)
         grid.addWidget(buttonForward,5,2)
         buttonStop.setText("Stop")
         buttonStop.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
         buttonStop.clicked.connect(self.stop_was_clicked)
         grid.addWidget(buttonStop,6,2)
         buttonTurnLeft.setText("Turn Left")
         buttonTurnLeft.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
         buttonTurnLeft.clicked.connect(self.left_was_clicked)
         grid.addWidget(buttonTurnLeft, 5,1,2,1)
         buttonTurnRight.setText("Turn Right")
         buttonTurnRight.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
         buttonTurnRight.clicked.connect(self.right_was_clicked)
         grid.addWidget(buttonTurnRight, 5,3,2,1)


         grid.addWidget(QLabel(),4,5,1,2)
         grid.addWidget(QLabel(),5,4,2,1)


         buttonModeManual = QPushButton()
         buttonModeTracking = QPushButton()
         buttonModeHand = QPushButton()

         buttonModeManual.setText("Manual Control")
         buttonModeManual.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
         grid.addWidget(buttonModeManual, 1, 5, 1, 2)
         buttonModeManual.clicked.connect(self.switch_to_manual)
         buttonModeTracking.setText("Automatic Tracking ")
         buttonModeTracking.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
         grid.addWidget(buttonModeTracking, 2, 5, 1, 2)
         buttonModeTracking.clicked.connect(self.switch_to_object)
         buttonModeHand.setText("Gesture Control")
         buttonModeHand.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
         grid.addWidget(buttonModeHand, 3, 5, 1, 2)
         buttonModeHand.clicked.connect(self.switch_to_hand)


         self.available_cameras =QCameraInfo.availableCameras()

         self.viewfinder = QCameraViewfinder()

         self.viewfinder.show()

         self.select_camera(1)

         self.setLayout(grid)

         grid.addWidget(self.viewfinder,1,1,3,3)
         self.setWindowTitle("Controller")
         self.show()


      def select_camera(self, i):
         self.camera = QCamera(self.available_cameras[i])
         self.camera.setViewfinder(self.viewfinder)
         self.camera.setCaptureMode(QCamera.CaptureVideo)
         self.camera.error.connect(lambda: self.alert(self.camera.errorString()))
         self.camera.start()
         self.capture = QCameraImageCapture(self.camera)
         self.current_camera_name = self.available_cameras[i].description()
         self.save_seq = 0


      def alert(self, msg):

         error= QErrorMessage(self)
         error.showMessage(msg)


      def forward_was_clicked(self):
         if Window.states==0:
            keyboard = pynput.keyboard.Controller()
            keyboard.press('w')
            print('Forward ')
         elif Window.states==3:
            print('On timeout')
         else:
            print('not in manual mode')
      def right_was_clicked(self):
         if Window.states == 0:
             keyboard = pynput.keyboard.Controller()
             keyboard.press('D')
             print('Right ')
         elif Window.states==3:
            print('On timeout')
         else:
            print('not in manual mode')

      def left_was_clicked(self):
         if Window.states == 0:
            keyboard = pynput.keyboard.Controller()
            keyboard.press('A')
            print('Left ')
         elif Window.states==3:
            print('On timeout')
         else:
            print('not in manual mode')

      def stop_was_clicked(self):
         if Window.states == 0:
            keyboard = pynput.keyboard.Controller()
            keyboard.press('X')
            print('Stop ')
         elif Window.states==3:
            print('On timeout')
         else:
            print('not in manual mode')


      def emerg_stop(self):
         self.isEnabled(False)
         keyboard = pynput.keyboard.Controller()
         keyboard.press('X')
         Window.states=3
         sleep(5)
         Window.states=0
         self.isEnabled(True)
         print('EMERGENCY STOP')


      def switch_to_manual(self):
         if Window.states!=3:
            keyboard = pynput.keyboard.Controller()
            if Window.states == 1:
               print('hand to manual')
            elif Window.states == 2:
               print('object to manual')
               keyboard.press('p')
            Window.states = 0
            keyboard.press('X')
         else:
            print('On timeout')


         print('manual')
      def switch_to_hand(self):
         if Window.states!=3:
            keyboard = pynput.keyboard.Controller()
            if Window.states == 0:
               print('manual to hand')
            elif Window.states == 2:
               print('object to manual')
               keyboard.press('p')
            Window.states = 1
            keyboard.press('X')
            print('hand')
         else:
            print('On timeout')

      def switch_to_object(self):
         if Window.states!=3:
            keyboard = pynput.keyboard.Controller()
            if Window.states == 0:
             print('manual to object')
            elif Window.states == 1:
               print('hand to object')
               keyboard.press('p')
            Window.states = 2
            keyboard.press('X')
            print('object')
         else:
            print('On timeout')


if __name__ == '__main__':
   App = QApplication(sys.argv)
   window = Window()

   sys.exit(App.exec())