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


@app.route("/os")
def listar_os():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT os.*, c.nome as cliente_nome, v.modelo as veiculo_modelo, m.nome as mecanico_nome
        FROM ordens_servico os
        JOIN clientes c ON os.cliente_id = c.id
        JOIN veiculos v ON os.veiculo_id = v.id
        JOIN mecanicos m ON os.mecanico_id = m.id
    """)

    ordens = cursor.fetchall()

    return render_template("os.html", ordens=ordens)

@app.route("/os/nova")
def nova_os():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()

    cursor.execute("SELECT * FROM veiculos")
    veiculos = cursor.fetchall()

    cursor.execute("SELECT * FROM mecanicos")
    mecanicos = cursor.fetchall()

    return render_template(
        "nova_os.html",
        clientes=clientes,
        veiculos=veiculos,
        mecanicos=mecanicos
    )

@app.route("/os/criar", methods=["POST"])
def criar_os():
    cliente_id = request.form["cliente_id"]
    veiculo_id = request.form["veiculo_id"]
    mecanico_id = request.form["mecanico_id"]
    problema = request.form["problema"]

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO ordens_servico 
        (cliente_id, veiculo_id, mecanico_id, status, problema_relatado)
        VALUES (%s, %s, %s, %s, %s)
    """, (cliente_id, veiculo_id, mecanico_id, "ABERTA", problema))

    conn.commit()

    return redirect("/os")

@app.route("/os/<int:id>")
def ver_os(id):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    # dados da OS
    cursor.execute("""
        SELECT os.*, c.nome as cliente, v.modelo as veiculo, m.nome as mecanico
        FROM ordens_servico os
        JOIN clientes c ON os.cliente_id = c.id
        JOIN veiculos v ON os.veiculo_id = v.id
        JOIN mecanicos m ON os.mecanico_id = m.id
        WHERE os.id = %s
    """, (id,))
    os = cursor.fetchone()

    # itens da OS
    cursor.execute("SELECT * FROM os_itens WHERE os_id=%s", (id,))
    itens = cursor.fetchall()

    # peças disponíveis
    cursor.execute("SELECT * FROM pecas")
    pecas = cursor.fetchall()

    cursor.execute("""
    SELECT SUM(valor_total) as total
    FROM os_itens
    WHERE os_id=%s
    """, (id,))
    total = cursor.fetchone()["total"] or 0

    return render_template("ver_os.html", os=os, itens=itens, pecas=pecas, total=total)

@app.route("/os/<int:id>/add-peca", methods=["POST"])
def add_peca(id):
    peca_id = request.form["peca_id"]
    quantidade = int(request.form["quantidade"])

    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    # pegar peça
    cursor.execute("SELECT * FROM pecas WHERE id=%s", (peca_id,))
    peca = cursor.fetchone()

    valor_unitario = peca["preco_venda"]
    valor_total = valor_unitario * quantidade

    # inserir item
    cursor.execute("""
        INSERT INTO os_itens
        (os_id, peca_id, descricao, tipo, quantidade, valor_unitario, valor_total)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        id, peca_id, peca["nome"], "PECA",
        quantidade, valor_unitario, valor_total
    ))

    # 🔥 REDUZ ESTOQUE
    cursor.execute("""
        UPDATE pecas
        SET quantidade_estoque = quantidade_estoque - %s
        WHERE id = %s
    """, (quantidade, peca_id))

    conn.commit()

    return redirect(f"/os/{id}")

@app.route("/os/<int:id>/add-servico", methods=["POST"])
def add_servico(id):
    descricao = request.form["descricao"]
    valor = float(request.form["valor"])

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO os_itens
        (os_id, descricao, tipo, quantidade, valor_unitario, valor_total)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (id, descricao, "SERVICO", 1, valor, valor))

    conn.commit()

    return redirect(f"/os/{id}")

@app.route("/relatorios/os-abertas")
def os_abertas():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT os.*, c.nome as cliente, v.modelo as veiculo
        FROM ordens_servico os
        JOIN clientes c ON os.cliente_id = c.id
        JOIN veiculos v ON os.veiculo_id = v.id
        WHERE os.status = 'ABERTA'
    """)

    ordens = cursor.fetchall()

    return render_template("relatorio_os_abertas.html", ordens=ordens)

@app.route("/relatorios/estoque-baixo")
def estoque_baixo():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM pecas
        WHERE quantidade_estoque <= 5
    """)

    pecas = cursor.fetchall()

    return render_template("relatorio_estoque.html", pecas=pecas)

@app.route("/relatorios/os-concluidas")
def os_concluidas():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT os.*, c.nome as cliente
        FROM ordens_servico os
        JOIN clientes c ON os.cliente_id = c.id
        WHERE os.status = 'CONCLUIDA'
    """)

    ordens = cursor.fetchall()

    return render_template("relatorio_concluidas.html", ordens=ordens)

if __name__ == "__main__":
    app.run(debug=True)