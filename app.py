from flask import Flask
import mysql.connector

app = Flask(__name__)

from flask import Flask
import mysql.connector

app = Flask(__name__)

@app.route("/teste-db")
def teste_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345",
            database="oficina"
        )

        if conn.is_connected():
            return "Conexão com MySQL funcionando!"

    except Exception as e:
        return f"Erro na conexão: {e}"

@app.route("/")
def home():
    return "Servidor Flask rodando!"

if __name__ == "__main__":
    app.run(debug=True)
