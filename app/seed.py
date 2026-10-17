"""
Script para popular o banco com dados iniciais de demonstração.
Execute: python -m app.seed
"""
from app.database import SessionLocal, engine, Base
from app.models.models import Usuario, OrdemServico
from passlib.context import CryptContext
from datetime import datetime, timedelta

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

Base.metadata.create_all(bind=engine)
db = SessionLocal()

# Limpa dados existentes (apenas para demonstração)
db.query(OrdemServico).delete()
db.query(Usuario).delete()
db.commit()

# Cria usuários
tecnico = Usuario(
    nome="Jorge Alves",
    login="jorge.tecnico",
    senha_hash=pwd_context.hash("teste123"),
    tipo="tecnico"
)
atendente = Usuario(
    nome="Maria Silva",
    login="maria.atendente",
    senha_hash=pwd_context.hash("teste123"),
    tipo="atendente"
)
db.add(tecnico)
db.add(atendente)
db.commit()
db.refresh(tecnico)

# Cria ordens de serviço
ordens = [
    OrdemServico(
        numero_os="2026-0187",
        nome_cliente="Carlos Mendes",
        identificador_aparelho="356789012345678",
        status_atual="Em reparo",
        data_entrada=datetime.utcnow() - timedelta(days=2),
        data_ultima_atualizacao=datetime.utcnow() - timedelta(hours=3),
        usuario_id=tecnico.id
    ),
    OrdemServico(
        numero_os="2026-0191",
        nome_cliente="Ana Paula Ribeiro",
        identificador_aparelho="359876543210987",
        status_atual="Aguardando peça",
        data_entrada=datetime.utcnow() - timedelta(days=1),
        data_ultima_atualizacao=datetime.utcnow() - timedelta(hours=8),
        usuario_id=tecnico.id
    ),
    OrdemServico(
        numero_os="2026-0193",
        nome_cliente="Roberto Lima",
        identificador_aparelho="351234567890123",
        status_atual="Pronto para retirada",
        data_entrada=datetime.utcnow() - timedelta(days=3),
        data_ultima_atualizacao=datetime.utcnow() - timedelta(hours=1),
        usuario_id=tecnico.id
    ),
]

for ordem in ordens:
    db.add(ordem)

db.commit()
print("Banco populado com sucesso!")
print("Usuários criados:")
print("  - jorge.tecnico / teste123 (técnico)")
print("  - maria.atendente / teste123 (atendente)")
db.close()
