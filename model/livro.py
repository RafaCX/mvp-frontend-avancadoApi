from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime
from typing import Union
from model import Base

class Livro(Base):
    __tablename__ = 'livro'

    id = Column("pk_livro", Integer, primary_key=True)
    titulo = Column(String(200), unique=True)
    autor = Column(String(140))
    editora = Column(String(140))
    genero = Column(String(100))
    ano_publicacao = Column(Integer)
    sinopse = Column(String(4000))
    data_insercao = Column(DateTime, default=datetime.now())

    def __init__(self, titulo: str, autor: str, editora: str,
                 genero: str, ano_publicacao: int, sinopse: str,
                 data_insercao: Union[datetime, None] = None):
        """
        Cria um Livro

        Arguments:
            titulo: título da obra
            autor: autor do livro
            editora: editora do livro
            genero: gênero literário
            ano_publicacao: ano de publicação
            sinopse: breve descrição da obra
            data_insercao: data de inserção na base
        """
        self.titulo = titulo
        self.autor = autor
        self.editora = editora
        self.genero = genero
        self.ano_publicacao = ano_publicacao
        self.sinopse = sinopse
        if data_insercao:
            self.data_insercao = data_insercao
