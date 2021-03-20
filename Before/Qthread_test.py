"""
Эта штукак просто для проверки работы с калссом QThread
и начало пути в многопоточности!
"""
import pandas as pd
import numpy as np
import sys, time
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox, QComboBox



class MyWindow(QtWidgets.QWidget):
    change_value = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.d = {'Остаток': 'ММКИ ЛПЦ 3000 Статус производства и отгрузки на 13.01.2021.XLSX',
                  'Заказ': "Остаток производства 13.01.2021.xlsx"}
        self.test = r'F:\3000' + '\\'
        self.coun=0
        self.t=[]


        self.b1 = QtWidgets.QPushButton('Нажми')
        self.b1.clicked.connect(self.button_clicked)
        layout = QtWidgets.QHBoxLayout()
        self.label_main = QtWidgets.QLabel()

        layout.addWidget(self.label_main)
        layout.addWidget(self.b1)
        self.setLayout(layout)

    def button_clicked(self):

        # self.worker = TryThresd(self)
        self.worker = TryThresd(self,
                                'Заказ',
                                'декабрь',
                                "A:AR",
                                range(0, 4))
        self.worker.start()
        self.worker.change_value.connect(self.test_one)
        self.worker2 = TryThresd(self,
                                 'Остаток',
                                 'Sheet1',
                                 "A:DA")
        self.worker2.start()


        self.worker.finished.connect(self.isFinished)
        self.worker2.finished.connect(self.isFinished)


    def test_one(self,val):
        self.t=val
        print(self.t.head(5))

    def isFinished(self):
        self.coun+=1
        print("Thread finished " + str(self.coun))
        if self.coun==2:
          print('krasava!')



class TryThresd(QThread):
     change_value = QtCore.pyqtSignal(object)

     def __init__(self,root,sp_name,nam,col,skipr=None):
     # def __init__(self, root): #skiprows=None
        super().__init__(root)
        self.main = root
        self._sp_name=sp_name
        self._nam=nam
        self._col=col
        self._skipr=skipr

     def run(self):
        way1 = self.main.test + self.main.d[self._sp_name]
        df_zak = pd.read_excel(way1,
                               sheet_name=self._nam,
                               usecols=self._col,
                               skiprows=self._skipr)
        print("заказ приехал")
        self.change_value.emit(df_zak)




# def window():
#     app = QApplication(sys.argv)
#     win = MyWindow()
#     win.show()
#     # test=TwoWindow.button_clicked()
#     sys.exit(app.exec_())

if __name__=='__main__':
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())


