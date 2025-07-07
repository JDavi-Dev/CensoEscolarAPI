from flask_restful import Resource, marshal

import psycopg2

from helpers.database import getConnection
from helpers.logging import logger, log_exception

from models.CensoEscolar import CensoEscolar, censo_fields

class CensosEscolaresResource(Resource):
    def get(self, ano_censo):
        logger.info(f"Get - Censo escolar por ano: {ano_censo}")
        try:
            censosEscolares = []
            conn = getConnection()
            cursor = conn.cursor()
            cursor.execute(
                'SELECT * FROM censo_escolar WHERE ano_censo = %s', (ano_censo,))
            resultSet = cursor.fetchall()

            if not resultSet:
                logger.warning(f"Censo escolar {ano_censo} não encontrado.")
                return {"mensagem": "Censo escolar não encontrado."}, 404
            
            for row in resultSet:
                censoEscolar = CensoEscolar(
                    ano_censo=row[0],
                    estado=row[1],
                    sigla=row[2],
                    cod_estado=row[3],
                    total_matriculas=row[4]
                )
                censosEscolares.append(censoEscolar)

        except psycopg2.Error:
            log_exception("Exception postgres")
            return {"mensagem": "Problema com o banco de dados."}, 500
        finally:
            conn.close()

        logger.info(f"Censo escolar {ano_censo} retornado com sucesso")
        return marshal(censosEscolares, censo_fields), 200

class CensoEscolarEstadoResource(Resource):
    def get(self, ano_censo, cod_estado):
        logger.info(f"Get - Censo escolar {ano_censo} por código estado: {cod_estado}")
        try:
            conn = getConnection()
            cursor = conn.cursor()
            cursor.execute(
                'SELECT * FROM censo_escolar WHERE ano_censo = %s and cod_estado = %s', (ano_censo, cod_estado,))
            row = cursor.fetchone()

            if row is None:
                logger.warning(f"Censo escolar {ano_censo} do estado {cod_estado} não encontrado.")
                return {"mensagem": "Censo escolar não encontrado."}, 404

            logger.info(row)
            censoEscolar = CensoEscolar(
                ano_censo=row[0],
                estado=row[1],
                sigla=row[2],
                cod_estado=row[3],
                total_matriculas=row[4]
            )

        except psycopg2.Error as e:
            log_exception("Exception postgres")
            return {"mensagem": "Problema com o banco de dados."}, 500
        finally:
            conn.close()

        logger.info(f"Censo escolar {ano_censo} do estado {cod_estado} retornado com sucesso")
        return marshal(censoEscolar, censo_fields), 200