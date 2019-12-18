import sys

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import easyquotation
import pandas as pd
from PyQt5.QtCore import QTimer, pyqtSignal, QThread, Qt
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtWidgets import *
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
from stock.data.models import *

stocks = Stock.objects.all()


class WorkThread(QThread):
    trigger = pyqtSignal(str)

    def __int__(self):
        super(WorkThread, self).__init__()

    def run(self):
        global stocks
        try:
            quotation = easyquotation.use('qq')
            price = quotation.stocks(list(map(lambda s: s.stockid, stocks)), prefix=True)
            with pd.option_context('display.max_rows', None, 'display.max_columns', None):
                hk = pd.DataFrame(price)
                hk = hk.T.ix[:, ['name', 'now', 'open', 'close']]
                price = hk.iterrows()

            row = 0
            for index, stock in price:
                self.trigger.emit(f"{row}:{stock['name']}:{stock['now']}:{stock['open']}")

                row += 1
        except Exception as e:
            print(e)


class MyApp(QMainWindow):
    def __init__(self, stockIds, parent=None):
        super(MyApp, self).__init__(parent)
        self.stocks = stockIds
        self.m = PlotCanvas(self, width=5, height=4)

        self.createTable()

        self.timer = QTimer()
        self.timer.setInterval(5000)
        self.timer.timeout.connect(self.start)
        self.timer.start()

        self.work = WorkThread()
        self.work.trigger.connect(self.showPrice)

        layout = QHBoxLayout(self)
        layout.addWidget(self.listView)
        self.work.trigger.connect(self.m.plot)
        layout.addWidget(self.m)
        window = QWidget()
        window.setLayout(layout)
        self.setCentralWidget(window)

    def start(self):
        self.work.start()

    def createTable(self):
        self.listView = QTableWidget()
        self.listView.setRowCount(10)
        self.listView.setColumnCount(3)
        self.listView.itemSelectionChanged.connect(self.choose)
        for row, s in enumerate(self.stocks):
            item = QTableWidgetItem()
            item.setText(s.stockid)
            self.listView.setItem(row, 0, item)

            item = QTableWidgetItem()
            item.setText("")
            self.listView.setItem(row, 1, item)

            item = QTableWidgetItem()
            item.setText("")
            self.listView.setItem(row, 2, item)

    def showPrice(self, str):
        row = int(str.split(':')[0])
        name = str.split(':')[1]
        price = str.split(':')[2]
        open = str.split(':')[3]

        self.listView.item(row, 1).setText(name)
        price_cell = self.listView.item(row, 2)
        if float(open) > float(price):
            price_cell.setForeground(QBrush(QColor(0, 255, 0)))
        else:
            price_cell.setForeground(QBrush(QColor(255, 0, 0)))
        price_cell.setTextAlignment(Qt.AlignCenter)

        price_cell.setText(price)

    def choose(self):
        self.m.choosed = self.listView.selectedIndexes()[0].row()
        self.m.clear()


class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.data = []
        self.choosed = 0

    def clear(self):
        self.data = []
        self.ax.clear()

    def plot(self, msg):
        if int(msg.split(":")[0]) == self.choosed:
            print(msg)
            self.data.append(float(msg.split(":")[2]))
            self.ax = self.figure.add_subplot(111)
            self.ax.plot(self.data, 'r-')
            self.ax.set_title(msg.split(':')[1])
            self.draw()


def main():
    app = QApplication(sys.argv)
    t = MyApp(stocks)
    t.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
