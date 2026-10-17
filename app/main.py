from fastapi import FastAPI, Request, Depends, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime
import os

from app.database import engine, get_db, Base
from app.models.models import Usuario, OrdemServico

# Cria as tabelas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Torotech Status", version="0.1.0")

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Status permitidos
STATUS_PERMITIDOS = [
    "Em diagnóstico",
    "Aguardando peça",
    "Em reparo",
    "Pronto para retirada"
]


@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
async def login(
    request: Request,
    login: str = Form(...),
    senha: str = Form(...),
    db: Session = Depends(get_db)
):
    # Autenticação simplificada para MVP (em produção usar hash)
    usuario = db.query(Usuario).filter(Usuario.login == login).first()
    
    if not usuario:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "erro": "Login ou senha incorretos. Verifique e tente novamente."}
        )
    
    # TODO: Validar senha com bcrypt
    response = RedirectResponse(url="/ordens", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="usuario_id", value=str(usuario.id))
    response.set_cookie(key="usuario_nome", value=usuario.nome)
    response.set_cookie(key="usuario_tipo", value=usuario.tipo)
    return response


@app.get("/ordens", response_class=HTMLResponse)
async def listar_ordens(request: Request, db: Session = Depends(get_db)):
    usuario_id = request.cookies.get("usuario_id")
    if not usuario_id:
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    
    busca = request.query_params.get("q", "").strip()
    query = db.query(OrdemServico)
    if busca:
        query = query.filter(
            (OrdemServico.numero_os.contains(busca)) |
            (OrdemServico.identificador_aparelho.contains(busca)) |
            (OrdemServico.nome_cliente.contains(busca))
        )
    ordens = query.order_by(OrdemServico.data_ultima_atualizacao.desc()).all()
    return templates.TemplateResponse(
        "lista_ordens.html",
        {
            "request": request,
            "ordens": ordens,
            "usuario_nome": request.cookies.get("usuario_nome"),
            "usuario_tipo": request.cookies.get("usuario_tipo"),
            "mensagem": request.query_params.get("mensagem")
        }
    )


@app.get("/ordens/{numero_os}", response_class=HTMLResponse)
async def detalhe_ordem(request: Request, numero_os: str, db: Session = Depends(get_db)):
    usuario_id = request.cookies.get("usuario_id")
    if not usuario_id:
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    
    ordem = db.query(OrdemServico).filter(OrdemServico.numero_os == numero_os).first()
    if not ordem:
        return RedirectResponse(url="/ordens?mensagem=Ordem não encontrada", status_code=status.HTTP_303_SEE_OTHER)
    
    return templates.TemplateResponse(
        "detalhe_ordem.html",
        {
            "request": request,
            "ordem": ordem,
            "status_permitidos": STATUS_PERMITIDOS,
            "usuario_nome": request.cookies.get("usuario_nome"),
            "usuario_tipo": request.cookies.get("usuario_tipo")
        }
    )


@app.post("/ordens/{numero_os}/status")
async def atualizar_status(
    request: Request,
    numero_os: str,
    novo_status: str = Form(...),
    db: Session = Depends(get_db)
):
    usuario_id = request.cookies.get("usuario_id")
    if not usuario_id:
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    
    if novo_status not in STATUS_PERMITIDOS:
        return RedirectResponse(
            url=f"/ordens/{numero_os}?erro=Status inválido",
            status_code=status.HTTP_303_SEE_OTHER
        )
    
    ordem = db.query(OrdemServico).filter(OrdemServico.numero_os == numero_os).first()
    if not ordem:
        return RedirectResponse(url="/ordens?mensagem=Ordem não encontrada", status_code=status.HTTP_303_SEE_OTHER)
    
    ordem.status_atual = novo_status
    ordem.data_ultima_atualizacao = datetime.utcnow()
    ordem.usuario_id = int(usuario_id)
    db.commit()
    
    return RedirectResponse(
        url="/ordens?mensagem=Status atualizado com sucesso.",
        status_code=status.HTTP_303_SEE_OTHER
    )


@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie("usuario_id")
    response.delete_cookie("usuario_nome")
    response.delete_cookie("usuario_tipo")
    return response
