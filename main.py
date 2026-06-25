import os
import secrets
from typing import Optional
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel

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
def get_livros(
    page: int = 1, 
    size: int = 10,  
    sort_by: str = "id",
    credentials: HTTPBasicCredentials = Depends(autenticar_usuario)
):
    if page < 1 or size < 1:
        raise HTTPException(status_code=400, detail="Page e size com valores inválidos.")
    if not biblioteca:
        raise HTTPException(status_code=404, detail="Nenhum livro cadastrado no momento.")
    
    campos_validos = ["id", "nome_livro", "autor_livro", "ano_livro"]
    if sort_by not in campos_validos:
        raise HTTPException(
            status_code=400, 
            detail=f"Campo de ordenação inválido. Escolha entre: {', '.join(campos_validos)}"
        )

    if sort_by == "id":
        livros_ordenados = sorted(biblioteca.items(), key=lambda x: x[0])
    else:
        livros_ordenados = sorted(biblioteca.items(), key=lambda x: x[1][sort_by])
    

    start = (page - 1) * size
    end = start + size

    paginas_livros = [
        {
            "id": id_livro, 
            "nome_livro": livro_data["nome_livro"], 
            "autor_livro": livro_data["autor_livro"], 
            "ano_livro": livro_data["ano_livro"]
        }
        for id_livro, livro_data in livros_ordenados[start:end]
    ]

    return {
        "page": page, 
        "size": size, 
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
def put_livros(id_livro: int, livro: Livro, credentials: HTTPBasicCredentials = Depends(autenticar_usuario)):
    if id_livro not in biblioteca:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    else:
        biblioteca[id_livro] = livro.dict()
        return {"message": "Livro updated com sucesso!"}
    

@app.delete("/deleta/{id_livro}")
def delete_livros(id_livro: int, credentials: HTTPBasicCredentials = Depends(autenticar_usuario)):
    if id_livro not in biblioteca:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    else:
        del biblioteca[id_livro]
        return {"message": "Livro deletado com sucesso!"}