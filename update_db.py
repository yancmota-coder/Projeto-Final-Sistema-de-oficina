import sqlite3

conn = sqlite3.connect("oficina.db")
cursor = conn.cursor()

try:
    cursor.execute("""
    ALTER TABLE ordens_servico
    ADD COLUMN data_conclusao DATETIME
    """)
    print("Coluna criada com sucesso 🔥")
except Exception as e:
    print("Erro ou já existe:", e)

conn.commit()
conn.close()