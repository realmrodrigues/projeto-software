"""Testes de integração das rotas"""

from fastapi.testclient import TestClient

from app.main import STATUS_PERMITIDOS, app

client = TestClient(app)


def test_pagina_login_carrega():
    response = client.get("/")
    assert response.status_code == 200


def test_acesso_ordens_sem_autenticacao_redireciona():
    response = client.get("/ordens", follow_redirects=False)
    assert response.status_code in [303, 302, 307]


def test_status_permitidos_constante():
    assert len(STATUS_PERMITIDOS) == 4
    assert "Em reparo" in STATUS_PERMITIDOS


def test_logout_redireciona():
    response = client.get("/logout", follow_redirects=False)
    assert response.status_code in [303, 302, 307]
