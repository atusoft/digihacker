from ffpyplayer.player import MediaPlayer
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QImage, QImageReader
from PyQt5.QtCore import QTimer


class MyApp(QWidget):
    def __init__(self, name, parent=None):
        super(MyApp, self).__init__(parent)
        self.label = QLabel()
        self.qimg = QImage()
        self.val = ''

        self.player = MediaPlayer(name)
        self.timer = QTimer()
        self.timer.setInterval(50)
        self.timer.start()
        self.timer.timeout.connect(self.showFrame)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.setWindowTitle(name)

        # self.showFullScreen()

    def showFrame(self):
        frame, self.val = self.player.get_frame()
        if frame is not None:
            img, t = frame
            self.qimg = QImage(bytes(img.to_bytearray()[0]), img.get_size()[0], img.get_size()[1],
                               QImage.Format_RGB888)
            self.label.setPixmap(QPixmap.fromImage(self.qimg))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    t = MyApp(sys.argv[1])
    t.show()
    sys.exit(app.exec_())
