import sqlite3
from db_functions import run_search_query


def get_master_data(p):
    """

    :param p:
    :return:
    """
    sql='select * from sqlite_master;'
    result = run_search_query(sql,p)
    print(type(result))
    for x in result:
        print(x)

def get_sqlite_schema(p):
    # name has been changed to sqlite_schema but still
    # seems to be master in this this installation
    sql="select name from sqlite_master;"
    result = run_search_query(sql, p)
    for x in result:
        print(x)


if __name__ == "__main__":
    db_path = 'dbase/triya_data.sqlite'
    #get_master_data(db_path)
    get_sqlite_schema(db_path)
    print()