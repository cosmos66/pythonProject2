from PyQt5 import QtCore
from PyQt5.QtCore import QThread


sql_text="""select
CONVERT (VARCHAR,_Date_Time,120) as Дата,
CONVERT (VARCHAR,_Fld2435RRef,1) as Валюта,
CONVERT (VARCHAR,_Fld2436RRef,1) as ВидДЗ,
CONVERT (VARCHAR,_Fld2437,120) as ДатаОплаты,
CONVERT (VARCHAR,_Fld2439_RRRef,1) as Заказ2,
CONVERT (VARCHAR,_Fld2444RRef,1) as Покупатель,
CONVERT (VARCHAR,_Fld2447RRef,1) as Проект,
CONVERT (VARCHAR,_Fld2460RRef,1) as Причина,
CONVERT (VARCHAR,_IDRRef,1) as Ссылка,
_Number as Номер
FROM juvelirochka_DAILY.dbo._Document108
WHERE Year(CONVERT (VARCHAR,_Date_Time,120))>=4021
      and MONTH(CONVERT (VARCHAR,_Date_Time,120))>=5 
      and DAY(CONVERT (VARCHAR,_Date_Time,120))>=13"""


class TryThresd(QThread):
    change_value = QtCore.pyqtSignal(object)
    def __init__(self, _name):#,_sql_cod):#,_engine,_sql_code):
         QThread.__init__(self)
         self.name = _name
#          self.engine = _engine
#          self.code=_sql_cod
#          print(self.name,type(self.engine),type(self.code))
#
#
    def run(self):
        print(self.name + " Poexali!")
        # server = 'msk1-dbprod01.ves-media.com,1433'
        # database = 'juvelirochka_DAILY'
        # username = 'sdemyanosov@ves-media.com'
        # password = 'YC3ex22r'
        # conn = ado.connect("PROVIDER=MSOLEDBSQL;Data Source={0};Database={1}; \
        #        trusted_connection=yes;UID={2};PWD={3};".format(server, database, username, password))
        # curs = conn.cursor()
        # curs.execute(self.code)
        # data = curs.fetchone()[0]
        # print(self.name + "Закончили!")
        print(self.name + " stop")
        self.change_value.emit(self.name)

def write_df(val):
    print(val + "kfkfkklf")

worker =TryThresd("Тестовый1")#, engine, sql_test1)

worker2 = TryThresd("Тестовый2")#, engine, sql_test1)
worker2.start()
worker.start()

worker.change_value.connect(write_df)