import pandas as pd
import numpy as np
import sys, time
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox, QComboBox,QAction
import sys
import os

# import Qthread_test
from Qthread_test import TryThresd as TryThresd


class MyWindow(QDialog):
    def __init__(self, root):
        super().__init__(root)
        self.main=root
        #self.test = {}

        self.b1 = QtWidgets.QPushButton('Выберите папку')
        self.b1.clicked.connect(self.button_clicked)
        layout = QtWidgets.QHBoxLayout()
        self.label_main = QtWidgets.QLabel()
        layout.addWidget(self.label_main)
        layout.addWidget(self.b1)
        self.setLayout(layout)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Return:
            self.button_clicked()

    def button_clicked(self):
        self.wb_path = QtWidgets.QFileDialog.getExistingDirectory(self,
                                                             "Выберите папку")

        files = os.listdir(self.wb_path)
        self.d = [""]
        self.close()
        for f in files:
            if (f.endswith('.xlsx')
                    or f.endswith('.xlsb')
                    or f.endswith('.XLSX')):
                self.d.append(f)
        self.main.test=self.d





"""
Попытка ловли через виджет
"""
class Main_Window(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        print(2)
        """
        далее идет фишка с самоспрятом
        """
        hide_action = QAction("Hide", self)
        hide_action.triggered.connect(self.hide)

        self.test = {}
        self.win = MyWindow(self)
        self.win.exec_()
        self.hide()
        print(self.test)


def Window():
    app = QApplication(sys.argv)
    win2 = Main_Window()
    win2.show()
    sys.exit(app.exec_())
Window()

