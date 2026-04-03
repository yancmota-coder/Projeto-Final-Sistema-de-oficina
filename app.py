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

    # 1. Apagar veículos do cliente
    cursor.execute("DELETE FROM veiculos WHERE cliente_id=%s", (id,))

    # 2. Apagar cliente
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

@app.route("/mecanicos")
def listar_mecanicos():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM mecanicos")
    mecanicos = cursor.fetchall()

    return render_template("mecanicos.html", mecanicos=mecanicos)

@app.route("/mecanicos/novo")
def novo_mecanico():
    return render_template("novo_mecanico.html")

@app.route("/mecanicos/criar", methods=["POST"])
def criar_mecanico():
    nome = request.form["nome"]
    especialidade = request.form["especialidade"]

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO mecanicos (nome, especialidade) VALUES (%s, %s)",
        (nome, especialidade)
    )
    conn.commit()

    return redirect("/mecanicos")

@app.route("/mecanicos/editar/<int:id>")
def editar_mecanico(id):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM mecanicos WHERE id=%s", (id,))
    mecanico = cursor.fetchone()

    return render_template("editar_mecanico.html", mecanico=mecanico)

@app.route("/mecanicos/deletar/<int:id>")
def deletar_mecanico(id):
    conn = conectar()
    cursor = conn.cursor()

    # 2. Apagar mecanico
    cursor.execute("DELETE FROM mecanicos WHERE id=%s", (id,))

    conn.commit()

    return redirect("/mecanicos")

@app.route("/mecanicos/atualizar/<int:id>", methods=["POST"])
def atualizar_mecanico(id):
    nome = request.form["nome"]
    especialidade = request.form["especialidade"]

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE mecanicos SET nome=%s, especialidade=%s WHERE id=%s",
        (nome, especialidade, id)
    )

    conn.commit()

    return redirect("/mecanicos")

@app.route("/pecas")
def listar_pecas():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM pecas")
    pecas = cursor.fetchall()

    return render_template("pecas.html", pecas=pecas)

@app.route("/pecas/novo")
def nova_peca():
    return render_template("nova_peca.html")

@app.route("/pecas/criar", methods=["POST"])
def criar_peca():
    nome = request.form["nome"]
    codigo = request.form["codigo"]
    quantidade = int(request.form["quantidade_estoque"])
    preco = float(request.form["preco_venda"])

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO pecas (nome, codigo, quantidade_estoque, preco_venda) VALUES (%s, %s, %s, %s)",
        (nome, codigo, quantidade, preco)
    )

    conn.commit()

    return redirect("/pecas")

@app.route("/pecas/editar/<int:id>")
def editar_peca(id):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM pecas WHERE id=%s", (id,))
    peca = cursor.fetchone()

    return render_template("editar_peca.html", peca=peca)

@app.route("/pecas/atualizar/<int:id>", methods=["POST"])
def atualizar_peca(id):
    nome = request.form["nome"]
    codigo = request.form["codigo"]
    quantidade_estoque = int(request.form["quantidade_estoque"])
    preco_venda = float(request.form["preco_venda"])

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE pecas SET nome=%s, codigo=%s, quantidade_estoque=%s, preco_venda=%s WHERE id=%s",
        (nome, codigo, quantidade_estoque, preco_venda, id)
    )

    conn.commit()

    return redirect("/pecas")

@app.route("/pecas/deletar/<int:id>")
def deletar_peca(id):
    conn = conectar()
    cursor = conn.cursor()

    # 2. Apagar peça
    cursor.execute("DELETE FROM pecas WHERE id=%s", (id,))

    conn.commit()

    return redirect("/pecas")

if __name__ == "__main__":
    app.run(debug=True)