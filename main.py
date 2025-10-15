from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel, Field
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import os

# Importando as camadas de aplicação e infraestrutura
from application.use_cases.cadastrar_colheita import CadastrarColheita
from application.use_cases.listar_colheitas import ListarColheitas
from application.use_cases.gerar_relatorio import GerarRelatorioTXT
from infra.repositories.sqlite_colheita_repository import SQLiteColheitaRepository
from infra.database.database import init_db
from application.interfaces.colheita_repository import ColheitaRepository

# --- Inicialização da Aplicação e Infraestrutura ---
init_db()

app = FastAPI(
    title="AgroLoss Manager API",
    description="API para gestão de perdas na colheita de cana-de-açúcar.",
    version="1.0.0"
)

# --- CONFIGURAÇÃO DO CORS ---
origins = [
    "http://localhost", "http://localhost:8000",
    "http://127.0.0.1", "http://127.0.0.1:8000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

# --- CONFIGURAÇÃO DO FRONT-END ---
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# --- Injeção de Dependência ---
def get_colheita_repo() -> ColheitaRepository:
    return SQLiteColheitaRepository()

# --- Modelos de Dados da API (Pydantic) ---
class ColheitaBase(BaseModel):
    id_talhao: str = Field(..., example="T-015")
    maquina: str = Field(..., example="Colheitadeira XYZ-2000")
    operador: str = Field(..., example="João Silva")
    toneladas_potenciais: float = Field(..., gt=0, example=150.5)
    toneladas_colhidas: float = Field(..., gt=0, example=140.0)

class ColheitaCreate(ColheitaBase):
    pass

class ColheitaRead(ColheitaBase):
    id: int
    class Config:
        from_attributes = True

# --- ENDPOINT PARA SERVIR O FRONT-END ---
@app.get("/", response_class=HTMLResponse, tags=["Front-end"])
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# --- ENDPOINTS DA API ---
@app.post("/api/colheitas", response_model=ColheitaRead, status_code=201, tags=["API - Colheitas"])
def criar_colheita(colheita_data: ColheitaCreate, repo: ColheitaRepository = Depends(get_colheita_repo)):
    cadastrar_uc = CadastrarColheita(repository=repo)
    return cadastrar_uc.execute(colheita_data.dict())

@app.get("/api/colheitas", response_model=List[ColheitaRead], tags=["API - Colheitas"])
def listar_todas_as_colheitas(repo: ColheitaRepository = Depends(get_colheita_repo)):
    listar_uc = ListarColheitas(repository=repo)
    return listar_uc.execute()

# << INÍCIO DA ALTERAÇÃO >>
@app.post("/api/colheitas/gerar-relatorio", response_class=FileResponse, tags=["API - Relatórios"])
def gerar_relatorio(repo: ColheitaRepository = Depends(get_colheita_repo)):
    """
    Gera um arquivo de texto com o relatório de perdas e o retorna para download.
    """
    listar_uc = ListarColheitas(repository=repo)
    todos_os_registros = listar_uc.execute()
    if not todos_os_registros:
        raise HTTPException(status_code=404, detail="Nenhum registro encontrado para gerar relatório.")

    gerar_relatorio_uc = GerarRelatorioTXT()
    # O método execute() já salva o arquivo 'relatorio_perdas.txt'
    gerar_relatorio_uc.execute(todos_os_registros)

    caminho_arquivo = "relatorio_perdas.txt"

    # Verifica se o arquivo foi criado antes de tentar enviá-lo
    if not os.path.exists(caminho_arquivo):
        raise HTTPException(status_code=500, detail="Erro ao gerar o arquivo de relatório.")

    # Retorna o arquivo como uma resposta para download
    return FileResponse(
        path=caminho_arquivo,
        filename=caminho_arquivo,
        media_type='text/plain'
    )