"""Testes unitários do serviço de autenticação"""
from app.services.auth_service import hash_senha, verificar_senha


def test_hash_senha_gera_hash_diferente_da_original():
    senha = "teste123"
    hash_gerado = hash_senha(senha)
    assert hash_gerado != senha
    assert len(hash_gerado) > 20


def test_verificar_senha_correta():
    senha = "teste123"
    hash_gerado = hash_senha(senha)
    assert verificar_senha(senha, hash_gerado) is True


def test_verificar_senha_incorreta():
    senha = "teste123"
    hash_gerado = hash_senha(senha)
    assert verificar_senha("senha_errada", hash_gerado) is False