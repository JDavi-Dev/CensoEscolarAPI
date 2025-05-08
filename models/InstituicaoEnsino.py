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
