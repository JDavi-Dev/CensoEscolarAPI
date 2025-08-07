from flask import request, abort
from flask_restful import Resource, marshal

from sqlalchemy.exc import SQLAlchemyError

from helpers.database import db
from helpers.logging import logger, log_exception 

from models.Municipio import municipio_fields, Municipio

class MunicipiosResouce(Resource):
    def get(self):
        logger.info(f"Get - Todas os municipios")

        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 100))

        try:
            municipio = db.session.execute(
                db.select(Municipio)
                .offset((page - 1) * per_page)
                .limit(per_page)
                ).scalars().all()

            logger.info(f"Municipios retornadas com sucesso")
            return marshal(municipio, municipio_fields), 200

        except SQLAlchemyError:
            log_exception("Exception SQLAlchemy ao buscar municipios.")
            db.session.rollback()
            abort(500, description="Problema com o banco de dados.")
        except Exception:
            log_exception("Erro inesperado ao buscar municipios")
            abort(500, description="Ocorreu um erro inesperado.")

    def post(self):
        logger.info("Post - Municipio")
        municipio_data = request.get_json()

        try:
            novo_municipio = Municipio(**municipio_data)

            db.session.add(novo_municipio)
            db.session.commit()

            logger.info(f"Nova municipio com codigo {novo_municipio.cod_municipio} cadastrada com sucesso")
            return marshal(novo_municipio, municipio_fields), 201
        
        except SQLAlchemyError:
            log_exception("Exception SQLAlchemy ao inserir novo municipio.")
            db.session.rollback()
            abort(500, description="Problema com o banco de dados.")
        except Exception:
            log_exception("Erro inesperado ao inserir novo municipio")
            abort(500, description="Ocorreu um erro inesperado.")

class MunicipioResource(Resource):
    def get(self, cod_municipio):
        logger.info(f"Get - Municipio por código: {cod_municipio}")

        try:
            municipio = db.session.execute(
                db.select(Municipio)
                .filter_by(cod_municipio=cod_municipio)
            ).scalar_one_or_none()

            if municipio is None:
                logger.warning(f"Municipio com código {cod_municipio} não encontrado.")
                return {"mensagem": "Municipio não encontrado."}, 404

            logger.info(f"Municipio com código {cod_municipio} retornado com sucesso")            
            return marshal(municipio, municipio_fields), 200

        except SQLAlchemyError:
            log_exception("Exception SQLAlchemy ao buscar municipio por código.")
            db.session.rollback()
            abort(500, description="Problema com o banco de dados.")
        except Exception:
            log_exception("Erro inesperado ao buscar municipio")
            abort(500, description="Ocorreu um erro inesperado.")

    def put(self, cod_municipio):
        logger.info(f"Put - Tentativa de atualizar municipio com código: {cod_municipio}")
        municipio_data = request.get_json()

        try:
            municipio = db.session.execute(
                db.select(Municipio)
                .filter_by(cod_municipio=cod_municipio)
            ).scalar_one_or_none()

            if municipio is None:
                logger.warning(f"Municipio com código {cod_municipio} não encontrado para atualizar.")
                return {"mensagem": "Municipio não encontrado."}, 404

            for key, value in municipio_data.items():
                setattr(municipio, key, value)

            db.session.commit()

            logger.info(f"Municipio com código {cod_municipio} atualizado com sucesso.")
            return {"mensagem": "Municipio atualizado com sucesso."}, 200
        
        except SQLAlchemyError:
            log_exception("Exception SQLAlchemy ao atualizar municipio.")
            db.session.rollback()
            abort(500, description="Problema com o banco de dados.")
        except Exception:
            log_exception(f"Erro inesperado ao atualizar municipio")
            abort(500, description="Ocorreu um erro inesperado.")

    def delete(self, cod_municipio):
        logger.info(f"Delete - Tentativa de deleção municipio com código: {cod_municipio}")

        try:
            municipio = db.session.execute(
                db.select(Municipio)
                .filter_by(cod_municipio=cod_municipio)
            ).scalar_one_or_none()

            if municipio is None:
                logger.warning(f"Municipio com código {cod_municipio} não encontrado para deleção.")
                return {"mensagem": "Municipio não encontrado."}, 404
            
            db.session.delete(municipio)
            db.session.commit()

            logger.info(f"Municipio com código {cod_municipio} removido com sucesso.")
            return {"mensagem": "Municipio removido com sucesso."}, 200
        
        except SQLAlchemyError:
            log_exception("Exception SQLAlchemy ao deletar municipio.")
            db.session.rollback()
            abort(500, description="Problema com o banco de dados.")
        except Exception:
            log_exception("Erro inesperado ao deletar municipio")
            abort(500, description="Ocorreu um erro inesperado.")