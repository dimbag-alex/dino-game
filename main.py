from UI import Ui_MainWindow
import sys
import random
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt5.QtCore import Qt

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.rad = random.randint(30, 70)
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 300, 300)
        self.btn = QPushButton("Draw", self)
        self.btn.resize(self.btn.sizeHint())
        self.btn.move(20, 20)
        self.drow=False
        self.btn.clicked.connect(self.cicle)
        self.coor_x=10
        self.coor_y = 10


    def cicle(self):
        self.coor_x = random.randint(20, 250)
        self.coor_y = random.randint(20, 250)
        self.rad = random.randint(30, 70)


    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.update()
        self.Circle(qp)
        qp.end()

    def Circle(self, qp):
        pen = QPen(Qt.yellow, 2)
        qp.setPen(pen)
        qp.drawEllipse(self.coor_x, self.coor_y, self.rad, self.rad)



    def drawFlag(self, qp):
        qp.setBrush(QColor(255, 0, 0))
        qp.drawRect(30, 30, 120, 30)
        qp.setBrush(QColor(0, 255, 0))
        qp.drawRect(30, 60, 120, 30)
        qp.setBrush(QColor(0, 0, 255))
        qp.drawRect(30, 90, 120, 30)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
