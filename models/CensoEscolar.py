from flask_restful import fields

censo_fields = {
    'ano_censo': fields.Integer,
    'estado': fields.String,
    'sigla': fields.String,
    'cod_estado': fields.Integer,
    'total_matriculas': fields.Integer
}

class CensoEscolar:
    def __init__(self, ano_censo, estado, sigla, cod_estado, total_matriculas):
        self.ano_censo = ano_censo
        self.estado = estado
        self.sigla = sigla
        self.cod_estado = cod_estado
        self.total_matriculas = total_matriculas