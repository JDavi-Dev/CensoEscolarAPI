from sqlalchemy.orm import Mapped, mapped_column, relationship

from helpers.database import db

from flask_restful import fields

uf_fields = {
    'cod_uf': fields.Integer,
    'sigla': fields.String,
    'nome': fields.String,
    'regiao': fields.String
}

class UF(db.Model):
    __tablename__ = "tb_uf"
    
    cod_uf: Mapped[int] = mapped_column(primary_key=True)
    sigla: Mapped[str] = mapped_column()
    nome: Mapped[str] = mapped_column()
    regiao: Mapped[str] = mapped_column()

    mesorregioes = relationship('Mesorregiao', back_populates='uf')
    microrregioes = relationship('Microrregiao', back_populates='uf')
    municipios = relationship('Municipio', back_populates='uf')
    instituicoes = relationship('Instituicao', back_populates='uf')
    censo_escolares = relationship('CensoEscolar', back_populates='uf')

    def __init__(self, cod_uf: int, sigla: str, nome: str, regiao: str):
        self.cod_uf = cod_uf
        self.sigla = sigla
        self.nome = nome
        self.regiao = regiao

    def __repr__(self):
        return f"<UF(cod_uf={self.cod_uf}, sigla='{self.sigla}', nome='{self.nome}', regiao='{self.regiao}')>"

    def __str__(self):
        return f"{self.nome} ({self.sigla}) - {self.regiao}"