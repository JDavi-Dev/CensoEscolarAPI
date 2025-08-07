from flask import request, abort
from flask_restful import Resource, marshal

from sqlalchemy.exc import SQLAlchemyError

from helpers.database import db
from helpers.logging import logger, log_exception 

from models.Microrregiao import microrregiao_fields, Microrregiao

class MicrorregioesResouce(Resource):
    def get(self):
        logger.info(f"Get - Todas as microrregioes")
        
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 31))
        
        try:
            microrregioes = db.session.execute(
                db.select(Microrregiao)
                .offset((page - 1) * per_page)
                .limit(per_page)
                ).scalars().all()

            logger.info(f"Microrregioes retornadas com sucesso")
            return marshal(microrregioes, microrregiao_fields), 200

        except SQLAlchemyError:
            log_exception("Exception SQLAlchemy ao buscar microrregioes.")
            db.session.rollback()
            abort(500, description="Problema com o banco de dados.")
        except Exception:
            log_exception("Erro inesperado ao buscar microrregioes")
            abort(500, description="Ocorreu um erro inesperado.")

    def post(self):
        logger.info("Post - Microrregiao")
        microrregiao_data = request.get_json()

        try:
            nova_microrregiao = Microrregiao(**microrregiao_data)

            db.session.add(nova_microrregiao)
            db.session.commit()

            logger.info(f"Nova microrregiao com codigo {nova_microrregiao.cod_microrregiao} cadastrada com sucesso")
            return marshal(nova_microrregiao, microrregiao_fields), 201
        
        except SQLAlchemyError:
            log_exception("Exception SQLAlchemy ao inserir nova microrregiao.")
            db.session.rollback()
            abort(500, description="Problema com o banco de dados.")
        except Exception:
            log_exception("Erro inesperado ao inserir nova microrregiao")
            abort(500, description="Ocorreu um erro inesperado.")

class MicrorregiaoResource(Resource):
    def get(self, cod_microrregiao):
        logger.info(f"Get - Microrregiao por código: {cod_microrregiao}")

        try:
            microrregiao = db.session.execute(
                db.select(Microrregiao)
                .filter_by(cod_microrregiao=cod_microrregiao)
            ).scalar_one_or_none()

            if microrregiao is None:
                logger.warning(f"Microrregiao com código {cod_microrregiao} não encontrada.")
                return {"mensagem": "Microrregiao não encontrada."}, 404

            logger.info(f"Microrregiao com código {cod_microrregiao} retornada com sucesso")            
            return marshal(microrregiao, microrregiao_fields), 200

        except SQLAlchemyError:
            log_exception("Exception SQLAlchemy ao buscar microrregiao por código.")
            db.session.rollback()
            abort(500, description="Problema com o banco de dados.")
        except Exception:
            log_exception("Erro inesperado ao buscar microrregiao")
            abort(500, description="Ocorreu um erro inesperado.")

    def put(self, cod_microrregiao):
        logger.info(f"Put - Tentativa de atualizar microrregiao com código: {cod_microrregiao}")
        microrregiao_data = request.get_json()

        try:
            microrregiao = db.session.execute(
                db.select(Microrregiao)
                .filter_by(cod_microrregiao=cod_microrregiao)
            ).scalar_one_or_none()

            if microrregiao is None:
                logger.warning(f"Microrregiao com código {cod_microrregiao} não encontrada para atualizar.")
                return {"mensagem": "Microrregiao não encontrada."}, 404

            for key, value in microrregiao_data.items():
                setattr(microrregiao, key, value)

            db.session.commit()

            logger.info(f"Microrregiao com código {cod_microrregiao} atualizada com sucesso.")
            return {"mensagem": "Microrregiao atualizada com sucesso."}, 200
        
        except SQLAlchemyError:
            log_exception("Exception SQLAlchemy ao atualizar microrregiao.")
            db.session.rollback()
            abort(500, description="Problema com o banco de dados.")
        except Exception:
            log_exception(f"Erro inesperado ao atualizar microrregiao")
            abort(500, description="Ocorreu um erro inesperado.")

    def delete(self, cod_microrregiao):
        logger.info(f"Delete - Tentativa de deleção microrregiao com código: {cod_microrregiao}")

        try:
            microrregiao = db.session.execute(
                db.select(Microrregiao)
                .filter_by(cod_microrregiao=cod_microrregiao)
            ).scalar_one_or_none()

            if microrregiao is None:
                logger.warning(f"Microrregiao com código {cod_microrregiao} não encontrada para deleção.")
                return {"mensagem": "Microrregiao não encontrada."}, 404
            
            db.session.delete(microrregiao)
            db.session.commit()

            logger.info(f"Microrregiao com código {cod_microrregiao} removida com sucesso.")
            return {"mensagem": "Microrregiao removida com sucesso."}, 200
        
        except SQLAlchemyError:
            log_exception("Exception SQLAlchemy ao deletar microrregiao.")
            db.session.rollback()
            abort(500, description="Problema com o banco de dados.")
        except Exception:
            log_exception("Erro inesperado ao deletar microrregiao")
            abort(500, description="Ocorreu um erro inesperado.")