import mysql.connector

def conectar():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="gui2008pwgb",  # coloque sua senha se tiver
        database="oficina"
    )
    return conn