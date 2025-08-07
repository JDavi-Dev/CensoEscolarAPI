from flask import request, abort
from flask_restful import Resource, marshal

from sqlalchemy.exc import SQLAlchemyError

from helpers.database import db
from helpers.logging import logger, log_exception 

from models.UF import uf_fields, UF

class UfsResouce(Resource):
    def get(self):
        logger.info(f"Get - Todas as UFs")

        try:
            uf = db.session.execute(db.select(UF)).scalars().all()

            logger.info(f"Ufs retornadas com sucesso")
            return marshal(uf, uf_fields), 200

        except SQLAlchemyError:
            log_exception("Exception SQLAlchemy ao buscar Ufs.")
            db.session.rollback()
            abort(500, description="Problema com o banco de dados.")
        except Exception:
            log_exception("Erro inesperado ao buscar Ufs")
            abort(500, description="Ocorreu um erro inesperado.")

    def post(self):
        logger.info("Post - UF")
        uf_data = request.get_json()

        try:
            nova_uf = UF(**uf_data)

            db.session.add(nova_uf)
            db.session.commit()

            logger.info(f"Nova UF com codigo {nova_uf.cod_uf} cadastrada com sucesso")
            return marshal(nova_uf, uf_fields), 201
        
        except SQLAlchemyError:
            log_exception("Exception SQLAlchemy ao inserir nova UF.")
            db.session.rollback()
            abort(500, description="Problema com o banco de dados.")
        except Exception:
            log_exception("Erro inesperado ao inserir nova UF")
            abort(500, description="Ocorreu um erro inesperado.")

class UfResource(Resource):
    def get(self, cod_uf):
        logger.info(f"Get - UF por código: {cod_uf}")

        try:
            uf = db.session.execute(
                db.select(UF)
                .filter_by(cod_uf=cod_uf)
            ).scalar_one_or_none()

            if uf is None:
                logger.warning(f"Uf com código {cod_uf} não encontrada.")
                return {"mensagem": "UF não encontrada."}, 404

            logger.info(f"Uf com código {cod_uf} retornada com sucesso")            
            return marshal(uf, uf_fields), 200

        except SQLAlchemyError:
            log_exception("Exception SQLAlchemy ao buscar uf por código.")
            db.session.rollback()
            abort(500, description="Problema com o banco de dados.")
        except Exception:
            log_exception("Erro inesperado ao buscar uf")
            abort(500, description="Ocorreu um erro inesperado.")

    def put(self, cod_uf):
        logger.info(f"Put - Tentativa de atualizar UF com código: {cod_uf}")
        uf_data = request.get_json()

        try:
            uf = db.session.execute(
                db.select(UF)
                .filter_by(cod_uf=cod_uf)
            ).scalar_one_or_none()

            if uf is None:
                logger.warning(f"UF com código {cod_uf} não encontrada para atualizar.")
                return {"mensagem": "UF não encontrada."}, 404

            for key, value in uf_data.items():
                setattr(uf, key, value)

            db.session.commit()

            logger.info(f"UF com código {cod_uf} atualizada com sucesso.")
            return {"mensagem": "UF atualizada com sucesso."}, 200
        
        except SQLAlchemyError:
            log_exception("Exception SQLAlchemy ao atualizar UF.")
            db.session.rollback()
            abort(500, description="Problema com o banco de dados.")
        except Exception:
            log_exception(f"Erro inesperado ao atualizar UF")
            abort(500, description="Ocorreu um erro inesperado.")

    def delete(self, cod_uf):
        logger.info(f"Delete - Tentativa de deleção uf com código: {cod_uf}")

        try:
            uf = db.session.execute(
                db.select(UF)
                .filter_by(cod_uf=cod_uf)
            ).scalar_one_or_none()

            if uf is None:
                logger.warning(f"Uf com código {cod_uf} não encontrada para deleção.")
                return {"mensagem": "Uf não encontrada."}, 404
            
            db.session.delete(uf)
            db.session.commit()

            logger.info(f"Uf com código {cod_uf} removida com sucesso.")
            return {"mensagem": "Uf removida com sucesso."}, 200
        
        except SQLAlchemyError:
            log_exception("Exception SQLAlchemy ao deletar Uf.")
            db.session.rollback()
            abort(500, description="Problema com o banco de dados.")
        except Exception:
            log_exception("Erro inesperado ao deletar Uf")
            abort(500, description="Ocorreu um erro inesperado.")