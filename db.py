<<<<<<< HEAD
import sqlite3

def conectar():
    conn = sqlite3.connect("oficina.db")
    conn.row_factory = sqlite3.Row
    return conn
=======
import pymysql
import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='12345',
    database='oficina'
)

print("Conectado!")
>>>>>>> 45533e5ce9431b8f2bdef6d081c9f64f848c7640
