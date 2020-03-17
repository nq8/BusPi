import sys
from PyQt5.QtWidgets import QApplication, QWidget, QAction, QTableWidget, QTableWidgetItem, QVBoxLayout, \
    QLabel, QHBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import *
from getData2 import *
import time

class Visualizer:
    def __init__(self):
        app = QApplication(sys.argv)

        self.mainWidget = QWidget()
        self.mainWidget.setWindowTitle('BusPi v0.1')
        self.mainWidget.setFixedHeight(300)
        self.mainWidget.setFixedWidth(500)

        #buslayout = QVBoxLayout()
        #bus_label = QLabel('Bus Schedule')
        #buslayout.addWidget(bus_label)
        #self.bus_table_widget = self.createTable()
        #buslayout.addWidget(self.bus_table_widget)

        #sbahnlayout = QVBoxLayout()
        #sbahn_label = QLabel('S-Bahn Schedule')
        #sbahnlayout.addWidget(sbahn_label)
        #self.sbahn_table_widget = self.createTable()
        #sbahnlayout.addWidget(self.sbahn_table_widget)

        bothlayout = QVBoxLayout()
        bothlabel = QLabel('Bus and S-Bahn Schedule')
        bothlayout.addWidget(bothlabel)
        self.table_widget = self.createTable()
        bothlayout.addWidget(self.table_widget)

        self.updateData()

        layout = QHBoxLayout()
        layout.addLayout(bothlayout)
        #layout.addLayout(buslayout)
        #layout.addLayout(sbahnlayout)
        self.mainWidget.setLayout(layout)
        self.mainWidget.show()

        app.exec_()

    def createTable(self):
        table_widget = QTableWidget()
        table_widget.setRowCount(6)
        table_widget.setColumnCount(3)
        table_widget.setHorizontalHeaderLabels(('Line', 'Dest.', 'Departure in'))
        table_widget.verticalHeader().setVisible(False)
        table_widget.setFixedHeight(225)
        table_widget.setFixedWidth(240)
        return table_widget


    def fillTableWithData(self, data, table_widget):
        if (len(data)>0):
            for i in range(table_widget.rowCount()):
                for j in range(table_widget.columnCount()):
                        table_widget.setItem(i, j, QTableWidgetItem(data[i][j]))
            table_widget.resizeColumnsToContents()
            table_widget.setAutoFillBackground(True)
            table_widget.setAlternatingRowColors(True)
            table_widget.setFixedHeight(225)
            table_widget.setFixedWidth(270)
            table_widget.horizontalHeader().setStretchLastSection(True)

    def retrieveBusData(self):
        busdata = getBusData()
        busdata = busdata[1:4]
        return busdata

    def retrieveSbahnData(self):
        sbahndata = getSbahnData()
        sbahndata = sbahndata[0:3]
        return sbahndata

    def updateData(self):
        busdata = self.retrieveBusData()
        #self.fillTableWithData(busdata, self.bus_table_widget)
        sbahndata = self.retrieveSbahnData()
        alldata = busdata+sbahndata
        self.fillTableWithData(alldata, self.table_widget)
        self.table_widget.horizontalHeader().setStretchLastSection(True)
        #self.fillTableWithData(sbahndata, self.sbahn_table_widget)
        QTimer.singleShot(10000, self.updateData)

if __name__ == '__main__':
    vis = Visualizer()

