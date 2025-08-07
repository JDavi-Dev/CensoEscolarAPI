from flask import request, abort
from flask_restful import Resource, marshal

from sqlalchemy.exc import SQLAlchemyError

from helpers.database import db
from helpers.logging import logger, log_exception 

from models.Mesorregiao import mesorregiao_fields, Mesorregiao

class MesorregioesResouce(Resource):
    def get(self):
        logger.info(f"Get - Todas as messorregioes")
        
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 22))

        try:
            mesorregiao = db.session.execute(
                db.select(Mesorregiao)
                .offset((page - 1) * per_page)
                .limit(per_page)
                ).scalars().all()

            logger.info(f"Mesorregioes retornadas com sucesso")
            return marshal(mesorregiao, mesorregiao_fields), 200

        except SQLAlchemyError:
            log_exception("Exception SQLAlchemy ao buscar messorregioes.")
            db.session.rollback()
            abort(500, description="Problema com o banco de dados.")
        except Exception:
            log_exception("Erro inesperado ao buscar messorregioes")
            abort(500, description="Ocorreu um erro inesperado.")

    def post(self):
        logger.info("Post - Mesorregiao")
        mesorregiao_data = request.get_json()

        try:
            nova_mesorregiao = Mesorregiao(**mesorregiao_data)

            db.session.add(nova_mesorregiao)
            db.session.commit()

            logger.info(f"Nova Mesorregiao com codigo {nova_mesorregiao.cod_mesorregiao} cadastrada com sucesso")
            return marshal(nova_mesorregiao, mesorregiao_fields), 201
        
        except SQLAlchemyError:
            log_exception("Exception SQLAlchemy ao inserir nova mesorregiao.")
            db.session.rollback()
            abort(500, description="Problema com o banco de dados.")
        except Exception:
            log_exception("Erro inesperado ao inserir nova mesorregiao")
            abort(500, description="Ocorreu um erro inesperado.")

class MesorregiaoResource(Resource):
    def get(self, cod_mesorregiao):
        logger.info(f"Get - Mesorregiao por código: {cod_mesorregiao}")

        try:
            mesorregiao = db.session.execute(
                db.select(Mesorregiao)
                .filter_by(cod_mesorregiao=cod_mesorregiao)
            ).scalar_one_or_none()

            if mesorregiao is None:
                logger.warning(f"Mesorregiao com código {cod_mesorregiao} não encontrada.")
                return {"mensagem": "Mesorregiao não encontrada."}, 404

            logger.info(f"Mesorregiao com código {cod_mesorregiao} retornada com sucesso")            
            return marshal(mesorregiao, mesorregiao_fields), 200

        except SQLAlchemyError:
            log_exception("Exception SQLAlchemy ao buscar mesorregiao por código.")
            db.session.rollback()
            abort(500, description="Problema com o banco de dados.")
        except Exception:
            log_exception("Erro inesperado ao buscar mesorregiao")
            abort(500, description="Ocorreu um erro inesperado.")

    def put(self, cod_mesorregiao):
        logger.info(f"Put - Tentativa de atualizar mesorregiao com código: {cod_mesorregiao}")
        mesorregiao_data = request.get_json()

        try:
            mesorregiao = db.session.execute(
                db.select(Mesorregiao)
                .filter_by(cod_mesorregiao=cod_mesorregiao)
            ).scalar_one_or_none()

            if mesorregiao is None:
                logger.warning(f"Mesorregiao com código {cod_mesorregiao} não encontrada para atualizar.")
                return {"mensagem": "Mesorregiao não encontrada."}, 404

            for key, value in mesorregiao_data.items():
                setattr(mesorregiao, key, value)

            db.session.commit()

            logger.info(f"Mesorregiao com código {cod_mesorregiao} atualizada com sucesso.")
            return {"mensagem": "Mesorregiao atualizada com sucesso."}, 200
        
        except SQLAlchemyError:
            log_exception("Exception SQLAlchemy ao atualizar mesorregiao.")
            db.session.rollback()
            abort(500, description="Problema com o banco de dados.")
        except Exception:
            log_exception(f"Erro inesperado ao atualizar mesorregiao")
            abort(500, description="Ocorreu um erro inesperado.")

    def delete(self, cod_mesorregiao):
        logger.info(f"Delete - Tentativa de deleção mesorregiao com código: {cod_mesorregiao}")

        try:
            mesorregiao = db.session.execute(
                db.select(Mesorregiao)
                .filter_by(cod_mesorregiao=cod_mesorregiao)
            ).scalar_one_or_none()

            if mesorregiao is None:
                logger.warning(f"Mesorregiao com código {cod_mesorregiao} não encontrada para deleção.")
                return {"mensagem": "Mesorregiao não encontrada."}, 404
            
            db.session.delete(mesorregiao)
            db.session.commit()

            logger.info(f"Mesorregiao com código {cod_mesorregiao} removida com sucesso.")
            return {"mensagem": "Mesorregiao removida com sucesso."}, 200
        
        except SQLAlchemyError:
            log_exception("Exception SQLAlchemy ao deletar mesorregiao.")
            db.session.rollback()
            abort(500, description="Problema com o banco de dados.")
        except Exception:
            log_exception("Erro inesperado ao deletar mesorregiao")
            abort(500, description="Ocorreu um erro inesperado.")