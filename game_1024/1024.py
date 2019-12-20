import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QImage, QImageReader, QPainter, QColor, QFont
import random
import numpy as np

padding = 20
blankColor = QColor(204, 192, 178)


class Square:
    def __init__(self, x, y, num=0):
        self.num = num
        self.x = x
        self.y = y
        self.width = 200

    def moveLeft(self):
        if self.x > 1:
            self.x -= 1

    def moveRight(self):
        if self.x < 4:
            self.x += 1

    def moveUp(self):
        if self.y > 1:
            self.y -= 1

    def moveDown(self):
        if self.y < 4:
            self.y += 1

    @property
    def xpos(self):
        return self.x * self.width

    @property
    def ypos(self):
        return self.y * self.width

    def draw(self, p):
        p.fillRect(self.xpos + padding, self.ypos + padding, self.width - padding, self.width - padding,
                   blankColor)
        if self.num > 0:
            print(f"print {self.num}")
            font = p.font()
            font.setPointSize(32)
            p.setFont(font)
            p.setPen(Qt.red)
            p.drawText(self.xpos + int(self.width / 2) - 10, self.ypos + int(self.width / 2) + 30, f"{self.num}")

    def __str__(self):
        return f"{self.num} at {self.xpos},{self.ypos}"


class MyApp(QWidget):
    def __init__(self, parent=None):
        super(MyApp, self).__init__(parent)
        self.label = QLabel()
        self.qimg = QImage()
        self.canvas = QPixmap()
        self.tempCanvas = QPixmap()
        self.isDrawing = False
        self.val = ''
        self.square = list()
        self.allSquares = np.zeros((4, 4), dtype=int)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.setWindowTitle("1024")
        self.setMinimumWidth(800 + padding)
        self.setMinimumHeight(800 + padding)
        self.initUi()
        self.currentX = 0
        self.currentY = 0

    def initUi(self):
        self.canvas = QPixmap(self.width(), self.height())
        self.canvas.fill(Qt.white)
        p = QPainter(self.canvas)
        for y in range(0, 4):
            for x in range(0, 4):
                s = Square(x=x, y=y)
                s.draw(p)

    def keyPressEvent(self, QKeyEvent):
        # self.isDrawing = True
        painter = QPainter(self.canvas)
        if QKeyEvent.key() == Qt.Key_Space:
            self.generate_square(painter)
        if QKeyEvent.key() == Qt.Key_Left:
            print(self.allSquares)
            self.move_left(painter)
        if QKeyEvent.key() == Qt.Key_Right:
            self.allSquares = np.rot90(self.allSquares, k=2)
            print(self.allSquares)
            self.move_left(painter)
            self.allSquares = np.rot90(self.allSquares, k=2)
        if QKeyEvent.key() == Qt.Key_Up:
            self.allSquares = np.rot90(self.allSquares)
            self.move_left(painter)
            self.allSquares = np.rot90(self.allSquares, k=3)
        if QKeyEvent.key() == Qt.Key_Down:
            self.allSquares = np.rot90(self.allSquares, k=3)
            self.move_left(painter)
            self.allSquares = np.rot90(self.allSquares)

        for x in range(0, 4):
            for y in range(0, 4):
                s = Square(x, y, num=self.allSquares[y][x])
                s.draw(painter)

        self.update()

    def move_left(self, painter):
        for row in range(0, 4):

            queue = self.allSquares[row]
            # move zero to right side
            queue = np.concatenate((queue[queue != 0], queue[queue == 0]))
            for i, n in enumerate(queue):
                if i < len(queue) - 1 and queue[i] == queue[i + 1]:
                    queue[i] = queue[i] * 2
                    queue[i + 1] = 0
            queue = np.concatenate((queue[queue != 0], queue[queue == 0]))
            print(f"pad: {queue}")
            for i, n in enumerate(queue):
                self.allSquares[row][i] = n
                print(self.allSquares[row][i])

    def generate_square(self, painter):
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        if self.allSquares[row][col] == 0:
            print(f"generate {row},{col}")
            s = Square(col, row, num=2)
            s.draw(painter)
            self.allSquares[row][col] = int(s.num)
        else:
            self.generate_square(painter)

    def paintEvent(self, QPaintEvent):
        painter = QPainter(self)

        painter.drawPixmap(0, 0, self.canvas)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    t = MyApp()
    t.show()
    sys.exit(app.exec_())
