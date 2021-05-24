from sqlalchemy.engine import create_engine
import pandas as pd
import sys
def build_sql(_engine,
              _voc_check,
              _ms_df='dbo._Document117',
              _col_name="*",
              _condit="WHERE DATEDIFF_BIG(DAY, '4021-05-17 00:00:00',_Date_Time) >= 0",
              _sql_reqest_start="select"):

    """"Создает запрос mssql условиями на нужные столбцы.Перегенерурет на столбы в 1С

         :param _engine: Движлк для рабты с БД
         :type _df_c_type: slqalchemy engine

         :param _voc_check: Словарик для сопоставление
         :type _voc_check: dict

         :param _ms_df: Имя базы данных к которой надо подключиться
         :type _ms_df: str

         :param _col_name: Список колонок 1С для сопоставления
         :type _col_name: list

         :param _condit: Условие на T-SQL
         :type _condit: str

         :param _sql_reqest_start: На случай если надо допроверка перед select
         :type _sql_reqest_start: str

         :raises ValueError: Если типа данных T-SQL нет в словаре

         """
    try:
        _Sql_chek = """SELECT distinct
            c.name 'Column Name',
            t.Name 'Data type',
            c.max_length 'Max Length',
            c.precision ,
            c.scale ,
            c.is_nullable,
            ISNULL(i.is_primary_key, 0) 'Primary Key'
        FROM    
            sys.columns c
        INNER JOIN 
            sys.types t ON c.user_type_id = t.user_type_id
        LEFT OUTER JOIN 
            sys.index_columns ic ON ic.object_id = c.object_id AND ic.column_id = c.column_id
        LEFT OUTER JOIN 
            sys.indexes i ON ic.object_id = i.object_id AND ic.index_id = i.index_id
        WHERE
            c.object_id = OBJECT_ID('juvelirochka_DAILY.{}')""".format(_ms_df)
        _df_c_type=(pd.read_sql_query(_Sql_chek, _engine.connect())
          .drop_duplicates(subset=['Column Name', 'Data type'],
                           keep='last'))
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise

    _dic_type_change = {'binary': 1,
                        'datetime': 120,
                        'noraml': ['nchar', 'nvarchar', 'numeric']} #словарики под типы с заменами
    # _list_type_norm = ['nchar', 'nvarchar', 'numeric'] # типы которые можно не приобразовывать
    #Надо тут написать проверку на всякую муть
    if _col_name!="*":
        _anti_voc_check={x:y for y,x in _voc_check.items()} # словарь наоборот
        _col_name=[_col_name] if type(_col_name)==str else _col_name
        _l_chek=list(set(_col_name)-set(_anti_voc_check.keys()))
        if len(_l_chek)>0:  #Проверка на правильность названия
            raise ValueError ("Неверно указаные столбы \n{}".format(_l_chek))
        else:
            _col_name =[_anti_voc_check[x] for x in _col_name]
            _df_c_type=_df_c_type[_df_c_type['Column Name'].isin(_col_name)]
    _sql_reqest = _sql_reqest_start
    for x, y in zip(_df_c_type['Column Name'], _df_c_type['Data type']):
        if y != 'timestamp':
           if y in _dic_type_change['noraml']:
               _sql_reqest = _sql_reqest + '\n' + "{} as {},"\
                             .format(x, _voc_check[x])
           elif y in _dic_type_change.keys():
               _sql_reqest = _sql_reqest +'\n' + \
                             "CONVERT (VARCHAR(60),{},{}) as {},"\
                             .format(x,_dic_type_change[y], _voc_check[x])
           else:
               raise ValueError('Неверно указан тип данных SQL, {} добавляй в словарь'.format(y))

    _sql_reqest=_sql_reqest[:-1]+"\nFROM juvelirochka_DAILY.{}\n{} ".format(_ms_df,_condit)
    return _sql_reqest

if __name__=='__main__':
    print('ugu')