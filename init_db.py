import psycopg2
import json
from psycopg2.extras import execute_batch

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
    
# Uso de métodos que melhora o desempenho para inserções de grande volume de dados no postgres

# Método 1: Desativar índices/constraints antes da inserção
# Primeiro desativar constraints na tb_instituicao que dependem de tb_municipio
cursor.execute("""
    ALTER TABLE tb_instituicao 
    DROP CONSTRAINT IF EXISTS tb_instituicao_cod_municipio_fkey;
""")

# Agora podemos desativar as constraints em tb_municipio
cursor.execute("""
    ALTER TABLE tb_municipio 
    DROP CONSTRAINT IF EXISTS tb_municipio_pkey CASCADE;
""")
cursor.execute("""
    ALTER TABLE tb_municipio 
    DROP CONSTRAINT IF EXISTS tb_municipio_cod_microrregiao_fkey;
""")
cursor.execute("""
    ALTER TABLE tb_municipio 
    DROP CONSTRAINT IF EXISTS tb_municipio_cod_mesorregiao_fkey;
""")
cursor.execute("""
    ALTER TABLE tb_municipio 
    DROP CONSTRAINT IF EXISTS tb_municipio_cod_uf_fkey;
""")
print("Constraints desativadas para tb_municipio")

# Preparar dados para insert em batch
muni_data = []
for mun in munis:
    microrregiao = mun.get('microrregiao')
    if microrregiao is None:
        print(f"Aviso: Município {mun['nome']} (código: {mun['cod_municipio']}) não possui microrregião. Pulando...")
        continue

    mesorregiao = microrregiao.get('mesorregiao')
    if mesorregiao is None:
        print(f"Aviso: Microrregião do município {mun['nome']} (código: {mun['cod_municipio']}) não possui mesorregião. Pulando...")
        continue

    muni_data.append((
        mun['cod_municipio'],
        mun['nome'],
        microrregiao['id'],
        mesorregiao['id'],
        mesorregiao['UF']['id']
    ))

# Método 2: Inserção em batch
execute_batch(
    cursor,
    "INSERT INTO tb_municipio (cod_municipio, nome, cod_microrregiao, cod_mesorregiao, cod_uf) VALUES (%s, %s, %s, %s, %s)",
    muni_data,
    page_size=1000
)
print(f"Inseridos {len(muni_data)} municípios em batch")

# Método 1: Reativar índices/constraints após inserção
cursor.execute("""
    ALTER TABLE tb_municipio 
    ADD PRIMARY KEY (cod_municipio);
""")
cursor.execute("""
    ALTER TABLE tb_municipio 
    ADD CONSTRAINT tb_municipio_cod_microrregiao_fkey 
    FOREIGN KEY (cod_microrregiao) REFERENCES tb_microrregiao(cod_microrregiao);
""")
cursor.execute("""
    ALTER TABLE tb_municipio 
    ADD CONSTRAINT tb_municipio_cod_mesorregiao_fkey 
    FOREIGN KEY (cod_mesorregiao) REFERENCES tb_mesorregiao(cod_mesorregiao);
""")
cursor.execute("""
    ALTER TABLE tb_municipio 
    ADD CONSTRAINT tb_municipio_cod_uf_fkey 
    FOREIGN KEY (cod_uf) REFERENCES tb_uf(cod_uf);
""")

# 6. Inserir Instituições - OTIMIZADO (Métodos 1, 2 e 3)
censo_files = ["censo_escolar_2023.json", "censo_escolar_2024.json"]

# Método 1: Desativar índices/constraints antes da inserção
cursor.execute("""
    ALTER TABLE tb_instituicao 
    DROP CONSTRAINT IF EXISTS tb_instituicao_pkey CASCADE;
""")
cursor.execute("""
    ALTER TABLE tb_instituicao 
    DROP CONSTRAINT IF EXISTS tb_instituicao_cod_estado_fkey;
""")
cursor.execute("""
    ALTER TABLE tb_instituicao 
    DROP CONSTRAINT IF EXISTS tb_instituicao_mesorregiao_cod_estado_fkey;
""")
cursor.execute("""
    ALTER TABLE tb_instituicao 
    DROP CONSTRAINT IF EXISTS tb_instituicao_microrregiao_cod_estado_fkey;
""")
print("Constraints desativadas para tb_instituicao")


# Método 3: Transações em blocos grandes
batch_size = 10000
total_inst = 0

for censo_file in censo_files:
    print(f"Processando arquivo: {censo_file}")
    with open(censo_file, "r", encoding="utf-8") as f:
        insts = json.load(f)
    
    # Preparar dados para insert em batch
    inst_data = []
    for inst in insts:
        inst_data.append((
            inst['ano_censo'],
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
        ))
    
    # Método 2: Inserção em batch com commits periódicos
    for i in range(0, len(inst_data), batch_size):
        chunk = inst_data[i:i + batch_size]
        execute_batch(
            cursor,
            """INSERT INTO tb_instituicao (
                ano_censo, regiao, cod_regiao, estado, sigla, cod_estado,
                municipio, cod_municipio, mesorregiao, 
                microrregiao, entidade, cod_entidade, qt_mat_bas
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            chunk,
            page_size=5000
        )
        conn.commit()  # Método 4: Commit periódico
        print(f"Commit batch com {len(chunk)} registros (total: {i + len(chunk)}/{len(inst_data)})")
    
    total_inst += len(inst_data)

print(f"Total de instituições inseridas: {total_inst}")

# Método 1: Reativar índices/constraints após inserção
cursor.execute("""
    ALTER TABLE tb_instituicao 
    ADD PRIMARY KEY (ano_censo, cod_entidade);
""")
cursor.execute("""
    ALTER TABLE tb_instituicao 
    ADD CONSTRAINT tb_instituicao_cod_estado_fkey 
    FOREIGN KEY (cod_estado) REFERENCES tb_uf(cod_uf);
""")
cursor.execute("""
    ALTER TABLE tb_instituicao 
    ADD CONSTRAINT tb_instituicao_mesorregiao_cod_estado_fkey 
    FOREIGN KEY (mesorregiao, cod_estado) REFERENCES tb_mesorregiao(nome, cod_uf);
""")
cursor.execute("""
    ALTER TABLE tb_instituicao 
    ADD CONSTRAINT tb_instituicao_microrregiao_cod_estado_fkey 
    FOREIGN KEY (microrregiao, cod_estado) REFERENCES tb_microrregiao(nome, cod_uf);
""")
print("Constraints reativadas para tb_instituicao")

# Sincroniza a sequência com o valor máximo do cod_entidade
cursor.execute("SELECT setval('public.tb_instituicao_cod_entidade_seq', (SELECT MAX(cod_entidade) FROM tb_instituicao))")

# 7. Inserir dados consolidados na tabela censo_escolar
print("Populando tabela censo_escolar com dados consolidados...")

# Ano 2023
cursor.execute("""
    INSERT INTO censo_escolar (ano_censo, estado, sigla, cod_estado, total_matriculas)
    SELECT 
        i.ano_censo,
        u.nome as estado,
        u.sigla,
        u.cod_uf as cod_estado,
        COALESCE(SUM(i.qt_mat_bas), 0) as total_matriculas
    FROM tb_instituicao i
    JOIN tb_uf u ON i.cod_estado = u.cod_uf
    WHERE i.ano_censo = 2023
    GROUP BY i.ano_censo, u.nome, u.sigla, u.cod_uf
""")

# Ano 2024
cursor.execute("""
    INSERT INTO censo_escolar (ano_censo, estado, sigla, cod_estado, total_matriculas)
    SELECT 
        i.ano_censo,
        u.nome as estado,
        u.sigla,
        u.cod_uf as cod_estado,
        COALESCE(SUM(i.qt_mat_bas), 0) as total_matriculas
    FROM tb_instituicao i
    JOIN tb_uf u ON i.cod_estado = u.cod_uf
    WHERE i.ano_censo = 2024
    GROUP BY i.ano_censo, u.nome, u.sigla, u.cod_uf
""")

print("Tabela censo_escolar populada com sucesso.")

# Commit e fechar conexão
conn.commit()
conn.close()
print("Banco inicializado com sucesso.")