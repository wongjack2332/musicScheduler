import pymysql
import pymysql.cursors


HOST = 'localhost'
USER = 'root'
PASSWORD = 'root'
DATABASE_NAME = 'musicschedulerdb'


def get_connection():
    connection = pymysql.connect(host=HOST, user=USER, password=PASSWORD,
                                 db=DATABASE_NAME, cursorclass=pymysql.cursors.DictCursor)

    return connection


def run_sql(cursor, statement):
    try:
        cursor.execute(statement)
    except pymysql.err.OperationalError:
        print("skipped, error in execution")
        return list()

    return cursor.fetchall()


def close_connection(connection):
    connection.close()


if __name__ == "__main__":
    pass
