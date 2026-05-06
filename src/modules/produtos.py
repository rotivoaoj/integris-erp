from src.database.database import conectar

def salvar_produto(dados):

    conn = conectar()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
        INSERT INTO produtos
        (codigo, nome, tamanho, cor, preco_custo, preco_venda, estoque, estoque_minimo, imagem)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, dados)
        conn.commit()
    finally:
        conn.close()

def listar_produtos():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            codigo,
            nome,
            preco_venda,
            estoque,
            estoque_minimo
        FROM produtos
    """)

    produtos = cursor.fetchall()

    conn.close()

    return produtos


def excluir_produto(id_produto):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM produtos
        WHERE id = ?
    """, (id_produto,))

    conn.commit()
    conn.close()

def inserir_produto(codigo, nome, preco_venda, estoque):

    conn = conectar()
    cursor = conn.cursor()

    # verificar se já existe
    cursor.execute("SELECT id FROM produtos WHERE codigo = ?", (codigo,))
    existe = cursor.fetchone()

    if existe:
        print("Código já cadastrado!")
        conn.close()
        return

    cursor.execute("""
        INSERT INTO produtos
        (codigo, nome, preco_venda, estoque)
        VALUES (?, ?, ?, ?)
    """, (codigo, nome, preco_venda, estoque))

    conn.commit()
    conn.close()
    
def atualizar_produto(id_produto, codigo, nome, preco_venda, estoque):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE produtos
        SET codigo = ?, nome = ?, preco_venda = ?, estoque = ?
        WHERE id = ?
    """, (codigo, nome, preco_venda, estoque, id_produto))

    conn.commit()
    conn.close()
    
def valor_total_estoque():
    from src.database.database import conectar

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT SUM(preco_venda * estoque) FROM produtos
    """)

    resultado = cursor.fetchone()[0]

    conn.close()

    return resultado if resultado else 0