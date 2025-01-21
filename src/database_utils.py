import pymysql
import pymysql.cursors
connection = pymysql.connect(host='localhost', user='root', password='root', database='testdatabase', cursorclass=pymysql.cursors.DictCursor)   
print(connection)