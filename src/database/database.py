import sqlite3
import os 
from src.settings.config import AMBIENTE, DB_DEV, DB_PROD

def conectar():

    if AMBIENTE == "DEV":
        caminho = DB_DEV
    else:
        caminho = DB_PROD

    # cria pasta se não existir
    os.makedirs(os.path.dirname(caminho), exist_ok=True)

    conn = sqlite3.connect(caminho)

    return conn

def criar_tabelas():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo TEXT UNIQUE,
        nome TEXT,
        tamanho TEXT,
        cor TEXT,
        preco_custo REAL,
        preco_venda REAL,
        estoque INTEGER,
        estoque_minimo INTEGER,
        imagem TEXT,
        data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS movimentacoes_estoque (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        produto_id INTEGER,
        tipo TEXT,
        quantidade INTEGER,
        motivo TEXT,
        data DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
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
        subtotal REAL
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS configuracoes (
        chave TEXT PRIMARY KEY,
        valor TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT UNIQUE,
        chave_hash TEXT NOT NULL,
        salt TEXT NOT NULL,
        ativo INTEGER DEFAULT 1
    )
    """)

    conn.commit()
    conn.close()