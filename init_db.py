import sqlite3
import json

# Conectar ou criar um banco de dados SQLite
conn = sqlite3.connect("censo_escolar.db")
cursor = conn.cursor()

# Executar o script SQL para criar a tabela
with open("schemas.sql", "r", encoding="utf-8") as sql_file:
    sql_script = sql_file.read()
    cursor.executescript(sql_script)

# Carregar os dados do arquivo JSON
with open("censo_nordeste_2024.json", "r", encoding="utf-8") as json_file:
    dados = json.load(json_file)

# Inserir os dados na tabela
for item in dados:
    cursor.execute("""
    INSERT INTO tb_instituicao (
        regiao, cod_regiao, estado, sigla, cod_estado, municipio, cod_municipio,
        mesorregiao, cod_mesorregiao, microrregiao, cod_microrregiao,
        entidade, cod_entidade, qt_mat_bas
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        item["regiao"], item["cod_regiao"], item["estado"], item["sigla"], item["cod_estado"],
        item["municipio"], item["cod_municipio"], item["mesorregiao"],
        item["cod_mesorregiao"], item["microrregiao"], item["cod_microrregiao"], 
        item["entidade"], item["cod_entidade"], item["qt_mat_bas"]
    ))

# Confirmar e fechar conexão
conn.commit()
conn.close()
