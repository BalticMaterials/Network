import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel,QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

def window():
   app = QApplication(sys.argv)
   widget = QWidget()

   textLabel = QLabel(widget)
   textLabel.setText("Network-State Overview")
   textLabel.move(10,10)
   
   button1 = QPushButton(widget)
   button1.setText("Button1")
   button1.move(128 ,64)
   
   def button1_clicked():
    print("Button 1 clicked")
   
   button1.clicked.connect(button1_clicked)
   

   widget.setGeometry(100,100,1920,1080)
   widget.setWindowTitle("BalticMaterials GmbH - Robotic Network")
   widget.show()
   sys.exit(app.exec_())

if __name__ == '__main__':
   window()