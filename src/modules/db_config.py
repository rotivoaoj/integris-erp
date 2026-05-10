from src.database.database import conectar

def salvar_config(chave, valor):
    conn = conectar()
    cursor = conn.cursor()

    # Check if config already exists
    cursor.execute("SELECT COUNT(*) FROM configuracoes WHERE chave = ?", (chave,))
    exists = cursor.fetchone()[0] > 0

    if exists:
        # Update existing
        cursor.execute("UPDATE configuracoes SET valor = ? WHERE chave = ?", (str(valor), chave))
    else:
        # Insert new
        cursor.execute("INSERT INTO configuracoes (chave, valor) VALUES (?, ?)", (chave, str(valor)))

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