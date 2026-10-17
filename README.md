# Torotech Status

MVP de controle de status de ordens de serviço para a assistência técnica **Torotech** (Centro do Rio de Janeiro).

## 🎯 Problema que resolve

Falha de comunicação entre o atendimento e os técnicos sobre o status real dos aparelhos em reparo. O sistema permite que o técnico atualize o status de forma rápida e que o atendente consulte essa informação em tempo real.

## 🛠️ Tecnologias

- **Python 3.12**
- **FastAPI**
- **Jinja2** (templates)
- **SQLAlchemy** + **SQLite**
- **Passlib** (bcrypt) para hash de senhas

## 📋 Pré-requisitos

- Python 3.12+
- pip

## 🚀 Como executar localmente

```bash
# 1. Clone o repositório
git clone https://github.com/realmrodrigues/projeto-software.git
cd projeto-software

# 2. Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate   # Linux/macOS
# ou
venv\Scripts\activate      # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Popule o banco com dados de demonstração
python -m app.seed

# 5. Inicie o servidor
uvicorn app.main:app --reload
```

Acesse: http://localhost:8000

### Usuários de demonstração

| Login            | Senha     | Perfil     |
|------------------|-----------|------------|
| jorge.tecnico    | teste123  | Técnico    |
| maria.atendente  | teste123  | Atendente  |

## 📁 Estrutura do projeto

```
torotech-status/
├── app/
│   ├── main.py              # Aplicação principal e rotas
│   ├── database.py          # Configuração do banco
│   ├── models/
│   │   └── models.py        # Entidades (Usuario, OrdemServico)
│   ├── templates/           # Telas HTML
│   │   ├── login.html
│   │   ├── lista_ordens.html
│   │   └── detalhe_ordem.html
│   ├── seed.py              # Dados iniciais de demonstração
│   └── static/              # Arquivos estáticos
├── requirements.txt
├── .env.example
└── README.md
```

## 🔒 Segurança

- Senhas armazenadas com bcrypt (nunca em texto puro)
- Autenticação obrigatória para operações de atualização e consulta
- Validação de status permitidos no servidor

## 📄 Licença

Projeto acadêmico - Análise e Desenvolvimento de Sistemas.
