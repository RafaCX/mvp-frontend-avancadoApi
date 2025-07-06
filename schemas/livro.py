from pydantic import BaseModel
from typing import List, Optional
from model import Livro

class LivroSchema(BaseModel):
    """Define como um novo livro deve ser representado"""
    titulo: str = "O Pequeno Príncipe"
    autor: str = "Antoine de Saint-Exupéry"
    editora: Optional[str] = "Agir"
    genero: Optional[str] = "Ficção"
    ano_publicacao: Optional[int] = 1943
    sinopse: Optional[str] = "Uma história sobre a amizade e a importância dos valores humanos."

class LivroBuscaSchema(BaseModel):
    """Define como deve ser a estrutura que representa a busca por um livro"""
    titulo: str = "O Pequeno Príncipe"

class LivroViewSchema(BaseModel):
    """Define como um livro será retornado"""
    id: int = 1
    titulo: str = "O Pequeno Príncipe"
    autor: str = "Antoine de Saint-Exupéry"
    editora: str = "Agir"
    genero: str = "Ficção"
    ano_publicacao: int = 1943
    sinopse: str = "Uma história sobre a amizade e a importância dos valores humanos."
    data_insercao: str = "01/01/2024 10:00:00"

class ListaLivrosSchema(BaseModel):
    """Define como uma lista de livros será retornada"""
    livros: List[LivroViewSchema]

class LivroDelSchema(BaseModel):
    """Define como deve ser a estrutura do dado retornado após uma requisição de remoção"""
    message: str
    titulo: str

class LivroExternoSchema(BaseModel):
    """Define como um livro da API externa será representado"""
    titulo: str
    autor: str
    editora: str
    ano_publicacao: str
    sinopse: str

class ListaLivrosExternosSchema(BaseModel):
    """Define como uma lista de livros externos será retornada"""
    livros: List[LivroExternoSchema]

def apresenta_livro(livro: Livro):
    """Retorna representação do livro seguindo o schema definido em LivroViewSchema"""
    return {
        "id": livro.id,
        "titulo": livro.titulo,
        "autor": livro.autor,
        "editora": livro.editora,
        "genero": livro.genero,
        "ano_publicacao": livro.ano_publicacao,
        "sinopse": livro.sinopse,
        "data_insercao": livro.data_insercao
    }

def apresenta_livros(livros: List[Livro]):
    """Retorna representação da lista de livros seguindo o schema definido em ListaLivrosSchema"""
    result = []
    for livro in livros:
        result.append({
            "id": livro.id,
            "titulo": livro.titulo,
            "autor": livro.autor,
            "editora": livro.editora,
            "genero": livro.genero,
            "ano_publicacao": livro.ano_publicacao,
            "sinopse": livro.sinopse,
            "data_insercao": livro.data_insercao
        })
    
    return {"livros": result}