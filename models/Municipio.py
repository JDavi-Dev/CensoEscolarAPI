from helpers.database import db

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from flask_restful import fields

municipio_fields = {
    'cod_municipio': fields.Integer,
    'nome': fields.String,
    'cod_microrregiao': fields.Integer,
    'cod_mesorregiao': fields.Integer,
    'cod_uf': fields.Integer
}

class Municipio(db.Model):
    __tablename__ = "tb_municipio"

    cod_municipio: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column()
    cod_microrregiao: Mapped[int] = mapped_column(ForeignKey('tb_microrregiao.cod_microrregiao'))
    cod_mesorregiao: Mapped[int] = mapped_column(ForeignKey('tb_mesorregiao.cod_mesorregiao'))
    cod_uf: Mapped[int] = mapped_column(ForeignKey('tb_uf.cod_uf'))

    microrregioes = relationship('Microrregiao', back_populates='municipios')
    mesorregioes = relationship('Mesorregiao', back_populates='municipios')
    uf = relationship('UF', back_populates='municipios')
    instituicoes = relationship('Instituicao', back_populates='municipios')

    def __init__(self, cod_municipio: int, nome: str, cod_microrregiao: int, cod_mesorregiao: int, cod_uf: int):
        self.cod_municipio = cod_municipio
        self.nome = nome
        self.cod_microrregiao = cod_microrregiao
        self.cod_mesorregiao = cod_mesorregiao
        self.cod_uf = cod_uf

    def __repr__(self):
        return f"<Municipio(cod_municipio={self.cod_municipio}, nome='{self.nome}', cod_uf={self.cod_uf})>"

    def __str__(self):
        return f"{self.nome} (UF: {self.cod_uf})"