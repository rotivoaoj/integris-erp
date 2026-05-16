from src.database import database
from src.utils.formatacao import data_hora_brasileira

def entrada_estoque(produto_id, quantidade, motivo="Entrada manual"):

    conn = database.conectar()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE produtos
        SET estoque = estoque + ?
        WHERE id = ?
    """, (quantidade, produto_id))

    cursor.execute("""
        INSERT INTO movimentacoes_estoque
        (produto_id, tipo, quantidade, motivo)
        VALUES (?, 'entrada', ?, ?)
    """, (produto_id, quantidade, motivo))

    conn.commit()
    conn.close()


# 🔥 VERSÃO CORRETA (única)
def saida_estoque(produto_id, quantidade, motivo="Saída manual", conn=None):

    close_conn = False

    if conn is None:
        conn = database.conectar()
        close_conn = True

    cursor = conn.cursor()

    # 🔥 BUSCA ESTOQUE ATUAL
    cursor.execute("""
        SELECT estoque FROM produtos WHERE id = ?
    """, (produto_id,))

    estoque_atual = cursor.fetchone()[0]

    # 🚫 BLOQUEIO
    if quantidade > estoque_atual:
        if close_conn:
            conn.close()
        raise Exception("Estoque insuficiente")

    # ✅ ATUALIZA
    cursor.execute("""
        UPDATE produtos
        SET estoque = estoque - ?
        WHERE id = ?
    """, (quantidade, produto_id))

    # 📄 REGISTRA
    cursor.execute("""
        INSERT INTO movimentacoes_estoque
        (produto_id, tipo, quantidade, motivo)
        VALUES (?, 'saida', ?, ?)
    """, (produto_id, quantidade, motivo))

    if close_conn:
        conn.commit()
        conn.close()


def historico_movimentacoes():

    conn = database.conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            m.id,
            p.nome,
            m.tipo,
            m.quantidade,
            m.motivo,
            m.data
        FROM movimentacoes_estoque m
        JOIN produtos p ON p.id = m.produto_id
        ORDER BY m.data DESC
    """)

    dados = cursor.fetchall()

    conn.close()

    formatted = []
    for row in dados:
        linha = list(row)
        linha[5] = data_hora_brasileira(linha[5])
        formatted.append(tuple(linha))

    return formatted

def historico_movimentacoes_paginado(limite, offset):

    from src.database.database import conectar

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            m.id,
            p.nome,
            m.tipo,
            m.quantidade,
            m.motivo,
            m.data
        FROM movimentacoes_estoque m
        JOIN produtos p ON p.id = m.produto_id
        ORDER BY m.data DESC
        LIMIT ? OFFSET ?
    """, (limite, offset))

    dados = cursor.fetchall()
    conn.close()

    formatted = []
    for row in dados:
        linha = list(row)
        linha[5] = data_hora_brasileira(linha[5])
        formatted.append(tuple(linha))

    return formatted