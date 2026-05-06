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
    CREATE TABLE IF NOT EXISTS configuracoes (
        chave TEXT PRIMARY KEY,
        valor TEXT
    )
    """)

    conn.commit()
    conn.close()