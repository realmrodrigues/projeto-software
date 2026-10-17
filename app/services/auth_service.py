import bcrypt


def hash_senha(senha: str) -> str:
    """Gera hash bcrypt da senha."""
    senha_bytes = senha.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(senha_bytes, salt).decode("utf-8")


def verificar_senha(senha_plana: str, senha_hash: str) -> bool:
    """Verifica se a senha corresponde ao hash armazenado."""
    try:
        return bcrypt.checkpw(senha_plana.encode("utf-8"), senha_hash.encode("utf-8"))
    except Exception:
        return False
