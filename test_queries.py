import sqlite3
from db_functions import run_search_query, run_commit_query, run_search_query_tuples


#@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r



def get_master_data(p):
    """

    :param p:
    :return:
    """
    sql = 'select * from sqlite_master;'
    result = run_search_query(sql,p)
    print(type(result))
    for x in result:
        print(x)


def get_sqlite_schema(p):
    # name has been changed to sqlite_schema but still
    # seems to be master in this this installation
    sql = 'select name from sqlite_master;'
    result = run_search_query(sql, p)
    for x in result:
        for y in x:
            print(y)



def get_page_one(p):
    sql = 'select header, content, image from page where pagenumber = 1;'
    result = run_search_query(sql,p)
    return result


def get_programs(p):
    sql = 'select name, subtitle, content, coachingfee, boathire, coachingfee+boathire ' \
          'as "total", image, updated_at from programs;'
    result = run_search_query(sql,p)
    return result


def insert_member(p):
    sql = """
    insert into member(first_name,second_name,email,password,authorisation)
    values(?,?,?,?,?,?,date('now'),?,?,?); """
    values_tuple = ("Warren", "Smith", "021236673", "waz@gmail.com", "67 Noodle Lane", "Karori", "admin", "temp", 0)
    run_commit_query(sql, values_tuple,p)


def get_news(p):
    sql = "select news_id, title, content from news;"
    result = run_search_query(sql,p)
    return result


if __name__ == "__main__":
    db_path = 'dbase/triya_data.sqlite'
    #get_master_data(db_path)
    #get_sqlite_schema(db_path)
    program_data = get_programs(db_path)
    for x in program_data:
        print(x.keys())
        print(x['updated_at'])
        print(x['total'])
    #insert_member(db_path)
    #get_news(db_path)
    #get_sqlite_schema(db_path)
    print()