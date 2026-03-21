from flask import Flask, render_template, request, redirect
from db import conectar

app = Flask(__name__)

@app.route("/")
def home():
    return "Olá Mundo - Sistema de Oficina"

@app.route("/teste-db")
def teste_db():
    conn = conectar()

    if conn.is_connected():
        return "Conexão com MySQL funcionando!"
    else:
        return "Erro na conexão"
    
@app.route("/clientes")
def listar_clientes():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT c.id, c.nome, c.telefone, v.marca, v.modelo
        FROM clientes c
        LEFT JOIN veiculos v ON c.id = v.cliente_id
        """)
    clientes = cursor.fetchall()

    return render_template("clientes.html", clientes=clientes)

@app.route("/clientes/novo")
def novo_cliente():
    return render_template("novo_cliente.html")


@app.route("/clientes/criar", methods=["POST"])
def criar_cliente():
    nome = request.form["nome"]
    telefone = request.form["telefone"]
    email = request.form["email"]

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO clientes (nome, telefone, email) VALUES (%s, %s, %s)",
        (nome, telefone, email)
    )

    conn.commit()

    return redirect("/clientes")

@app.route("/clientes/deletar/<int:id>")
def deletar_cliente(id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM clientes WHERE id=%s", (id,))
    conn.commit()

    return redirect("/clientes")


@app.route("/clientes/editar/<int:id>")
def editar_cliente(id):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM clientes WHERE id=%s", (id,))
    cliente = cursor.fetchone()

    return render_template("editar_cliente.html", cliente=cliente)

@app.route("/clientes/atualizar/<int:id>", methods=["POST"])
def atualizar_cliente(id):
    nome = request.form["nome"]
    telefone = request.form["telefone"]
    email = request.form["email"]

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE clientes SET nome=%s, telefone=%s, email=%s WHERE id=%s",
        (nome, telefone, email, id)
    )

    conn.commit()

    return redirect("/clientes")

@app.route("/clientes/<int:id>/veiculos/novo")
def novo_veiculo(id):
    return render_template("novo_veiculo.html", cliente_id=id)

@app.route("/veiculos/criar", methods=["POST"])
def criar_veiculo():
    cliente_id = request.form["cliente_id"]
    marca = request.form["marca"]
    modelo = request.form["modelo"]
    placa = request.form["placa"]

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO veiculos (cliente_id, marca, modelo, placa) VALUES (%s, %s, %s, %s)",
        (cliente_id, marca, modelo, placa)
    )

    conn.commit()

    return redirect("/clientes")

if __name__ == "__main__":
    app.run(debug=True)