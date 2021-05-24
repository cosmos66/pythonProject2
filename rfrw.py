import adodbapi as ado
server = 'msk1-dbprod01.ves-media.com,1433'
database = 'juvelirochka_DAILY'
username = 'sdemyanosov@ves-media.com'
password = 'YC3ex22r'
# curs=ado.connect("PROVIDER=MSOLEDBSQL;Data Source={0};Database={1}; \
#       trusted_connection=yes;UID={2};PWD={3};".format(server, database, username, password))
conn = ado.connect("PROVIDER=MSOLEDBSQL;Data Source={0};Database={1}; \
       trusted_connection=yes;UID={2};PWD={3};".format(server,database ,username,password))
cur = conn.cursor()
sql_test="""SELECT TOP 1*
            FROM juvelirochka_DAILY.dbo._Document117""" # просто для создания коннектап

cur.execute(sql_test)