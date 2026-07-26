from src.database.database import conectar

def criar_tabelas():

    conn = conectar()
    cursor = conn.cursor()

    # =========================
    # PRODUTOS
    # =========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo TEXT UNIQUE,
        nome TEXT,
        preco_venda REAL,
        estoque INTEGER,
        estoque_minimo INTEGER
    )
    """)

    # =========================
    # VENDAS
    # =========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vendas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        total REAL,
        data DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS itens_venda (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        venda_id INTEGER,
        produto_id INTEGER,
        nome TEXT,
        quantidade INTEGER,
        preco_unit REAL,
        subtotal REAL,
        FOREIGN KEY (venda_id) REFERENCES vendas(id)
    )
    """)

    # =========================
    # CONFIGURAÇÕES
    # =========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS configuracoes (
        chave TEXT PRIMARY KEY,
        valor TEXT
    )
    """)
    
    # =========================
    # MOVIMENTAÇÕES DE ESTOQUE
    # =========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS movimentacoes_estoque (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        produto_id INTEGER,
        tipo TEXT, -- entrada ou saida
        quantidade INTEGER,
        motivo TEXT,
        data TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (produto_id) REFERENCES produtos(id)
    )
    """)
    
    # ===== ATUALIZA VALORES ANTIGOS ======
    cursor.execute("""
        UPDATE vendas
        SET data = datetime('now')
        WHERE data IS NULL
    """)

    conn.commit()
    conn.close()