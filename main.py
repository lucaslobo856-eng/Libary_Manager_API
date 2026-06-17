# API de livros

import secrets

from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from typing import Optional
import secrets 
import os

app = FastAPI(
    title="API de livros",
    description="API para gerenciar uma biblioteca de livros",
    version="1.0.0",
    contact={
        "name": "Lucas Ormond Lobo",
        "email": "lucasormonddev@gmail.com"
    }
)

usuario = "lucas"
senha = "123456"

security = HTTPBasic()

biblioteca = {}

class Livro(BaseModel):
    nome_livro: str
    autor_livro: str
    ano_livro: int

def autenticar_usuario(credentials: HTTPBasicCredentials = Depends(security)):
    is_username_correct = secrets.compare_digest(credentials.username, usuario)
    is_password_correct = secrets.compare_digest(credentials.password, senha)

    if not (is_username_correct and is_password_correct):
        raise HTTPException(
            status_code=401,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Basic"},
        )


@app.get("/livros")
def get_livros(page : int = 1, limit: int = 10, credentials: HTTPBasicCredentials = Depends(autenticar_usuario)):
    if page < 1 or limit < 1:
        raise HTTPException(status_code=400, detail="Page e limit com valores inválidos.")
    if not biblioteca:
        raise HTTPException(status_code=404, detail="Nenhum livro cadastrado no momento.")
    
    livros_ordenados = sorted(biblioteca.items(), key=lambda x: x[0])
    
    start = (page - 1) * limit
    end = start + limit

    paginas_livros = [
        {"id": id_livro, "nome_livro": livro_data["nome_livro"], "autor_livro": livro_data["autor_livro"], "ano_livro": livro_data["ano_livro"]}
        for id_livro, livro_data in livros_ordenados[start:end]
    ]

    return {
        "page": page, 
            "limit": limit, 
            "total": len(biblioteca), 
            "livros": paginas_livros
        }

@app.post("/adiciona")
def post_livros(id_livro: int, livro: Livro, credentials: HTTPBasicCredentials = Depends(autenticar_usuario)):
    if id_livro in biblioteca:
        raise HTTPException(status_code=400, detail="Esse livro já existe")
    else:
        biblioteca[id_livro] = livro.dict()
        return {"message": "Livro adicionado com sucesso!"}
    
@app.put("/atualiza/{id_livro}")
def put_livros (id_livro: int, livro: Livro, credentials: HTTPBasicCredentials = Depends(autenticar_usuario)):
    meu_livro = biblioteca.get(id_livro)
    if id_livro not in biblioteca:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    else:
        biblioteca[id_livro] = livro.dict()

        return {"message": "Livro atualizado com sucesso!"}
    

@app.delete("/deleta/{id_livro}")
def delete_livros(id_livro: int, credentials: HTTPBasicCredentials = Depends(autenticar_usuario)):
    if id_livro not in biblioteca:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    else:
        del biblioteca[id_livro]
        return {"message": "Livro deletado com sucesso!"}