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


def contar_movimentacoes():

    from src.database.database import conectar

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*) FROM movimentacoes_estoque
    """)

    total = cursor.fetchone()[0]
    conn.close()

    return total


def historico_movimentacoes_filtrado(filtro_produto, filtro_data, filtro_tipo, limite, offset):

    from src.database.database import conectar

    conn = conectar()
    cursor = conn.cursor()

    # Build the WHERE clause based on filters
    where_conditions = []
    params = []

    # FILTRO PRODUTO
    if filtro_produto:
        where_conditions.append("p.nome = ?")
        params.append(filtro_produto)

    # FILTRO DATA
    if filtro_data:
        from datetime import datetime

        try:
            data_formatada = datetime.strptime(
                filtro_data,
                "%d/%m/%Y"
            ).strftime("%Y-%m-%d")

            where_conditions.append("DATE(m.data) = ?")
            params.append(data_formatada)

        except:
            pass
        
    if filtro_tipo:
        where_conditions.append("m.tipo = ?")
        params.append(filtro_tipo)
        
    where_clause = " AND ".join(where_conditions) if where_conditions else "1=1"

    query = f"""
        SELECT 
            m.id,
            p.nome,
            m.tipo,
            m.quantidade,
            m.motivo,
            m.data
        FROM movimentacoes_estoque m
        JOIN produtos p ON p.id = m.produto_id
        WHERE {where_clause}
        ORDER BY m.data DESC
        LIMIT ? OFFSET ?
    """

    params.extend([limite, offset])
    cursor.execute(query, params)

    dados = cursor.fetchall()
    conn.close()

    formatted = []
    for row in dados:
        linha = list(row)
        linha[5] = data_hora_brasileira(linha[5])
        formatted.append(tuple(linha))

    return formatted


def contar_movimentacoes_filtrado(filtro_produto, filtro_data, filtro_tipo):

    from src.database.database import conectar

    conn = conectar()
    cursor = conn.cursor()

    # Build the WHERE clause based on filters
    where_conditions = []
    params = []

    # FILTRO PRODUTO
    if filtro_produto:
        where_conditions.append("p.nome = ?")
        params.append(filtro_produto)

    # FILTRO DATA
    if filtro_data:
        from datetime import datetime

        try:
            data_formatada = datetime.strptime(
                filtro_data,
               "%d/%m/%Y"
            ).strftime("%Y-%m-%d")

            where_conditions.append("DATE(m.data) = ?")
            params.append(data_formatada)

        except:
            pass

    if filtro_tipo:
        where_conditions.append("m.tipo = ?")
        params.append(filtro_tipo)
        
    where_clause = " AND ".join(where_conditions) if where_conditions else "1=1"

    query = f"""
        SELECT COUNT(*)
        FROM movimentacoes_estoque m
        JOIN produtos p ON p.id = m.produto_id
        WHERE {where_clause}
    """

    cursor.execute(query, params)

    total = cursor.fetchone()[0]
    conn.close()

    return total
