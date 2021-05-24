def get_data_from_db(_month, _where,
             _end_day=None,
             _year=datetime.date.today().year
             ):
    """Забирает информацию из базы ua_juvelir
        за указанный период и возврашает ввиде масива pandas"""

    if type(_month) not in ([int]) or \
            _month > 12 or \
            _month < 1:
        print("Неверно указан месяц")
        return

    _end_day = calendar.monthrange(_year, _month)[1] if _end_day == None else _end_day

    # Подключение к тонелю
    with SSHTunnelForwarder(
            ('92.242.47.188', 2200),
            ssh_username="sdemyanosov",
            ssh_password="5rC6RwWD",
            remote_bind_address=('localhost', 3306),
    ) as server:

        if server.local_bind_port > 0:
            print("Подключение к SSH есть")
        else:
            print("Нет подключение к SSH")
            return

        # подключение к базе
        mydb = mysql.connector.connect(
            host="localhost",
            user="sdemyanosov",
            password="j8N9GhR7g3",
            port=server.local_bind_port,
            db='ua_juvelir'
        )
        print("Подключение к базе -", mydb.is_connected())

        _m_take = "0" + str(_month) if _month < 10 else str(_month)
        __start = '{}-{}-01'.format(_year,
                                    _m_take)
        __finish = '{}-{}-{}'.format(_year,
                                     _m_take,
                                     _end_day)

        select_calls_query = """
                       SELECT * FROM ua_juvelir.{}
                       WHERE callid  between UNIX_TIMESTAMP('{}') AND UNIX_TIMESTAMP('{}')
                     """.format(_where, __start, __finish)
        return pd.read_sql_query(select_calls_query, mydb)


if __name__ == "__main__":
    get_data_from_db()

