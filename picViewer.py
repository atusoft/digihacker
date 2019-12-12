import sys
import os

from pathlib import Path

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QImage, QIcon
from PyQt5.QtCore import Qt, QSize, QRect


def parentDir(folder):
    return str(Path(folder).parent)


def isdir(path):
    return os.path.isdir(path)


def list_files(folder):
    files = []
    filenames = []
    for f in os.listdir(folder):
        files.append(os.path.join(folder, f))
        filenames.append(f)
    return files, filenames


def is_image(file):
    name, extension = os.path.splitext(file)
    return extension.lower() in ['.jpg', '.bmp', '.png','.ico','.tiff']


class MyApp(QMainWindow):
    folder = ''

    def __init__(self, folder, parent=None):
        super(MyApp, self).__init__(parent)
        self.folder = folder
        self.sp = None

        exitAct = QAction(QIcon(self.getStandIcon('SP_ArrowBack')), 'Back', self)
        exitAct.triggered.connect(self.backParentFolder)
        self.toolbar = self.addToolBar('Back')
        self.toolbar.addAction(exitAct)

        self.listView = QTableWidget()
        self.initPicList()

        self.setCentralWidget(self.listView)
        self.resize(1500, 800)
        self.setWindowTitle(folder)

    def initPicList(self):
        self.listView.setIconSize(QSize(300, 300))
        self.listView.horizontalHeader().setVisible(False)
        self.listView.verticalHeader().setVisible(False)
        self.listView.setShowGrid(False)
        self.listView.setColumnCount(5)
        self.listView.itemDoubleClicked.connect(self.show_pic)
        self.add_picture(self.listView)

    def backParentFolder(self):
        self.folder = parentDir(self.folder)
        self.add_picture(self.listView)

    def add_picture(self, listView):
        files, names = list_files(self.folder)
        listView.setRowCount(len(files) / 5)
        for i, file in enumerate(files):
            item = QTableWidgetItem()
            item.setFlags(Qt.ItemIsEnabled)
            icon = QIcon()
            QApplication.processEvents()
            qimg = QImage(file)
            icon.addPixmap(QPixmap.fromImage(qimg), QIcon.Normal, QIcon.Off)
            if isdir(file):
                dir_icon = 'SP_DirIcon'
                item.setIcon(self.getStandIcon(dir_icon))
            else:
                if is_image(names[i]):
                    item.setIcon(icon)
                else:
                    item.setIcon(self.getStandIcon('SP_FileIcon'))
            item.setToolTip(names[i])
            item.setText(names[i])
            listView.setRowHeight(i / 5, 300)
            listView.setColumnWidth(i % 5, 300)
            listView.setItem(i / 5, i % 5, item)
        self.setWindowTitle(self.folder)

    def getStandIcon(self, dir_icon):
        """icon names: https://joekuan.wordpress.com/2015/09/23/list-of-qt-icons/"""
        return self.style().standardIcon(getattr(QStyle, dir_icon))

    def show_pic(self, item):
        path = item.text()
        rpath = os.path.join(self.folder, path)
        if os.path.isdir(rpath):
            self.folder = rpath
            self.add_picture(self.listView)
        else:
            self.sp = Single_Pic(os.path.join(self.folder, path))
            self.sp.setGeometry(QRect(self.x(), self.y(), self.sp.width(), self.sp.height()))
            self.sp.show()


class Single_Pic(QWidget):
    def __init__(self, path):
        super().__init__()
        self.path = path
        self.initUI()

    def initUI(self):
        label = QLabel(self)
        qimg = QImage(self.path)
        label.resize(qimg.width() / qimg.height() * 800, 800)
        self.resize(label.width(), label.height())
        label.setPixmap(QPixmap.fromImage(qimg).scaled(label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    t = MyApp(sys.argv[1])
    t.show()
    sys.exit(app.exec_())
