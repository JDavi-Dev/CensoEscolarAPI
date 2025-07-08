DROP TABLE IF EXISTS tb_uf;

CREATE TABLE tb_uf (
  cod_uf SERIAL PRIMARY KEY,
  sigla TEXT ,
  nome TEXT ,
  regiao TEXT
);

DROP TABLE IF EXISTS tb_mesorregiao;

CREATE TABLE tb_mesorregiao (
  cod_mesorregiao SERIAL PRIMARY KEY,
  nome TEXT,
  cod_uf INTEGER,
  FOREIGN KEY (cod_uf) REFERENCES tb_uf(cod_uf),
  UNIQUE (nome, cod_uf)
);

DROP TABLE IF EXISTS tb_microrregiao;

CREATE TABLE tb_microrregiao (
  cod_microrregiao SERIAL PRIMARY KEY,
  nome TEXT,
  cod_mesorregiao INTEGER,
  cod_uf INTEGER,
  FOREIGN KEY (cod_mesorregiao) REFERENCES tb_mesorregiao(cod_mesorregiao),
  FOREIGN KEY (cod_uf) REFERENCES tb_uf(cod_uf),
  UNIQUE (nome, cod_uf)
);

DROP TABLE IF EXISTS tb_municipio;

CREATE TABLE tb_municipio (
  cod_municipio SERIAL PRIMARY KEY,
  nome TEXT,
  cod_microrregiao INTEGER,
  cod_mesorregiao INTEGER,
  cod_uf INTEGER,
  FOREIGN KEY (cod_microrregiao) REFERENCES tb_microrregiao(cod_microrregiao),
  FOREIGN KEY (cod_mesorregiao) REFERENCES tb_mesorregiao(cod_mesorregiao),
  FOREIGN KEY (cod_uf) REFERENCES tb_uf(cod_uf)
);

DROP TABLE IF EXISTS tb_instituicao;

CREATE TABLE tb_instituicao (
    ano_censo INTEGER,
    regiao TEXT,
    cod_regiao INTEGER,
    estado TEXT,
    sigla TEXT,
    cod_estado INTEGER,
    municipio TEXT,
    cod_municipio INTEGER,
    mesorregiao TEXT,
    microrregiao TEXT,
    entidade TEXT,
    cod_entidade SERIAL,
    qt_mat_bas INTEGER,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (ano_censo, cod_entidade),
    FOREIGN KEY (cod_estado) REFERENCES tb_uf(cod_uf),
    FOREIGN KEY (cod_municipio) REFERENCES tb_municipio(cod_municipio),
    FOREIGN KEY (mesorregiao, cod_estado) REFERENCES tb_mesorregiao(nome, cod_uf),
    FOREIGN KEY (microrregiao, cod_estado) REFERENCES tb_microrregiao(nome, cod_uf)
);

DROP TABLE IF EXISTS censo_escolar;

CREATE TABLE censo_escolar (
    ano_censo INTEGER,
    estado TEXT,
    sigla TEXT,
    cod_estado INTEGER,
    total_matriculas BIGINT,
    PRIMARY KEY (ano_censo, cod_estado),
    FOREIGN KEY (cod_estado) REFERENCES tb_uf(cod_uf)
);