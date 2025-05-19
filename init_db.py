import sqlite3
import json

# Conectar ou criar um banco de dados SQLite
conn = sqlite3.connect("CensoEscolarExtrator.db")
cursor = conn.cursor()

# 1. Criar as tabelas conforme schemas.sql
with open("schemas.sql", "r", encoding="utf-8") as sql_file:
    sql_script = sql_file.read()
    cursor.executescript(sql_script)

# 2. Inserir Instituições
with open("censo_nordeste_2024.json", "r", encoding="utf-8") as f:
    insts = json.load(f)
for inst in insts:
    cursor.execute(
        "INSERT INTO tb_instituicao (\
            regiao, cod_regiao, estado, sigla, cod_estado,\
            municipio, cod_municipio, mesorregiao, cod_mesorregiao,\
            microrregiao, cod_microrregiao, entidade, cod_entidade, qt_mat_bas\
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            inst['regiao'],
            inst['cod_regiao'],
            inst['estado'],
            inst['sigla'],
            inst['cod_estado'],
            inst['municipio'],
            inst['cod_municipio'],
            inst['mesorregiao'],
            inst['cod_mesorregiao'],
            inst['microrregiao'],
            inst['cod_microrregiao'],
            inst.get('entidade'),
            inst.get('cod_entidade'),
            inst.get('qt_mat_bas')
        )
    )

# 3. Inserir UFs
with open("ufs_nordeste.json", "r", encoding="utf-8") as f:
    ufs = json.load(f)
for uf in ufs:
    cursor.execute(
        "INSERT OR IGNORE INTO tb_uf (cod_uf, sigla, nome, regiao) VALUES (?, ?, ?, ?)",
        (
            uf['cod_uf'],
            uf['sigla'],
            uf['nome'],
            uf['regiao']
        )
    )

# 4. Inserir Municípios
with open("municipios_nordeste.json", "r", encoding="utf-8") as f:
    munis = json.load(f)
for mun in munis:
    cursor.execute(
        "INSERT OR IGNORE INTO tb_municipio (cod_municipio, nome, cod_microrregiao, cod_mesorregiao, cod_uf) VALUES (?, ?, ?, ?, ?)",
        (
            mun['cod_municipio'],
            mun['nome'],
            mun['microrregiao']['id'],
            mun['microrregiao']['mesorregiao']['id'],
            mun['microrregiao']['mesorregiao']['UF']['id']
        )
    )


# 5. Inserir Mesorregiões
with open("mesorregioes_nordeste.json", "r", encoding="utf-8") as f:
    mesor = json.load(f)
for m in mesor:
    cursor.execute(
        "INSERT OR IGNORE INTO tb_mesorregiao (cod_mesorregiao, nome, cod_uf) VALUES (?, ?, ?)",
        (
            m['cod_mesorregiao'],
            m['nome'],
            m['UF']['id']
        )
    )

# 6. Inserir Microrregiões
with open("microrregioes_nordeste.json", "r", encoding="utf-8") as f:
    micros = json.load(f)
for micro in micros:
    cursor.execute(
        "INSERT OR IGNORE INTO tb_microrregiao (cod_microrregiao, nome, cod_mesorregiao, cod_uf) VALUES (?, ?, ?, ?)",
        (
            micro['cod_microrregiao'],
            micro['nome'],
            micro['mesorregiao']['id'],
            micro['mesorregiao']['UF']['id']
        )
    )



# Commit e fechar conexão
conn.commit()
conn.close()
print("Banco 'CensoEscolarExtrator.db' inicializado com sucesso.")
