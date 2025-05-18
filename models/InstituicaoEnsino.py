from marshmallow import Schema, fields, validate, ValidationError

class InstituicaoEnsino:
    def __init__(self, id_instituicao, regiao, cod_regiao, estado, sigla, cod_estado,
                 municipio, cod_municipio, mesorregiao, cod_mesorregiao,
                 microrregiao, cod_microrregiao, entidade, cod_entidade, qt_mat_bas):
        self.id_instituicao = id_instituicao
        self.regiao = regiao
        self.cod_regiao = cod_regiao
        self.estado = estado
        self.sigla = sigla
        self.cod_estado = cod_estado
        self.municipio = municipio
        self.cod_municipio = cod_municipio
        self.mesorregiao = mesorregiao
        self.cod_mesorregiao = cod_mesorregiao
        self.microrregiao = microrregiao
        self.cod_microrregiao = cod_microrregiao
        self.entidade = entidade
        self.cod_entidade = cod_entidade
        self.qt_mat_bas = qt_mat_bas

    def toDict(self):
        return {
            'id_instituicao': self.id_instituicao,
            'regiao': self.regiao,
            'cod_regiao': self.cod_regiao,
            'estado': self.estado,
            'sigla': self.sigla,
            'cod_estado': self.cod_estado,
            'municipio': self.municipio,
            'cod_municipio': self.cod_municipio,
            'mesorregiao': self.mesorregiao,
            'cod_mesorregiao': self.cod_mesorregiao,
            'microrregiao': self.microrregiao,
            'cod_microrregiao': self.cod_microrregiao,
            'entidade': self.entidade,
            'cod_entidade': self.cod_entidade,
            'qt_mat_bas': self.qt_mat_bas
        }

class InstituicaoEnsinoSchema(Schema):
    def validate_positive(value):
        if value <= 0:
            raise ValidationError("O valor deve ser um número inteiro positivo.")
    
    id_instituicao = fields.Int()
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
        validate=validate_positive,
        error_messages={
            "required": "Código da Região é obrigatório.",
            "null": "Código da Região não pode ser nulo."
        }
    )
    estado = fields.Str(
        required=True, 
        validate=validate.Length(min=5, max=50),
        error_messages={
            "required": "Estado é obrigatório.",
            "null": "Estado não pode ser nulo.",
            "validator_failed": "O Estado deve ter entre 5 e 50 caracteres."
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
    cod_estado = fields.Int(
        required=True,
        validate=validate_positive,
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
    cod_municipio = fields.Int(
        required=True,
        validate=validate_positive,
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
    cod_mesorregiao = fields.Int(
        required=True,
        validate=validate_positive,
        error_messages={
            "required": "Código da Mesorregião é obrigatório.",
            "null": "Código da Mesorregião não pode ser nulo."
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
    cod_microrregiao = fields.Int(
        required=True,
        validate=validate_positive,
        error_messages={
            "required": "Código da Microrregião é obrigatório.",
            "null": "Código da Microrregião não pode ser nulo."
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
    cod_entidade = fields.Int(
        required=True,
        validate=validate_positive,
        error_messages={
            "required": "Código da Entidade é obrigatório.",
            "null": "Código da Entidade não pode ser nulo."
        }
    )
    qt_mat_bas = fields.Int(
        required=True,
        validate=validate_positive,
        error_messages={
            "required": "Quantidade de Matriculados é obrigatória.",
            "null": "Quantidade de Matriculados não pode ser nula."
        }
    )
