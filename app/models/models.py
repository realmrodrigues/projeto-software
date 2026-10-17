from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    login = Column(String(50), unique=True, nullable=False, index=True)
    senha_hash = Column(String(255), nullable=False)
    tipo = Column(String(20), nullable=False)  # "atendente" ou "tecnico"

    ordens = relationship("OrdemServico", back_populates="usuario")


class OrdemServico(Base):
    __tablename__ = "ordens_servico"

    id = Column(Integer, primary_key=True, index=True)
    numero_os = Column(String(20), unique=True, nullable=False, index=True)
    nome_cliente = Column(String(100), nullable=False)
    identificador_aparelho = Column(String(50), nullable=False)
    status_atual = Column(String(30), nullable=False, default="Em diagnóstico")
    data_entrada = Column(DateTime, default=datetime.utcnow)
    data_ultima_atualizacao = Column(DateTime, default=datetime.utcnow)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

    usuario = relationship("Usuario", back_populates="ordens")
