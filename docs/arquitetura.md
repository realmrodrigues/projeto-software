# Arquitetura do Torotech Status

## Padrão adotado
Arquitetura Monolítica em Camadas

### Camadas
1. **Apresentação** – Templates Jinja2 (login, lista, detalhe)
2. **Aplicação** – Rotas FastAPI e regras de negócio
3. **Dados** – SQLAlchemy + SQLite

## Fluxo principal
Técnico atualiza status → Atendente consulta em tempo real
