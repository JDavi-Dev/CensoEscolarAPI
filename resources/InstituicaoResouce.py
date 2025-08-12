from flask import request, abort
from flask_restful import Resource, marshal

from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import or_, cast, String

from helpers.database import db
from helpers.logging import logger, log_exception 

from models.Instituicao import instiuicao_fields, Instituicao, InstituicaoEnsinoSchema


class InstituicoesResouce(Resource):
    def get(self, ano_censo):
        logger.info("Get - Instituições por ano")

        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 100))
        cod_estado = request.args.get('cod_estado')
        search_query = request.args.get('q', "").strip()

        try:
            # Query base
            query = db.select(Instituicao).filter_by(ano_censo=ano_censo)

            count_query = db.select(db.func.count()).select_from(Instituicao).filter_by(ano_censo=ano_censo)

            # Filtro por estado
            if cod_estado:
                query = query.filter_by(cod_estado=cod_estado)
                count_query = count_query.filter_by(cod_estado=cod_estado)
                logger.info(f"Filtrando instituições por ano {ano_censo} e estado {cod_estado}")

            # Filtro por busca
            if search_query:
                logger.info(f"Aplicando filtro de busca: '{search_query}'")
                like_pattern = f"%{search_query}%"
                search_filter = or_(
                    Instituicao.entidade.ilike(like_pattern),
                    Instituicao.municipio.ilike(like_pattern),
                    Instituicao.mesorregiao.ilike(like_pattern),
                    Instituicao.microrregiao.ilike(like_pattern),
                    Instituicao.regiao.ilike(like_pattern),
                    cast(Instituicao.cod_entidade, String).ilike(like_pattern)
                )
                query = query.filter(search_filter)
                count_query = count_query.filter(search_filter)

                # Ordenar por relevância:
                query = query.order_by(
                    Instituicao.entidade.ilike(like_pattern).desc(),
                    Instituicao.municipio.ilike(like_pattern).desc(),
                    Instituicao.cod_entidade.asc()
                )
            else:
                # Ordenação padrão sem busca
                query = query.order_by(Instituicao.entidade.asc())

            # Contagem total filtrada
            total = db.session.execute(count_query).scalar()

            instituicoes = db.session.execute(
                query
                .filter_by(ano_censo=ano_censo)
                .offset((page - 1) * per_page)
                .limit(per_page)
            ).scalars().all()

            if not instituicoes:
                logger.warning(f"Nenhuma instituição encontrada para o ano {ano_censo} e estado {cod_estado if cod_estado else 'todos os estados'}.")
                return {
                    "mensagem": "Nenhuma instituição encontrada.",
                    "instituicoes": [],
                    "total": 0
                }, 404

            logger.info(f"Instituições do ano {ano_censo} (estado: {cod_estado if cod_estado else 'todos'}) retornadas com sucesso")
            return { "instituicoes": marshal(instituicoes, instiuicao_fields), "total": total }, 200

        except SQLAlchemyError:
            log_exception("Exception SQLAlchemy ao listar instituições.")
            db.session.rollback()
            abort(500, description="Problema com o banco de dados.")
        except Exception:
            log_exception("Erro inesperado ao listar instituições")
            abort(500, description="Ocorreu um erro inesperado.")

class NovaInstituicaoResouce(Resource):
    def post(self):
        logger.info("Post - Instituição")
        instituicao_schema = InstituicaoEnsinoSchema()
        instituicao_data = request.get_json()

        try:
            validated_data = instituicao_schema.load(instituicao_data)
            nova_instituicao = Instituicao(**validated_data)

            db.session.add(nova_instituicao)
            db.session.commit()

            logger.info(f"Nova instituição com codigo {nova_instituicao.cod_entidade} cadastrada com sucesso")
            return marshal(nova_instituicao, instiuicao_fields), 201
        
        except ValidationError as err:
            logger.warning(f"Erro(s) na validação ao inserir nova instituição: \n\t{err.messages}")
            return {"mensagem": "Falha na validação dos dados. Verifique os campos e tente novamente.", "detalhes": err.messages}, 422
        except SQLAlchemyError:
            log_exception("Exception SQLAlchemy ao inserir nova instituição.")
            db.session.rollback()
            abort(500, description="Problema com o banco de dados.")
        except Exception:
            log_exception("Erro inesperado ao inserir nova instituição")
            abort(500, description="Ocorreu um erro inesperado.")


class InstituicaoResouce(Resource):
    def get(self, ano_censo, cod_entidade):
        logger.info(f"Get - Instituição por ano {ano_censo} e código de entidade: {cod_entidade}")

        try:
            instituicao = db.session.execute(
                db.select(Instituicao)
                .filter_by(ano_censo=ano_censo, cod_entidade=cod_entidade)
            ).scalar_one_or_none()

            if instituicao is None:
                logger.warning(f"Instituição com ano {ano_censo} e código {cod_entidade} não encontrada.")
                return {"mensagem": "Instituição não encontrada."}, 404

            logger.info(f"Instituição com ano {ano_censo} e codigo {cod_entidade} retornada com sucesso")            
            return marshal(instituicao, instiuicao_fields), 200

        except SQLAlchemyError:
            log_exception("Exception SQLAlchemy ao buscar instituição por ano e código.")
            db.session.rollback()
            abort(500, description="Problema com o banco de dados.")
        except Exception:
            log_exception("Erro inesperado ao buscar instituição")
            abort(500, description="Ocorreu um erro inesperado.")
        
    def put(self, ano_censo, cod_entidade):
        logger.info(f"Put - Tentativa de atualizar instituição com ano {ano_censo} e código: {cod_entidade}")
        instituicao_schema = InstituicaoEnsinoSchema()
        instituicao_data = request.get_json()

        try:
            instituicao = db.session.execute(
                db.select(Instituicao)
                .filter_by(ano_censo=ano_censo, cod_entidade=cod_entidade)
            ).scalar_one_or_none()

            if instituicao is None:
                logger.warning(f"Instituição com ano {ano_censo} e código {cod_entidade} não encontrada para atualizar.")
                return {"mensagem": "Instituição não encontrada."}, 404

            validated_data = instituicao_schema.load(instituicao_data, partial=True)

            for key, value in validated_data.items():
                setattr(instituicao, key, value)

            db.session.commit()

            logger.info(f"Instituição com ano {ano_censo} e código {cod_entidade} atualizada com sucesso.")
            return {"mensagem": "Instituição atualizada com sucesso."}, 200
        
        except ValidationError as err:
            logger.warning(f"Erro de validação ao atualizar instituição com código {cod_entidade} do ano {ano_censo}\n\t{err.messages}")
            return {"mensagem": "Falha na validação dos dados. Verifique os campos e tente novamente.", "detalhes": err.messages}, 422
        except SQLAlchemyError:
            log_exception("Exception SQLAlchemy ao atualizar instituição.")
            db.session.rollback()
            abort(500, description="Problema com o banco de dados.")
        except Exception:
            log_exception(f"Erro inesperado ao atualizar instituição")
            abort(500, description="Ocorreu um erro inesperado.")

    def delete(self, ano_censo, cod_entidade):
        logger.info(f"Delete - Tentativa de deleção da instituição com código: {cod_entidade}")

        try:
            instituicao = db.session.execute(
                db.select(Instituicao)
                .filter_by(ano_censo=ano_censo, cod_entidade=cod_entidade)
            ).scalar_one_or_none()

            if instituicao is None:
                logger.warning(f"Instituição com ano {ano_censo} e código {cod_entidade} não encontrada para deleção.")
                return {"mensagem": "Instituição não encontrada."}, 404
            
            db.session.delete(instituicao)
            db.session.commit()

            logger.info(f"Instituição com ano {ano_censo} e código {cod_entidade} removida com sucesso.")
            return {"mensagem": "Instituição removida com sucesso."}, 200
        
        except SQLAlchemyError:
            log_exception("Exception SQLAlchemy ao deletar instituição.")
            db.session.rollback()
            abort(500, description="Problema com o banco de dados.")
        except Exception:
            log_exception("Erro inesperado ao deletar instituição")
            abort(500, description="Ocorreu um erro inesperado.")