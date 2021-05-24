import sys
import pandas as pd
import numpy as np
import adodbapi as ado
import pickle
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
import sqlalchemy.pool as pool
from sqlalchemy import text
from sqlalchemy.pool import NullPool # для подключения мультипроцессора
from SQL_reques import build_sql
from dateutil.relativedelta import relativedelta
import datetime
from PyQt5 import QtCore
from PyQt5.QtCore import QThread

def connect():
    server = 'msk1-dbprod01.ves-media.com,1433'
    database = 'juvelirochka_DAILY'
    username = 'sdemyanosov@ves-media.com'
    password = 'YC3ex22r'
    return ado.connect("PROVIDER=MSOLEDBSQL;Data Source={0};Database={1}; \
       trusted_connection=yes;UID={2};PWD={3};".format(server,database ,username,password))

sql_test="""SELECT TOP 1*
            FROM juvelirochka_DAILY.dbo._Document117""" # просто для создания коннектап

mypool = pool.QueuePool(connect)
conn = mypool.connect()
curs = conn.cursor()
curs.execute(sql_test)
engine = create_engine('mssql+adodbapi://', module=ado, pool = mypool)

Session = sessionmaker()
Session.configure(bind=engine)
sess = Session()
vocl_path=r'C:\Users\sdemyanosov\Documents\Сверка\1c\slov'+'\\'

v_name='dic_Document117' # Зявка Клиент
dic_Document117 = pickle.load( open( vocl_path+v_name+".p", "rb" ) )


list_zak=['Ссылка',
          "Дата",
          "ВнешнийПроект",
          "ВидЗаявки",
          'Закрыта',
         'ЗакрытаДата',
          'Клиент',
          'ClientID',
          'СуммаТовара',
          'ТипЦены',
          'ДатаОплаты'
         ]

# Ловим актуальные дни
std=day_for_analize=datetime.datetime.now()-datetime.timedelta(days=7)

wher_con_zak="""WHERE Year(CONVERT (VARCHAR,_Date_Time,120))>={}
      and MONTH(CONVERT (VARCHAR,_Date_Time,120))>={} 
      and DAY(CONVERT (VARCHAR,_Date_Time,120))>={}""".format(std.year+2000,std.month,std.day)

sql_test1=build_sql(engine,
                    dic_Document117,
                    'dbo._Document117',
                    _condit=wher_con_zak,
                     _col_name=list_zak
                    )


class TryThresd(QThread):
#     change_value = QtCore.pyqtSignal(object)
    def __init__(self, _name):#,_engine,_sql_code):
         QThread.__init__(self)
         self.name = _name
#          self.engine = _engine
#          self.code=_sql_code
#          print(self.name,type(self.engine),type(self.code))
#
#
    def run(self):
        print("%s is running" % self.name)
#         _tem = pd.read_sql_query(self.code, self.engine.connect())
#         print("%s stop running" % self.name)
#         self.change_value.emit(_tem)
#
# # test = ""
#
# def write_df(val):
#     val.info()
#     # test = val
#     # test.info()
#
def other_run():
    worker = TryThresd("Тестовый1")#, engine, sql_test1)
#     try:
    worker.start()
#     except Exception:
#         e = sys.exc_info()[1]
#         print(e.args[0])
#     # worker.change_value.connect(write_df)

print("Поехали!")
other_run()