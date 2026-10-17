"""Testes unitários dos models"""

from datetime import datetime

from app.models.models import OrdemServico, Usuario


def test_criar_usuario():
    usuario = Usuario(
        nome="Jorge Alves",
        login="jorge.tecnico",
        senha_hash="hash_falso_para_teste",
        tipo="tecnico",
    )
    assert usuario.nome == "Jorge Alves"
    assert usuario.login == "jorge.tecnico"
    assert usuario.tipo == "tecnico"


def test_criar_ordem_servico():
    ordem = OrdemServico(
        numero_os="2026-0187",
        nome_cliente="Carlos Mendes",
        identificador_aparelho="356789012345678",
        status_atual="Em reparo",
        data_entrada=datetime.utcnow(),
        data_ultima_atualizacao=datetime.utcnow(),
        usuario_id=1,
    )
    assert ordem.numero_os == "2026-0187"
    assert ordem.status_atual == "Em reparo"


def test_status_permitidos():
    status_validos = ["Em diagnóstico", "Aguardando peça", "Em reparo", "Pronto para retirada"]
    for status in status_validos:
        ordem = OrdemServico(
            numero_os="TEST-001",
            nome_cliente="Teste",
            identificador_aparelho="123",
            status_atual=status,
            usuario_id=1,
        )
        assert ordem.status_atual == status
