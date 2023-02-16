import sys
import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import*
from PyQt5.QtWidgets import *
from Communication_testing import client_manual

class Window(QWidget):
      def __init__(self):
         super().__init__()


         self.setGeometry(100,100,800,600)

         grid = QGridLayout()


         buttonEmergStop = QPushButton()
         buttonEmergStop.setText("STOP")
         buttonEmergStop.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Expanding)
         grid.addWidget(buttonEmergStop,5,5,2,2)




         buttonForward = QPushButton()
         buttonReverse = QPushButton()
         buttonTurnLeft = QPushButton()
         buttonTurnRight = QPushButton()

         buttonForward.setText("Forward")
         buttonForward.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
         buttonForward.clicked.connect(client_manual.check_key('w'))
         grid.addWidget(buttonForward,5,2)
         buttonReverse.setText("Reverse")
         buttonReverse.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
         grid.addWidget(buttonReverse,6,2)
         buttonTurnLeft.setText("Turn Left")
         buttonTurnLeft.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
         grid.addWidget(buttonTurnLeft, 5,1,2,1)
         buttonTurnRight.setText("Turn Right")
         buttonTurnRight.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
         grid.addWidget(buttonTurnRight, 5,3,2,1)


         grid.addWidget(QLabel(),4,5,1,2)
         grid.addWidget(QLabel(),5,4,2,1)


         buttonModeManual = QPushButton()
         buttonModeTracking = QPushButton()
         buttonModeHand = QPushButton()

         buttonModeManual.setText("Manual Control")
         buttonModeManual.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
         grid.addWidget(buttonModeManual, 1, 5, 1, 2)
         buttonModeTracking.setText("Automatic Tracking ")
         buttonModeTracking.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
         grid.addWidget(buttonModeTracking, 2, 5, 1, 2)
         buttonModeHand.setText("Gesture Control")
         buttonModeHand.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
         grid.addWidget(buttonModeHand, 3, 5, 1, 2)


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


if __name__ == '__main__':
   App = QApplication(sys.argv)
   window = Window()

   sys.exit(App.exec())