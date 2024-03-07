from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication,QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QHBoxLayout
from PyQt5.QtGui import QPixmap
import sys

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(0,0,640,480)


def main():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())

main()