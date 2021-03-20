"""
Основная форма которая подтягивает и передает
все в остальные формы
В перспективе надо будет разбить все на модули
"""

import sys, os, time
import pandas as pd
from PyQt5 import QtWidgets, QtCore

#Подключаемые модули
import Dialog
from Qthread_test import TryThresd as TryThresd



class MyWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.test = {}
        self.CurStatus =QtWidgets.QListWidget()
        self.t=[]
        # self.co = 0
        # self.worker={}


        self.b1 = QtWidgets.QPushButton('Выберите папку')
        self.b1.clicked.connect(self.button_clicked)
        layout = QtWidgets.QHBoxLayout()
        self.label_main = QtWidgets.QLabel()
        layout.addWidget(self.label_main)
        layout.addWidget(self.b1)
        layout.addWidget(self.CurStatus )

        self.setLayout(layout)
        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('Main Form')

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Return:
            self.button_clicked()

    def button_clicked(self):
        self.wb_path = QtWidgets.QFileDialog.getExistingDirectory(self,
                                                             "Выберите папку")
        files = os.listdir(self.wb_path)
        self.d = [""]
        file_form=['xlsx','xlsb']

        for f in files:
            if f.split('.')[-1].lower() in file_form:
                self.d.append(f)
        self.CurStatus.addItem("Папка выбрана")
        self.dialog = Dialog(self)
        self.dialog.exec_()
        self.other_run()

    def other_run(self):
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

    def test_one(self, val):
        self.t = val
        print(self.t.head(5))

    def isFinished(self):
        self.coun += 1
        print("Thread finished " + str(self.coun))
        if self.coun == 2:
            print('krasava!')


# class TryThresd(QtCore.QThread):
#     any_signal=QtCore.pyqtSignal(int)
#
#     def __init__(self, root):
#         super().__init__(root)
#         self.main = root
#
#     def run(self):
#
#         way1 = self.main.wb_path + '/'+self.main.test['Zak']
#         print(way1)
#         self.df_zak = pd.read_excel(way1,
#                                sheet_name='декабрь',
#                                usecols="A:AR",
#                                skiprows=range(0, 4))
#         self.main.CurStatus.addItem("заказ приехал")
#         self.any_signal.emit(1)
#         # QtWidgets.QApplication.processEvents()
#         # self.main.co+=1
#         # self.main.CurStatus.addItem(self.main.co)
#
#
#
# class TryTh(QtCore.QThread):
#     def __init__(self, root):
#         super().__init__(root)
#         self.main = root
#
#     def run(self):
#         way2 = self.main.wb_path + '/' + self.main.test['Status']
#         self.df_ost = pd.read_excel(way2,
#                                sheet_name='Sheet1',
#                                usecols="A:DA")
#         self.main.CurStatus.addItem("остаток получен")



class Dialog(QtWidgets.QDialog, Dialog.Ui_Dialog_next):
    def __init__(self, root):
        super().__init__(root)
        self.setupUi(self)
        self.main = root
        self.Text_path.setText(self.main.wb_path)

        knopk=[self.sklad_mnlz,
               self.sklad_nerez,
               self.sklad_rez,
               self.zakaz,
               self.status]
        inclu=[['Мнлз', 'мнлз'],
               ['нерез', 'не рез'],
               ['реза', 'рез'],
               ['ост', 'заказ'],
               ['статус', 'стат']]
        exc=[[],[],
             ['нерез', 'не рез'],
             [], []]
        for x,y,z in zip(knopk,inclu,exc):
            self.__init_cb_test__(x,y,z)

        self.pB_main_run.clicked.connect(self.button_clicked)


    def __init_cb_test__(self,cm_name,item_name,iskl=[]):
        cm_name.addItems(self.main.d)
        for i in self.main.d:
            if not iskl:
              assert len(iskl)==0, "зашло то что не должно"
              if item_name[0] in i.lower() or item_name[1] in i.lower():
                 cm_name.setCurrentText(i)
                 break
            elif ((item_name[0] in i.lower()
                  or item_name[1] in i.lower())
                  and iskl[0] not in i.lower()
                  and iskl[1] not in i.lower()):
                # assert len(iskl) == 0, "зашло то что не должно"
                cm_name.setCurrentText(i)
                break

    def button_clicked(self):
        #проверка на корректно заполненное значение
        # tes_a=[]
        # for x in knopk:
        #     tes_a.append(x.currentText())
        tes_a=[self.sklad_mnlz.currentText(),
           self.sklad_nerez.currentText(),
           self.sklad_rez.currentText(),
           self.zakaz.currentText(),
           self.status.currentText()]
        tes_b=set(tes_a)
        if len(tes_a)>len(tes_b):
            msgBox = QtWidgets.QMessageBox()
            msgBox.setIcon(QtWidgets.QMessageBox.Information)
            msgBox.setText("задвоено значение")
            msgBox.setWindowTitle("Ошибка!")
            msgBox.exec_()
            return

        self.main.CurStatus.addItem("Файлы выбраны")
        self.main.test={"MNLZ":self.sklad_mnlz.currentText(),
           "Nerez":self.sklad_nerez.currentText(),
           "Rez":self.sklad_rez.currentText(),
           "Zak":self.zakaz.currentText(),
           "Status":self.status.currentText()}

        self.close()

def window():
    app = QtWidgets.QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())

window()