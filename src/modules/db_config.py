from src.database.database import conectar

def salvar_config(chave, valor):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO configuracoes (chave, valor)
        VALUES (?, ?)
        ON CONFLICT(chave) DO UPDATE SET valor=excluded.valor
    """, (chave, str(valor)))

    conn.commit()
    conn.close()


def obter_config(chave, padrao=None):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT valor FROM configuracoes WHERE chave = ?", (chave,))
    resultado = cursor.fetchone()

    conn.close()

    if resultado:
        return resultado[0]

    return padrao