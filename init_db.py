import psycopg2
import json

conn_params = {
    'database': 'censoescolar',
    'user': 'postgres',
    'password': '12345',
    'host': 'localhost',
    'port': '5432'
}

conn = psycopg2.connect(**conn_params)
cursor = conn.cursor()

# 1. Criar as tabelas conforme schemas.sql
with open("schemas.sql", "r", encoding="utf-8") as sql_file:
    sql_script = sql_file.read()
    cursor.execute(sql_script)

# 2. Inserir UFs
with open("ufs_brasil.json", "r", encoding="utf-8") as f:
    ufs = json.load(f)
for uf in ufs:
    cursor.execute(
        "INSERT INTO tb_uf (cod_uf, sigla, nome, regiao) VALUES (%s, %s, %s, %s)",
        (
            uf['cod_uf'],
            uf['sigla'],
            uf['nome'],
            uf['regiao']
        )
    )

# 3. Inserir Mesorregiões
with open("mesorregioes_brasil.json", "r", encoding="utf-8") as f:
    mesor = json.load(f)
for m in mesor:
    cursor.execute(
        "INSERT INTO tb_mesorregiao (cod_mesorregiao, nome, cod_uf) VALUES (%s, %s, %s)",
        (
            m['cod_mesorregiao'],
            m['nome'],
            m['UF']['id']
        )
    )

# 4. Inserir Microrregiões
with open("microrregioes_brasil.json", "r", encoding="utf-8") as f:
    micros = json.load(f)
for micro in micros:
    cursor.execute(
        "INSERT INTO tb_microrregiao (cod_microrregiao, nome, cod_mesorregiao, cod_uf) VALUES (%s, %s, %s, %s)",
        (
            micro['cod_microrregiao'],
            micro['nome'],
            micro['mesorregiao']['id'],
            micro['mesorregiao']['UF']['id']
        )
    )

# 5. Inserir Municípios
with open("municipios_brasil.json", "r", encoding="utf-8") as f:
    munis = json.load(f)
for mun in munis:
    microrregiao = mun.get('microrregiao')
    if microrregiao is None:
        print(f"Aviso: Município {mun['nome']} (código: {mun['cod_municipio']}) não possui microrregião. Pulando...")
        continue  # Pula para o próximo município

    mesorregiao = microrregiao.get('mesorregiao')
    if mesorregiao is None:
        print(f"Aviso: Microrregião do município {mun['nome']} (código: {mun['cod_municipio']}) não possui mesorregião. Pulando...")
        continue  # Pula para o próximo município

    cursor.execute(
        "INSERT INTO tb_municipio (cod_municipio, nome, cod_microrregiao, cod_mesorregiao, cod_uf) VALUES (%s, %s, %s, %s, %s)",
        (
            mun['cod_municipio'],
            mun['nome'],
            microrregiao['id'],
            mesorregiao['id'],
            mesorregiao['UF']['id']
        )
    )

# 6. Inserir Instituições
with open("censo_escolar_2024.json", "r", encoding="utf-8") as f:
    insts = json.load(f)
for inst in insts:
    cursor.execute(
        "INSERT INTO tb_instituicao (\
            regiao, cod_regiao, estado, sigla, cod_estado,\
            municipio, cod_municipio, mesorregiao, \
            microrregiao, entidade, cod_entidade, qt_mat_bas\
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
        (
            inst['regiao'],
            inst['cod_regiao'],
            inst['estado'],
            inst['sigla'],
            inst['cod_estado'],
            inst['municipio'],
            inst['cod_municipio'],
            inst['mesorregiao'],
            inst['microrregiao'],
            inst.get('entidade'),
            inst.get('cod_entidade'),
            inst.get('qt_mat_bas')
        )
    )

# Sicroniza a sequência com o valor máximo do cod_entidade
cursor.execute("SELECT setval('public.tb_instituicao_cod_entidade_seq', (SELECT MAX(cod_entidade) FROM tb_instituicao))")

# Commit e fechar conexão
conn.commit()
conn.close()
print("Banco inicializado com sucesso.")
