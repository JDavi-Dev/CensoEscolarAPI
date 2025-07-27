from flask_restful import Resource, marshal

from sqlalchemy.exc import SQLAlchemyError
from flask import abort

from helpers.database import db
from helpers.logging import logger, log_exception

from models import UF, CensoEscolar, Mesorregiao, Microrregiao, Municipio, Instituicao
from models.CensoEscolar import CensoEscolar, censo_fields

class CensosEscolaresResource(Resource):
    def get(self, ano_censo):
        logger.info(f"Get - Censo escolar por ano: {ano_censo}")
        try:
            censos = db.session.execute(
                db.select(CensoEscolar).filter_by(ano_censo=ano_censo)
            ).scalars().all()

            if not censos:
                logger.warning(f"Censo escolar {ano_censo} não encontrado.")
                return {"mensagem": "Censo escolar não encontrado."}, 404
            
            logger.info(f"Censo escolar {ano_censo} retornado com sucesso")
            return marshal(censos, censo_fields), 200
        except SQLAlchemyError:
            log_exception("Exception SQLAlchemy ao buscar censo escolar por ano.")
            db.session.rollback()
            abort(500, description="Problema com o banco de dados.")
        except Exception:
            log_exception("Erro inesperado ao buscar censo escolar por ano")
            abort(500, description="Ocorreu um erro inesperado.")


class CensoEscolarEstadoResource(Resource):
    def get(self, ano_censo, cod_estado):
        logger.info(f"Get - Censo escolar {ano_censo} por código estado: {cod_estado}")
        try:
            censo = db.session.execute(
                db.select(CensoEscolar).filter_by(ano_censo=ano_censo, cod_estado=cod_estado)
            ).scalar_one_or_none()

            if censo is None:
                logger.warning(f"Censo escolar {ano_censo} do estado {cod_estado} não encontrado.")
                return {"mensagem": "Censo escolar não encontrado."}, 404

            logger.info(f"Censo escolar {ano_censo} do estado {cod_estado} retornado com sucesso")
            return marshal(censo, censo_fields), 200

        except SQLAlchemyError:
            log_exception("Exception SQLAlchemy ao buscar censo escolar por estado.")
            db.session.rollback()
            abort(500, description="Problema com o banco de dados.")
        except Exception:
            log_exception("Erro inesperado ao buscar censo escolar por estado.")
            abort(500, description="Ocorreu um erro inesperado.")