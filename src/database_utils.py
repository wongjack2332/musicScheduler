import pymysql
import pymysql.cursors


HOST = 'localhost'
USER = 'root'
PASSWORD = 'root'
DATABASE_NAME = 'musicschedulerdb'


def get_connection():
    connection = pymysql.connect(host=HOST, user=USER, password=PASSWORD,
                                 db=DATABASE_NAME, cursorclass=pymysql.cursors.DictCursor)

    cursor = connection.cursor()
    return connection, cursor


def run_sql(cursor, statement):
    try:
        cursor.execute(statement)
    except pymysql.err.OperationalError:
        print("skipped, error in execution")

    return cursor.fetchall()


def close_connection(connection):
    connection.close()


if __name__ == "__main__":
    connection, cursor = get_connection()

    print(run_sql(cursor, "INSERT INTO users VALUES ()"))

    close_connection(connection)
