# API de livros

from fastapi import FastAPI, HTTPException

app = FastAPI()

biblioteca = {}

@app.get("/livros")
def get_livros():
    if not biblioteca:
        return {"message": "Nenhum livro encontrado"}
    else:
        return {"livros": biblioteca}
    

@app.post("/adiciona")
def post_livros(id_livro: int, nome_livro: str, autor_livro: str, ano_livro: int):
    if id_livro in biblioteca:
        raise HTTPException(status_code=400, detail="Esse livro já existe")
    else:
        biblioteca[id_livro] = {
            "nome": nome_livro,
            "autor": autor_livro,
            "ano": ano_livro
        }
        return {"message": "Livro adicionado com sucesso!"}
    
@app.put("/atualiza/{id_livro}")
def put_livros (id_livro: int, nome_livro: str, autor_livro: str, ano_livro: int):
    meu_livro = biblioteca.get(id_livro)
    if id_livro not in biblioteca:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    else:
        if nome_livro:
            meu_livro["nome_livro"] = nome_livro
        if autor_livro:
            meu_livro["autor_livro"] = autor_livro
        if ano_livro:
            meu_livro["ano_livro"] = ano_livro

        return {"message": "Livro atualizado com sucesso!"}
    

@app.delete("/deleta/{id_livro}")
def delete_livros(id_livro: int):
    if id_livro not in biblioteca:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    else:
        del biblioteca[id_livro]
        return {"message": "Livro deletado com sucesso!"}