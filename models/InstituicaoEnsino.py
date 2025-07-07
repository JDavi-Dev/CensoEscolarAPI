from marshmallow import Schema, fields, validate, ValidationError
from flask_restful import fields as flaskFields

from datetime import datetime

instiuicao_fields = {
    'ano_censo': flaskFields.Integer,
    'regiao': flaskFields.String,
    'cod_regiao': flaskFields.Integer,
    'estado': flaskFields.String,
    'sigla': flaskFields.String,
    'cod_estado': flaskFields.Integer,
    'municipio': flaskFields.String,
    'cod_municipio': flaskFields.Integer,
    'mesorregiao': flaskFields.String,
    'microrregiao': flaskFields.String,
    'entidade': flaskFields.String,
    'cod_entidade': flaskFields.Integer,
    'qt_mat_bas': flaskFields.Integer
}


class InstituicaoEnsino:
    def __init__(self, ano_censo, regiao, cod_regiao, estado, sigla, cod_estado,
                 municipio, cod_municipio, mesorregiao,
                 microrregiao, entidade, cod_entidade, qt_mat_bas):
        self.ano_censo = ano_censo
        self.regiao = regiao
        self.cod_regiao = cod_regiao
        self.estado = estado
        self.sigla = sigla
        self.cod_estado = cod_estado
        self.municipio = municipio
        self.cod_municipio = cod_municipio
        self.mesorregiao = mesorregiao
        self.microrregiao = microrregiao
        self.entidade = entidade
        self.cod_entidade = cod_entidade
        self.qt_mat_bas = qt_mat_bas


class InstituicaoEnsinoSchema(Schema):
    ano_censo = fields.Int(
        required=True,
        validate=validate.Range(min=1995, max=datetime.now(
        ).year - 1, error=f"O ano deve estar entre 1995 e {datetime.now().year - 1}."),
        error_messages={
            "required": "O ano do censo é obrigatório.",
            "null": "O ano do censo não pode ser nulo."
        }
    )
    regiao = fields.Str(
        required=True,
        validate=validate.Length(min=3, max=20),
        error_messages={
            "required": "Nome da Região é obrigatório.",
            "null": "Nome da Região não pode ser nulo.",
            "validator_failed": "O nome da Região deve ter entre 3 e 20 caracteres."
        }
    )
    cod_regiao = fields.Int(
        required=True,
        validate=validate.Range(
            min=1, max=5, error="O codigo de região deve estar entre 1 e 5"),
        error_messages={
            "required": "Código da Região é obrigatório.",
            "null": "Código da Região não pode ser nulo."
        }
    )
    estado = fields.Str(
        required=True,
        validate=validate.Length(min=4, max=50),
        error_messages={
            "required": "Estado é obrigatório.",
            "null": "Estado não pode ser nulo.",
            "validator_failed": "O Estado deve ter entre 4 e 50 caracteres."
        }
    )
    sigla = fields.Str(
        required=True,
        validate=validate.Length(min=2, max=2),
        error_messages={
            "required": "Sigla é obrigatória.",
            "null": "Sigla não pode ser nula.",
            "validator_failed": "A Sigla deve ter exatamente 2 caracteres."
        }
    )
    UFS_VALIDAS = [11, 12, 13, 14, 15, 16, 17, 21, 22, 23, 24,
                   25, 26, 27, 28, 29, 31, 32, 33, 35, 41, 42, 43, 50, 51, 52, 53]
    cod_estado = fields.Int(
        required=True,
        validate=validate.OneOf(UFS_VALIDAS, error=f"Código de estado inválido. Valores aceitos: {UFS_VALIDAS}"),
        error_messages={
            "required": "Código do Estado é obrigatório.",
            "null": "Código do Estado não pode ser nulo."
        }
    )
    municipio = fields.Str(
        required=True,
        validate=validate.Length(min=3, max=150),
        error_messages={
            "required": "Município é obrigatório.",
            "null": "Município não pode ser nulo.",
            "validator_failed": "O Município deve ter entre 3 e 150 caracteres."
        }
    )
    def tamanho_cod_municipio(value):
        if len(str(value)) != 7:
            raise ValidationError("O código do município deve ter 7 dígitos.")
    cod_municipio = fields.Int(
        required=True,
        validate=tamanho_cod_municipio,
        error_messages={
            "required": "Código do Município é obrigatório.",
            "null": "Código do Município não pode ser nulo."
        }
    )
    mesorregiao = fields.Str(
        required=True,
        validate=validate.Length(min=4, max=100),
        error_messages={
            "required": "Mesorregião é obrigatória.",
            "null": "Mesorregião não pode ser nula.",
            "validator_failed": "A Mesorregião deve ter entre 3 e 100 caracteres."
        }
    )
    microrregiao = fields.Str(
        required=True,
        validate=validate.Length(min=4, max=100),
        error_messages={
            "required": "Microrregião é obrigatória.",
            "null": "Microrregião não pode ser nula.",
            "validator_failed": "A Microrregião deve ter entre 3 e 100 caracteres."
        }
    )
    entidade = fields.Str(
        required=True,
        validate=validate.Length(min=3, max=100),
        error_messages={
            "required": "Entidade é obrigatória.",
            "null": "Entidade não pode ser nula.",
            "validator_failed": "A Entidade deve ter entre 3 e 100 caracteres."
        }
    )
    qt_mat_bas = fields.Int(
        required=True,
        validate=validate.Range(min=1, error="O valor deve ser um número inteiro positivo."),
        error_messages={
            "required": "Quantidade de Matriculados é obrigatória.",
            "null": "Quantidade de Matriculados não pode ser nula."
        }
    )
