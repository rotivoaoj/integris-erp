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

    for item in itens:
        saida_estoque(
            item["id"],
            item["quantidade"],
            "Venda",
            conn  # 👈 AGORA USA MESMA CONEXÃO
        )

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