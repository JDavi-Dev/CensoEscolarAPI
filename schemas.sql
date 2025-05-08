DROP TABLE IF EXISTS tb_instituicao;

CREATE TABLE tb_instituicao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    regiao TEXT,
    cod_regiao INTEGER,
    estado TEXT,
    sigla TEXT,
    cod_estado INTEGER,
    municipio TEXT,
    cod_municipio INTEGER,
    mesorregiao TEXT,
    cod_mesorregiao INTEGER,
    microrregiao TEXT,
    cod_microrregiao INTEGER,
    entidade TEXT,
    cod_entidade INTEGER,
    qt_mat_bas INTEGER,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);