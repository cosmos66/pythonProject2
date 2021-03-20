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




class TryThresd(QThread):
     change_value = QtCore.pyqtSignal(object)

     def __init__(self,root,sp_name,nam,col,skipr=None):
     # def __init__(self, root): #skiprows=None
        super().__init__(root)
        # print('test ' + sp_name)
        self.main = root
        self._sp_name=sp_name
        self._nam=nam
        self._col=col
        self._skipr=skipr

     def run(self):
         if self.main.file_dict[self._sp_name]=="":
             self.change_value.emit('')
             self.close()
         way1 = self.main.wb_path+ '/'+ self.main.file_dict[self._sp_name]
         try:
           df_zak = pd.read_excel(way1,
                               sheet_name=self._nam,
                               usecols=self._col,
                               skiprows=self._skipr)
         except Exception:
           e = sys.exc_info()[1]
           print(e.args[0])

         self.main.CurStatus.addItem(self._sp_name +" приехал")
         self.change_value.emit([self._sp_name,df_zak])



# if __name__=='__main__':
#     app = QApplication(sys.argv)
#     win = TryThresd()
#     win.show()
#     sys.exit(app.exec_())
