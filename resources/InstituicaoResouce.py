from flask import request
from flask_restful import Resource, marshal

import sqlite3
from marshmallow import ValidationError

from helpers.database import getConnection
from helpers.logging import logger, log_exception
from models.InstituicaoEnsino import instiuicao_fields

from models.InstituicaoEnsino import InstituicaoEnsino, InstituicaoEnsinoSchema


class InstituicoesResouce(Resource):
    def get(self):
        logger.info("Get - Instituições")

        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))

        try:
            instituicoesEnsino = []
            cursor = getConnection().cursor()

            # Calcular o offset para a consulta
            offset = (page - 1) * per_page

            cursor.execute(
                'SELECT * FROM tb_instituicao LIMIT ? OFFSET ?', (per_page, offset))
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
                instituicoesEnsino.append(instituicaoEnsino)

        except sqlite3.Error:
            logger.error("Exception sqlite")
            return {"mensagem": "Problema com o banco de dados."}, 500

        logger.info("Instituições retornadas com sucesso")
        return marshal(instituicoesEnsino, instiuicao_fields), 200

    def post(self):
        logger.info("Post - Instituição")
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
            logger.info(f"Nova instituição com codigo {cod_entidade} cadastrada com sucesso")
            return marshal(instituicaoEnsino, instiuicao_fields), 200
        except ValidationError as err:
            logger.warning(f"Erro(s) na validação ao inserir nova instituição: \n\t{err.messages}")
            return {"mensagem": "Falha na validação dos dados. Verifique os campos e tente novamente.", "detalhes": err.messages}, 422
        except sqlite3.Error:
            log_exception("Exception sqlite")
            return {"mensagem": "Problema com o banco de dados."}, 500


class InstituicaoResouce(Resource):
    def get(self, cod_entidade):
        logger.info(f"Get - Instituição por código de entidade: {cod_entidade}")
        try:
            conn = getConnection()
            cursor = conn.cursor()
            cursor.execute(
                'SELECT * FROM tb_instituicao WHERE cod_entidade = ?', (cod_entidade,))
            row = cursor.fetchone()

            if row is None:
                logger.warning(f"Instituição com código {cod_entidade} não encontrada.")
                return {"mensagem": "Instituição não encontrada."}, 404

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

        except sqlite3.Error:
            log_exception("Exception sqlite")
            return {"mensagem": "Problema com o banco de dados."}, 500
        finally:
            conn.close()

        logger.info(f"Instituição com codigo {cod_entidade} retornada com sucesso")
        return marshal(instituicaoEnsino, instiuicao_fields), 200

    def put(self, cod_entidade):
        logger.info(f"Put - Tentativa de atualizar instituição com código: {cod_entidade}")
        try:
            conn = getConnection()
            cursor = conn.cursor()
            cursor.execute(
                'SELECT * FROM tb_instituicao WHERE cod_entidade = ?', (cod_entidade,))
            row = cursor.fetchone()

            if row is None:
                logger.warning(f"Instituição com código {cod_entidade} não encontrada para atualizar.") 
                return {"mensagem": "Instituição não encontrada."}, 404

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
            logger.warning(f"Erro de validação ao atualizar instituição com código: {cod_entidade}\n\t{err.messages}")
            return {"mensagem": "Falha na validação dos dados. Verifique os campos e tente novamente.", "detalhes": err.messages}, 422
        except sqlite3.Error:
            log_exception("Exception sqlite")
            return {"mensagem": "Problema com o banco de dados."}, 500

        logger.info(f"Instituição com código {cod_entidade} atualizada com sucesso.")
        return {"mensagem": "Instituição atualizada com sucesso."}, 200

    def delete(self, cod_entidade):
        logger.info(f"Delete - Tentativa de deleção da instituição com código: {cod_entidade}")
        try:
            conn = getConnection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM tb_instituicao WHERE cod_entidade = ?', (cod_entidade,))
            conn.commit()
            if cursor.rowcount == 0:
                logger.warning(f"Instituição com código {cod_entidade} não encontrada para deleção.") 
                return {"mensagem": "Instituição não encontrada."}, 404
            else:
                logger.info(f"Instituição com código {cod_entidade} removida com sucesso.")
                return {"mensagem": "Instituição removida com sucesso."}, 200
        except sqlite3.Error:
            log_exception("Exception sqlite")
            return {"mensagem": "Problema com o banco de dados."}, 500