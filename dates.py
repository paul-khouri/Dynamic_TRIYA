from datetime import datetime


def reformatSQLiteDate(sqlite_datestring):
    """Reformat SQLite date to d-m-y
    :param (str) sqlite_datestring:
    :return: (str) date
    """
    x = datetime.strptime(sqlite_datestring, '%Y-%m-%d %H:%M:%S')
    print(x.strftime("%d/%m/%Y"))
    print(x.strftime("%a %d %b %y %H:%M"))
    return x.strftime("%d/%m/%Y")


if __name__ == "__main__":
    date_str = "2022-07-30 06:40:00"
    print(reformatSQLiteDate(date_str))

