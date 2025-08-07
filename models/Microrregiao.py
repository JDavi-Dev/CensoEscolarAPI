from helpers.database import db

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from flask_restful import fields

microrregiao_fields = {
    'cod_microrregiao': fields.Integer,
    'nome': fields.String,
    'cod_mesorregiao': fields.Integer,
    'cod_uf': fields.Integer
}

class Microrregiao(db.Model):
    __tablename__ = "tb_microrregiao"

    cod_microrregiao: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column()
    cod_mesorregiao: Mapped[int] = mapped_column(ForeignKey('tb_mesorregiao.cod_mesorregiao'))
    cod_uf: Mapped[int] = mapped_column(ForeignKey('tb_uf.cod_uf'))

    mesorregioes = relationship('Mesorregiao', back_populates='microrregioes')
    uf = relationship('UF', back_populates='microrregioes')
    municipios = relationship('Municipio', back_populates='microrregioes')

    __table_args__ = (
        UniqueConstraint('nome', 'cod_uf'),
    )

    def __init__(self, cod_microrregiao: int, nome: str, cod_mesorregiao: int, cod_uf: int):
        self.cod_microrregiao = cod_microrregiao
        self.nome = nome
        self.cod_mesorregiao = cod_mesorregiao
        self.cod_uf = cod_uf

    def __repr__(self):
        return f"<Microrregiao(cod_microrregiao={self.cod_microrregiao}, nome='{self.nome}', cod_mesorregiao={self.cod_mesorregiao}, cod_uf={self.cod_uf})>"

    def __str__(self):
        return f"{self.nome} (Mesorregião: {self.cod_mesorregiao})"