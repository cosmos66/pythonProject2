"""
Основная форма которая подтягивает и передает
все в остальные формы
В перспективе надо будет разбить все на модули
"""

import sys, os, time
import traceback
import pandas as pd
from PyQt5 import QtWidgets, QtCore, QtGui

# Подключаемые модули
import Dialog
from qt_calss import TryThresd as TryThresd


class MyWindow(QtWidgets.QWidget):
    """ Использую этот модуль как основной
        на первом этапе он будет служить
        как точка обмена информацие между окнами"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.file_dict = {}
        l4= ["Получатель",
                    "Заказ УИТ",
                    "Сбыт.зак. SAP",
                    "Толщина, мм",
                    "Ширина, мм",
                    "Длина, мм",
                    "Марка стали",
                    "Класс точности",
                    "Остаток в прокат, т",
                    "Шифр МВКС",
                    "Толщина",
                    "Ширина",
                    "Длина"]
        l5=['Номер контракта',
                   "SMI",
                   "Обозначение района",
                   "Внешний номер заказа",
                   "№ заказа",
                   "LSD комбината",
                   "Дата окончания заказа",
                   "Марка стали",
                   "НД на марку",
                   "НД на техтребования",
                   "Дата поставки по контракту",
                   "Состояние поставки",
                   "Si мин",
                   "Si макс"]
        self.MV={"MNLZ":"",  # основнй словарь в котором будет храниться инфо всгео массива
               "Nerez":"",
               "Rez":"",
               "Zak":l4,
               "Status":l5}
        self.df_z=[]  # основной массив с заказами
        self.coun = 0
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Main Form')
        # self.setGeometry(200, 200, 450, 450)

        self.b1 = QtWidgets.QPushButton('Выберите папку')
        self.b1.setToolTip('Нажми чтобы выбрать путь к папке с файлами')
        # self.b1.setGeometry(QtCore.QRect(150, 370, 150, 50))

        self.sav_bu = QtWidgets.QPushButton('Сохранить')
        # self.sav_bu.setGeometry(QtCore.QRect(150, 370, 150, 50))

        self.CurStatus = QtWidgets.QListWidget()
        # self.CurStatus.setGeometry(QtCore.QRect(50, 50, 350, 300))

        self.b1.clicked.connect(self.button_clicked)
        self.sav_bu.clicked.connect(self.soxr_clicked)
        layout = QtWidgets.QVBoxLayout()


        self.label_main = QtWidgets.QLabel()

        layout.addWidget(self.label_main)

        layout.addWidget(self.b1)
        layout.addWidget(self.CurStatus )
        layout.addWidget(self.sav_bu)
        self.sav_bu.hide()

        self.setLayout(layout)


    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Return:
            self.button_clicked()
        elif event.key() == QtCore.Qt.Key_Esc:
            self.close()
        else:
            return

    def button_clicked(self):
        self.b1.hide()
        self.wb_path = QtWidgets.QFileDialog.getExistingDirectory(self,
                                                             "Выберите папку",
                                                             'F:\Mega\Python Scripts' )  # убрать от греха
        files = os.listdir(self.wb_path)
        self.d = [""]
        file_form=['xlsx','xlsb']

        for f in files:
            if f.split('.')[-1].lower() in file_form:
                self.d.append(f)
        self.CurStatus.addItem("Папка выбрана")
        self.dialog = Dialog(self)
        self.hide()
        self.dialog.exec_()
        self.other_run()

    def other_run(self):
        self.worker = TryThresd(self,
                                'Zak',
                                'декабрь',
                                "A:AR",
                                range(0, 4))
        self.worker.start()
        self.worker.change_value.connect(self.write_df)
        self.worker2 = TryThresd(self,
                                 'Status',
                                 'Sheet1',
                                 "A:DA")
        self.worker2.start()
        self.worker2.change_value.connect(self.write_df)

    def write_df(self, val):
        '''Сохраняет отработавшие QThread в основной словарь'''
        self.MV[val[0]]=val[1][self.MV[val[0]]]
        self.isFinished()

    def isFinished(self):
        self.coun += 1
        print("Thread finished " + str(self.coun))
        if self.coun == 2:
            self.df_z = self.MV['Zak'].merge(self.MV['Status'],
                              how="left",
                              left_on="Заказ УИТ",
                              right_on="Внешний номер заказа")
            self.df_z= self.df_z.groupby(by=['Заказ УИТ',
                                           'Сбыт.зак. SAP',
                                          'Толщина, мм',
                                           'Ширина, мм',
                                           'Длина, мм',
                                           'Марка стали_x'])\
                                          .first().reset_index()  # костыль для вывода первого совпадения
            # self.df_z.info()

            self.CurStatus.addItem("Завершилось!!")
            self.sav_bu.show()

    def soxr_clicked(self):
        """Просто сохранялка потом напишу код"""
        # qm = QtWidgets.QMessageBox()#для выбора куда сохранять
        # res = qm.question(self, '',
        #                   "Сохранить в ту же папку?",
        #                   qm.Yes | qm.No, qm.Yes)
        #
        # if res == qm.Yes:
        #     # qm.information(self, '', self.wb_path)# отключить потом
        # else:
        #     self.wb_path=QtWidgets.QFileDialog.getExistingDirectory(self,
        #                                                      "Выберите папку",
        #                                                      self.wb_path )# убрать от греха
        #     # qm.information(self, '', self.wb_path)# отключить потом

        self.df_z.to_excel(self.wb_path +'\Test.xlsx', sheet_name='Sheet1', index=False)

        os.startfile(self.wb_path)  # открываем папку

class Dialog(QtWidgets.QDialog, Dialog.Ui_Dialog_next):
    def __init__(self, root):
        super().__init__(root)
        self.setupUi(self)
        self.main = root
        self.Text_path.setText(self.main.wb_path)

        self.knopk={"MNLZ":self.sklad_mnlz,
               "Nerez":self.sklad_nerez,
               "Rez":self.sklad_rez,
               "Zak":self.zakaz,
               "Status":self.status}

        inclu=[['Мнлз', 'мнлз'],
               ['нерез', 'не рез'],
               ['реза', 'рез'],
               ['ост', 'заказ'],
               ['статус', 'стат']]

        exc=[[],[],
             ['нерез', 'не рез'],
             [], []]
        for x,y,z in zip(self.knopk.values(),inclu,exc):
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
            elif (any(x in i.lower() for x in item_name)
                 and any(x in i.lower() for x in iskl)==False):
                cm_name.setCurrentText(i)
                break
        else:
            cm_name.setCurrentText("")

    # def keyPressEvent(self, event):
    #     if event.key() == QtCore.Qt.Key_Enter:
    #         self.button_clicked()

    def button_clicked(self):
        """Тут идет проверка на правильно выбранные значения
           и запись в словарь выбранные варианты"""
        #проверка на корректно заполненное значение
        self.main.show()
        tes_a=[]
        for x in self.knopk.values():
            tes_a.append(x.currentText())

        if len(tes_a)>len(set(tes_a)):
            msgBox = QtWidgets.QMessageBox()
            msgBox.setIcon(QtWidgets.QMessageBox.Information)
            msgBox.setText("задвоено значение")
            msgBox.setWindowTitle("Ошибка!")
            msgBox.exec_()
            return
        elif "" in tes_a:
            qm = QtWidgets.QMessageBox()
            res=qm.question(self, '', "Есть пустые значения, продолжить?", qm.Yes | qm.No,qm.No)

            if res==qm.Yes:
                qm.information(self, '', "Хер с тобой!")
            else:
                return

        # Запись в словарь
        self.main.CurStatus.addItem("Файлы выбраны")
        for key,value in self.knopk.items():
            self.main.file_dict[key]=value.currentText()

        self.close()

def window():
    app = QtWidgets.QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())

window()