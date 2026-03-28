import pymysql
import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='12345',
    database='oficina'
)

print("Conectado!")