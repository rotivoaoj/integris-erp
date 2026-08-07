import hashlib
import os
from src.database.database import conectar

HASH_NAME = "sha256"
ITERATIONS = 150000
SALT_SIZE = 16


def gerar_hash_chave(chave: str, salt: str | None = None) -> tuple[str, str]:
    if salt is None:
        salt_bytes = os.urandom(SALT_SIZE)
    else:
        salt_bytes = bytes.fromhex(salt)

    chave_bytes = chave.encode("utf-8")
    derived = hashlib.pbkdf2_hmac(HASH_NAME, chave_bytes, salt_bytes, ITERATIONS)
    return salt_bytes.hex(), derived.hex()


def existe_usuario() -> bool:
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    resultado = cursor.fetchone()
    conn.close()

    return bool(resultado and resultado[0] > 0)


def criar_usuario_inicial(chave: str, nome: str = "admin") -> None:
    salt, chave_hash = gerar_hash_chave(chave)
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE usuarios SET ativo = 0")
    cursor.execute(
        "INSERT OR REPLACE INTO usuarios (nome, chave_hash, salt, ativo) VALUES (?, ?, ?, 1)",
        (nome, chave_hash, salt)
    )
    conn.commit()
    conn.close()


def obter_usuario_admin() -> tuple[str, str] | None:
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT nome, chave_hash, salt FROM usuarios WHERE ativo = 1 ORDER BY id LIMIT 1"
    )
    resultado = cursor.fetchone()
    conn.close()

    return resultado if resultado else None


def validar_chave(chave: str) -> bool:
    usuario = obter_usuario_admin()
    if usuario is None:
        return False

    _, chave_hash, salt = usuario
    _, derived = gerar_hash_chave(chave, salt)
    return derived == chave_hash


def alterar_chave(chave_atual: str, chave_nova: str) -> bool:
    if not validar_chave(chave_atual):
        return False

    salt, chave_hash = gerar_hash_chave(chave_nova)
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE usuarios SET chave_hash = ?, salt = ? WHERE ativo = 1",
        (chave_hash, salt)
    )
    conn.commit()
    conn.close()
    return True
