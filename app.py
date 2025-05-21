from flask import request, jsonify
import sqlite3
from marshmallow import ValidationError

from helpers.application import app
from helpers.database import getConnection
from helpers.logging import logger
from helpers.CORS import cors

from models.InstituicaoEnsino import InstituicaoEnsino, InstituicaoEnsinoSchema

cors.init_app(app)

@app.route("/")
def index():
    versao = {"versao": "1.0.0"}
    return jsonify(versao), 200

@app.get("/instituicoes")
def instituicoesResource():
    logger.info("Get - Instituições")
    
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))

    try:
        instituicoesEnsino = []
        cursor = getConnection().cursor()

        # Calcular o offset para a consulta
        offset = (page - 1) * per_page
        
        cursor.execute('SELECT * FROM tb_instituicao LIMIT ? OFFSET ?', (per_page, offset))
        resultSet = cursor.fetchall()

        for row in resultSet:
            logger.info(row)
            instituicaoEnsino = InstituicaoEnsino(
                regiao=row[0],
                cod_regiao=row[1],
                estado=row[2],
                sigla=row[3],
                cod_estado=row[4],
                municipio=row[5],
                cod_municipio=row[6],
                mesorregiao=row[7],
                microrregiao=row[8],
                entidade=row[9],
                cod_entidade=row[10],
                qt_mat_bas=row[11]
            )
            instituicoesEnsino.append(instituicaoEnsino.toDict())

    except sqlite3.Error as e:
        return jsonify({"mensagem": "Problema com o banco de dados."}), 500

    return jsonify(instituicoesEnsino), 200

@app.post("/instituicoes")
def instituicaoInsercaoResource():
    print("Post - Instituição")
    instituicaoEnsinoSchema = InstituicaoEnsinoSchema()
    instituicaoData = request.get_json()
    
    try:
        instituicaoJson = instituicaoEnsinoSchema.load(instituicaoData)
        conn = getConnection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO tb_instituicao (regiao, cod_regiao, estado, sigla, cod_estado, municipio, cod_municipio, mesorregiao, microrregiao, entidade, qt_mat_bas) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', 
            (instituicaoJson['regiao'], instituicaoJson['cod_regiao'], instituicaoJson['estado'], instituicaoJson['sigla'], instituicaoJson['cod_estado'], 
             instituicaoJson['municipio'], instituicaoJson['cod_municipio'], instituicaoJson['mesorregiao'],
             instituicaoJson['microrregiao'], instituicaoJson['entidade'], instituicaoJson['qt_mat_bas'])
        )
        conn.commit()
        cod_entidade = cursor.lastrowid
        instituicaoEnsino = InstituicaoEnsino(
            instituicaoJson['regiao'], 
            instituicaoJson['cod_regiao'], 
            instituicaoJson['estado'], 
            instituicaoJson['sigla'], 
            instituicaoJson['cod_estado'], 
            instituicaoJson['municipio'], 
            instituicaoJson['cod_municipio'], 
            instituicaoJson['mesorregiao'], 
            instituicaoJson['microrregiao'], 
            instituicaoJson['entidade'],
            cod_entidade, 
            instituicaoJson['qt_mat_bas']
        )
        return jsonify(instituicaoEnsino.toDict()), 200
    except ValidationError as err:
        return jsonify(err.messages), 400
    except sqlite3.Error as e:
        return jsonify({"mensagem": "Problema com o banco de dados."}), 500

    return jsonify({"mensagem": "Não cadastrado"}), 406

@app.route("/instituicoes/<int:cod_entidade>", methods=["DELETE"])
def instituicaoRemocaoResource(cod_entidade):
    print("Delete - Instituição")
    try:
        conn = getConnection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tb_instituicao WHERE cod_entidade = ?', (cod_entidade,))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"mensagem": "Instituição não encontrada."}), 404
    except sqlite3.Error as e:
        return jsonify({"mensagem": "Problema com o banco de dados."}), 500
    return jsonify({"mensagem": "Instituição removida com sucesso."}), 200

@app.route("/instituicoes/<int:cod_entidade>", methods=["PUT"])
def instituicaoAtualizacaoResource(cod_entidade):
    print("Put - Instituição")
    try:
        conn = getConnection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tb_instituicao WHERE cod_entidade = ?', (cod_entidade,))
        row = cursor.fetchone()

        if row is None:
            return jsonify({"mensagem": "Instituição não encontrada."}), 404

        instituicaoEnsinoSchema = InstituicaoEnsinoSchema()
        instituicaoData = request.get_json()
        instituicaoJson = instituicaoEnsinoSchema.load(instituicaoData)

        cursor.execute('UPDATE tb_instituicao SET regiao = ?, cod_regiao = ?, estado = ?, sigla = ?, cod_estado = ?, municipio = ?, cod_municipio = ?, mesorregiao = ?, microrregiao = ?, entidade = ?, qt_mat_bas = ? WHERE cod_entidade = ?',
                       (instituicaoJson['regiao'], instituicaoJson['cod_regiao'], instituicaoJson['estado'], instituicaoJson['sigla'], instituicaoJson['cod_estado'], 
                        instituicaoJson['municipio'], instituicaoJson['cod_municipio'], instituicaoJson['mesorregiao'], 
                        instituicaoJson['microrregiao'], instituicaoJson['entidade'],
                        instituicaoJson['qt_mat_bas'], cod_entidade))
        conn.commit()
    except ValidationError as err:
        return jsonify(err.messages), 400
    except sqlite3.Error as e:
        return jsonify({"mensagem": "Problema com o banco de dados."}), 500

    return jsonify({"mensagem": "Instituição atualizada com sucesso."}), 200

@app.route("/instituicoes/<int:cod_entidade>", methods=["GET"])
def instituicoesByCodEntidadeResource(cod_entidade):
    logger.info("Get - Instituições por código de entidade")
    logger.info(f"cod_entidade: {cod_entidade}")
    try:
        conn = getConnection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tb_instituicao WHERE cod_entidade = ?', (cod_entidade,))
        row = cursor.fetchone()

        if row is None:
            return jsonify({"mensagem": "Instituição não encontrada."}), 404

        instituicaoEnsino = InstituicaoEnsino(
            regiao=row[0],
            cod_regiao=row[1],
            estado=row[2],
            sigla=row[3],
            cod_estado=row[4],
            municipio=row[5],
            cod_municipio=row[6],
            mesorregiao=row[7],
            microrregiao=row[8],
            entidade=row[9],
            cod_entidade=row[10],
            qt_mat_bas=row[11]
        )

    except sqlite3.Error as e:
        return jsonify({"mensagem": "Problema com o banco de dados."}), 500
    finally:
        conn.close()

    return jsonify(instituicaoEnsino.toDict()), 200
