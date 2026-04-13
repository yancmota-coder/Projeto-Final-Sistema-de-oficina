import sqlite3

conn = sqlite3.connect("oficina.db")
cursor = conn.cursor()

# Ativar chaves estrangeiras
cursor.execute("PRAGMA foreign_keys = ON;")

# ---------------- CLIENTES ----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    telefone TEXT,
    email TEXT
)
""")

# ---------------- VEICULOS ----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS veiculos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER,
    marca TEXT,
    modelo TEXT,
    placa TEXT,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE
)
""")

# ---------------- MECANICOS ----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS mecanicos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    especialidade TEXT
)
""")

# ---------------- PEÇAS ----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS pecas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    codigo TEXT,
    quantidade_estoque INTEGER DEFAULT 0,
    preco_venda REAL
)
""")

# ---------------- ORDENS DE SERVIÇO ----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS ordens_servico (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER,
    veiculo_id INTEGER,
    mecanico_id INTEGER,
    status TEXT DEFAULT 'ABERTA',
    problema_relatado TEXT,
    data_abertura DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (cliente_id) REFERENCES clientes(id),
    FOREIGN KEY (veiculo_id) REFERENCES veiculos(id),
    FOREIGN KEY (mecanico_id) REFERENCES mecanicos(id)
)
""")

# ---------------- ITENS DA OS ----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS os_itens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    os_id INTEGER,
    peca_id INTEGER,
    descricao TEXT,
    tipo TEXT, -- PECA ou SERVICO
    quantidade INTEGER,
    valor_unitario REAL,
    valor_total REAL,

    FOREIGN KEY (os_id) REFERENCES ordens_servico(id) ON DELETE CASCADE,
    FOREIGN KEY (peca_id) REFERENCES pecas(id)
)
""")

conn.commit()
conn.close()

print("Banco criado com sucesso 🔥")