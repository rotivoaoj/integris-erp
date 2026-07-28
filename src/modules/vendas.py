from src.database import database
from src.modules.estoque import saida_estoque

def buscar_produto_por_codigo(codigo):

    conn = database.conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nome, preco_venda, estoque
        FROM produtos
        WHERE codigo = ?
    """, (codigo,))

    produto = cursor.fetchone()

    conn.close()

    return produto

def registrar_venda(itens):

    conn = database.conectar()
    cursor = conn.cursor()

    total = 0

    for item in itens:
        total += item["preco"] * item["quantidade"]

    cursor.execute("""
        INSERT INTO vendas (total, data)
        VALUES (?, datetime('now'))
    """, (total,))

    venda_id = cursor.lastrowid

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

    for item in itens:
        saida_estoque(
            item["id"],
            item["quantidade"],
            "Venda",
            conn  # 👈 AGORA USA MESMA CONEXÃO
        )

        subtotal = item["preco"] * item["quantidade"]
        cursor.execute("""
            INSERT INTO itens_venda
            (venda_id, produto_id, nome, quantidade, preco_unit, subtotal)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            venda_id,
            item["id"],
            item["nome"],
            item["quantidade"],
            item["preco"],
            subtotal
        ))

    conn.commit()
    conn.close()
    
def faturamento_do_dia():
    from src.database.database import conectar

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT SUM(total)
        FROM vendas
        WHERE data >= datetime('now', 'start of day')
    """)

    resultado = cursor.fetchone()[0]

    conn.close()

    return resultado if resultado else 0

def faturamento_do_mes():
    from src.database.database import conectar

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT SUM(total)
        FROM vendas
        WHERE data >= datetime('now', 'start of month')
    """)

    resultado = cursor.fetchone()[0]

    conn.close()

    return resultado if resultado else 0


def listar_vendas_do_dia():
    from src.database.database import conectar

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            v.id,
            v.total,
            v.data,
            iv.produto_id,
            iv.nome,
            iv.quantidade,
            iv.preco_unit,
            iv.subtotal
        FROM vendas v
        JOIN itens_venda iv ON iv.venda_id = v.id
        WHERE v.data >= datetime('now', 'start of day')
        ORDER BY v.data ASC, v.id ASC
    """)

    dados = cursor.fetchall()
    conn.close()

    return dados

def vendas_por_dia(mes_offset=0):
    from src.database.database import conectar

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT strftime('%d', data) as dia, SUM(total)
        FROM vendas
        WHERE strftime('%Y-%m', data) = strftime('%Y-%m', 'now', '{mes_offset} month')
        GROUP BY dia
        ORDER BY dia
    """)

    dados = cursor.fetchall()
    conn.close()

    dias = [int(d[0]) for d in dados]
    valores = [d[1] for d in dados]

    return dias, valores

def vendas_por_dia_mes_atual():
    from src.database.database import conectar

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT strftime('%d', data) as dia, SUM(total)
        FROM vendas
        WHERE strftime('%Y-%m', data) = strftime('%Y-%m', 'now')
        GROUP BY dia
        ORDER BY dia
    """)

    dados = cursor.fetchall()
    conn.close()

    return dados

def vendas_mes_anterior_total():
    from src.database.database import conectar

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT SUM(total)
        FROM vendas
        WHERE strftime('%Y-%m', data) = strftime('%Y-%m', 'now', '-1 month')
    """)

    resultado = cursor.fetchone()[0]
    conn.close()

    return resultado if resultado else 0
