from helpers.database import db

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from flask_restful import fields

mesorregiao_fields = {
    'cod_mesorregiao': fields.Integer,
    'nome': fields.String,
    'cod_uf': fields.Integer
}

class Mesorregiao(db.Model):
    __tablename__ = "tb_mesorregiao"

    cod_mesorregiao: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column()
    cod_uf: Mapped[int] = mapped_column(ForeignKey('tb_uf.cod_uf'))

    __table_args__ = (
        UniqueConstraint('nome', 'cod_uf'),
    )

    uf = relationship('UF', back_populates='mesorregioes')
    microrregioes = relationship('Microrregiao', back_populates='mesorregioes')
    municipios = relationship('Municipio', back_populates='mesorregioes')

    def __init__(self, cod_mesorregiao: int, nome: str, cod_uf: int):
        self.cod_mesorregiao = cod_mesorregiao
        self.nome = nome
        self.cod_uf = cod_uf

    def __repr__(self):
        return f"<Mesorregiao(cod_mesorregiao={self.cod_mesorregiao}, nome='{self.nome}', cod_uf={self.cod_uf})>"

    def __str__(self):
        return f"{self.nome} (UF: {self.cod_uf})"