from helpers.database import db

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from flask_restful import fields

censo_fields = {
    'ano_censo': fields.Integer,
    'estado': fields.String,
    'sigla': fields.String,
    'cod_estado': fields.Integer,
    'total_matriculas': fields.Integer
}

class CensoEscolar(db.Model):
    __tablename__ = "censo_escolar"

    ano_censo: Mapped[int] = mapped_column(primary_key=True)
    estado: Mapped[str] = mapped_column()
    sigla: Mapped[str] = mapped_column()
    cod_estado: Mapped[int] = mapped_column(ForeignKey('tb_uf.cod_uf'), primary_key=True)
    total_matriculas: Mapped[int] = mapped_column()

    uf = relationship('UF', back_populates='censo_escolares')

    def __init__(self, ano_censo: int, estado: str, sigla: str, cod_estado: int, total_matriculas: int):
        self.ano_censo = ano_censo
        self.estado = estado
        self.sigla = sigla
        self.cod_estado = cod_estado
        self.total_matriculas = total_matriculas
    
    def __repr__(self):
        return f"<CensoEscolar(ano_censo={self.ano_censo}, estado='{self.estado}', sigla='{self.sigla}', cod_estado={self.cod_estado}, total_matriculas={self.total_matriculas})>"

    def __str__(self):
        return f"Censo Escolar {self.ano_censo} - {self.estado}: {self.total_matriculas} matrículas"