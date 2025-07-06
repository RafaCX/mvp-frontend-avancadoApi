from sqlalchemy.exc import IntegrityError
from flask_openapi3 import Info, Tag
from flask_openapi3 import OpenAPI
from flask_cors import CORS
from flask import redirect, jsonify
from model import Session, Livro
from logger import logger
from schemas.livro import *
from schemas.error import *
import requests

info = Info(title="API de Livros - MVP", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# Tags para organização da documentação
livro_tag = Tag(name="Livro", description="Operações relacionadas a livros")
externo_tag = Tag(name="API Externa", description="Busca de dados em APIs externas")

@app.get('/')
def home():
    """Redireciona para a documentação da API."""
    return redirect('/openapi')

@app.post('/livro', tags=[livro_tag],
          responses={"200": LivroViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_livro(form: LivroSchema):
    """Adiciona um novo Livro à base de dados."""
    livro = Livro(
        titulo=form.titulo,
        autor=form.autor,
        editora=form.editora,
        genero=form.genero,
        ano_publicacao=form.ano_publicacao,
        sinopse=form.sinopse
    )

    logger.debug(f"Adicionando livro: {livro.titulo}")
    session = Session()
    try:
        session.add(livro)
        session.commit()
        logger.info(f"Livro '{livro.titulo}' adicionado com sucesso.")
        return apresenta_livro(livro), 200
    except IntegrityError:
        error_msg = "Livro com esse título já existe na base."
        logger.warning(error_msg)
        return {"message": error_msg}, 409
    except Exception as e:
        error_msg = "Erro ao adicionar livro."
        logger.error(f"{error_msg} {e}")
        return {"message": error_msg}, 400
    finally:
        session.close()

@app.get('/livro', tags=[livro_tag],
         responses={"200": LivroViewSchema, "404": ErrorSchema})
def get_livro(query: LivroBuscaSchema):
    """Busca um livro pelo título."""
    session = Session()
    try:
        livro = session.query(Livro).filter(Livro.titulo.ilike(f"%{query.titulo}%")).first()

        if not livro:
            error_msg = "Livro não encontrado na base."
            logger.warning(error_msg)
            return {"message": error_msg}, 404
        else:
            logger.info(f"Livro encontrado: {livro.titulo}")
            return apresenta_livro(livro), 200
    finally:
        session.close()

@app.get('/livros', tags=[livro_tag],
         responses={"200": ListaLivrosSchema, "404": ErrorSchema})
def get_livros():
    """Lista todos os livros cadastrados."""
    session = Session()
    try:
        livros = session.query(Livro).all()

        if not livros:
            error_msg = "Nenhum livro encontrado."
            logger.warning(error_msg)
            return {"message": error_msg}, 404
        else:
            logger.info(f"{len(livros)} livros encontrados.")
            return apresenta_livros(livros), 200
    finally:
        session.close()

@app.delete('/livro', tags=[livro_tag],
            responses={"200": LivroDelSchema, "404": ErrorSchema})
def del_livro(query: LivroBuscaSchema):
    """Deleta um livro pelo título."""
    session = Session()
    try:
        livro = session.query(Livro).filter(Livro.titulo == query.titulo).first()

        if not livro:
            error_msg = "Livro não encontrado para remoção."
            logger.warning(error_msg)
            return {"message": error_msg}, 404

        titulo_removido = livro.titulo
        session.delete(livro)
        session.commit()
        logger.info(f"Livro deletado: {titulo_removido}")
        return {"message": "Livro removido com sucesso", "titulo": titulo_removido}
    finally:
        session.close()

@app.get('/externo/livros', tags=[externo_tag],
         responses={"200": ListaLivrosExternosSchema, "404": ErrorSchema, "500": ErrorSchema})
def buscar_livros_externos(query: LivroBuscaSchema):
    """Busca livros na API pública do Google Books"""
    termo = query.titulo
    url = f"https://www.googleapis.com/books/v1/volumes?q={termo}"

    try:
        response = requests.get(url)
        data = response.json()

        if "items" not in data:
            return {"message": "Nenhum resultado encontrado na API externa."}, 404

        resultados = []
        for item in data["items"][:5]:  # Limita a 5 resultados
            volume = item["volumeInfo"]
            livro_externo = {
                "titulo": volume.get("title", "Sem título"),
                "autor": ", ".join(volume.get("authors", ["Desconhecido"])),
                "editora": volume.get("publisher", "Desconhecida"),
                "ano_publicacao": str(volume.get("publishedDate", "Desconhecido"))[:4] if volume.get("publishedDate") else "Desconhecido",
                "sinopse": volume.get("description", "Sem sinopse")[:500] if volume.get("description") else "Sem sinopse"  # Limita o tamanho da sinopse
            }
            resultados.append(livro_externo)

        return {"livros": resultados}, 200

    except Exception as e:
        logger.error(f"Erro ao consultar API externa: {e}")
        return {"message": "Erro ao buscar dados da API externa."}, 500

if __name__ == '__main__':
    app.run(debug=True)