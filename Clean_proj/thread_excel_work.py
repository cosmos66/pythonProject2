import sys, time
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox, QComboBox


class TH_Zakaz(QThread):
    """работает с файлом заказа после его прочтения"""
    catch_back=QtCore.pyqtSignal(object)

    def __init__(self,root,zash):
        super().__init__(root)
        self.main=root
        self._l1= ["Получатель",
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
        self._df=zash

    def run(self):
        self.main.CurStatus.addItem("Заказ приехал")
        self.catch_back.emit(self._df[self._l1])

class TH_Statys(QThread):
    """работает с файлом заказа после его прочтения"""
    catch_back=QtCore.pyqtSignal(object)

    def __init__(self,root,stat):
        super().__init__(root)
        self.main=root
        self._l1= ['Номер контракта',
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
        self._df=stat

    def run(self):
        self.main.CurStatus.addItem("Статус приехал")
        self.catch_back.emit(self._df[self._l1])

# if __name__=='__main__':
#     app = QApplication(sys.argv)
#     win = TH_Zakaz()
#     sys.exit(app.exec_())