from PyQt5.QtCore import QTimer, pyqtSignal, QThread, Qt
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtWidgets import *
import sys


class EmailClient(QMainWindow):

    def __init__(self, parent=None):
        super(EmailClient, self).__init__(parent)


def main():
    app = QApplication(sys.argv)
    t = EmailClient()
    t.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
