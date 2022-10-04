import sqlite3

def execute_external_script(sql_script_path, db_path):
    """Run a Query using an external .sql

    :param (str) sql_query:
    :param (path) file_path:
    :return: (tuple) result
    """

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        print("connection successful")
        sql_query = open(sql_script_path)
        print("sql query" )
        sql_string = sql_query.read()
        cursor.executescript(sql_string)
        conn.commit()
        print("Query executed")
        cursor.close()
    except sqlite3.Error as error:
        print("Error while executing sql: {}".format(error))
        return False
    except IOError as error:
        print("Error: {}".format(error))
        return False
    if conn:
        conn.close()
        return True
    else:
        return False
        #print("sqlite connection is closed")


def run_search_query(sql_query, file_path, rowfactory=True):
    """Get results from an sql query

    :param sql_query: str
    :param file_path: str
    :param rowfactory: bool
    :return: tuple
    """

    try:
        db = sqlite3.connect(file_path)
        # will get multi dict rather than tuples, needs flask
        if rowfactory:
            db.row_factory = sqlite3.Row
        cursor = db.cursor()
        #print("connection successful")
        cursor.execute(sql_query)
        result = cursor.fetchall()
        #print("Search Query executed")
        cursor.close()
    except sqlite3.Error as error:
        print("Error while creating sqlite table: {}".format(error))
    finally:
        if db:
            db.close()
            #print("sqlite connection is closed")
        if result:
            return result

# tests
if __name__ == "__main__":
    db_path = 'dbase/triya_data.sqlite'
    sql_script_path = 'dbase/installer.sql'
    #open(sql_script_path)
    result = execute_external_script(sql_script_path,db_path)
    print(result)