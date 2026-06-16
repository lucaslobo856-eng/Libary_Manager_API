# API de livros

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(
    title="API de livros",
    description="API para gerenciar uma biblioteca de livros",
    version="1.0.0",
    contact={
        "name": "Lucas Ormond Lobo",
        "email": "lucasormonddev@gmail.com"
    }
)

biblioteca = {}

class Livro(BaseModel):
    nome_livro: str
    autor_livro: str
    ano_livro: int


@app.get("/livros")
def get_livros():
    if not biblioteca:
        return {"message": "Nenhum livro encontrado"}
    else:
        return {"livros": biblioteca}
    

@app.post("/adiciona")
def post_livros(id_livro: int, livro: Livro):
    if id_livro in biblioteca:
        raise HTTPException(status_code=400, detail="Esse livro já existe")
    else:
        biblioteca[id_livro] = livro.dict()
        return {"message": "Livro adicionado com sucesso!"}
    
@app.put("/atualiza/{id_livro}")
def put_livros (id_livro: int, livro: Livro):
    meu_livro = biblioteca.get(id_livro)
    if id_livro not in biblioteca:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    else:
        biblioteca[id_livro] = livro.dict()

        return {"message": "Livro atualizado com sucesso!"}
    

@app.delete("/deleta/{id_livro}")
def delete_livros(id_livro: int):
    if id_livro not in biblioteca:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    else:
        del biblioteca[id_livro]
        return {"message": "Livro deletado com sucesso!"}