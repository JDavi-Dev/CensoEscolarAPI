import json
import gzip
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text

from helpers.application import app
from helpers.database import db
from helpers.logging import log_exception

from models import UF, CensoEscolar, Mesorregiao, Microrregiao, Municipio, Instituicao
from models.UF import UF
from models.Mesorregiao import Mesorregiao
from models.Microrregiao import Microrregiao
from models.Municipio import Municipio
from models.Instituicao import Instituicao

print("Iniciando a criação e população do banco de dados...")

with app.app_context():
    try:
        if db.session.query(UF).first() is not None:
            print("==> O banco de dados já contém dados (persistidos via volume).")
            print("==> Pulando a fase de população de dados.")
            exit(0) # Sai com sucesso sem rodar o resto
    except Exception as e:
        print(f"Buscando estrutura de tabelas... (Erro esperado se banco estiver vazio: {e})")

    # --- Inserção de dados ---
    def load_minified(path):
        open_func = gzip.open if path.endswith(".gz") else open

        with open_func(path, "rt", encoding="utf-8") as f:
            content = json.load(f)

        cols = content["columns"]
        return [dict(zip(cols, row)) for row in content["data"]]

    # 1. Inserir UFs
    print("Populando tabela tb_uf...")
    ufs_data = load_minified("data/ufs.json.gz")
    ufs_to_add = [
        UF(uf_item["cod_uf"], uf_item["sigla"], uf_item["nome"], uf_item["regiao"])
        for uf_item in ufs_data
    ]
    db.session.bulk_save_objects(ufs_to_add)
    db.session.commit()
    print(f"Inseridos {len(ufs_to_add)} UFs.")

    # 2. Inserir Mesorregiões
    print("Populando tabela tb_mesorregiao...")
    mesor_data = load_minified("data/mesorregioes.json.gz")
    mesor_to_add = [
        Mesorregiao(m_item["cod_mesorregiao"], m_item["nome"], m_item["cod_uf"])
        for m_item in mesor_data
    ]
    db.session.bulk_save_objects(mesor_to_add)
    db.session.commit()
    print(f"Inseridas {len(mesor_to_add)} Mesorregiões.")

    # 3. Inserir Microrregiões
    print("Populando tabela tb_microrregiao...")
    micros_data = load_minified("data/microrregioes.json.gz")
    micros_to_add = [
        Microrregiao(
            micro_item["cod_microrregiao"],
            micro_item["nome"],
            micro_item["cod_mesorregiao"],
            micro_item["cod_uf"]
        )
        for micro_item in micros_data
    ]
    db.session.bulk_save_objects(micros_to_add)
    db.session.commit()
    print(f"Inseridas {len(micros_to_add)} Microrregiões.")

    # 4. Inserir Municípios
    print("Populando tabela tb_municipio...")
    munis_data = load_minified("data/municipios.json.gz")
    
    muni_to_add = []
    skipped_munis = 0
    muni_to_add = [
        Municipio(
            mun_item["cod_municipio"],
            mun_item["nome"],
            mun_item["cod_microrregiao"],
            mun_item["cod_mesorregiao"],
            mun_item["cod_uf"]
        )
        for mun_item in munis_data
    ]
    
    # Inserção em massa de municípios
    db.session.bulk_save_objects(muni_to_add)
    db.session.commit()
    print(f"Inseridos {len(muni_to_add)} municípios. {skipped_munis} municípios pulados.")    

    # 5. Inserir Instituições - OTIMIZADO (Métodos 1, 2 e 3)
    censo_files = ["data/censo_escolar_2023.json.gz", "data/censo_escolar_2024.json.gz"]

    # Método 1: Desativar índices/constraints antes da inserção
    try:
        db.session.execute(text("""
            ALTER TABLE tb_instituicao 
            DROP CONSTRAINT IF EXISTS tb_instituicao_pkey CASCADE;
        """))
        db.session.execute(text("""
            ALTER TABLE tb_instituicao 
            DROP CONSTRAINT IF EXISTS tb_instituicao_cod_estado_fkey;
        """))
        db.session.execute(text("""
            ALTER TABLE tb_instituicao 
            DROP CONSTRAINT IF EXISTS tb_instituicao_cod_municipio_fkey;
        """))
        db.session.execute(text("""
            ALTER TABLE tb_instituicao 
            DROP CONSTRAINT IF EXISTS tb_instituicao_mesorregiao_cod_estado_fkey;
        """))
        db.session.execute(text("""
            ALTER TABLE tb_instituicao 
            DROP CONSTRAINT IF EXISTS tb_instituicao_microrregiao_cod_estado_fkey;
        """))
        db.session.commit()
        print("Constraints desativadas para tb_instituicao")
    except SQLAlchemyError:
        db.session.rollback()
        log_exception("Erro SQLAlchemy ao desativar as constraints de tb_instituicao")
    except Exception:
        db.session.rollback()
        log_exception("Erro inesperado ao desativar as constraints de tb_instituicao")


    # Método 3: Transações em blocos grandes
    batch_size = 10000
    total_inst = 0

    for file in censo_files:
        insts_json = load_minified(file)

        inst_objects = [
            Instituicao(
                ano_censo=inst["ano_censo"],
                regiao=inst["regiao"],
                cod_regiao=inst["cod_regiao"],
                estado=inst["estado"],
                sigla=inst["sigla"],
                cod_estado=inst["cod_estado"],
                municipio=inst["municipio"],
                cod_municipio=inst["cod_municipio"],
                mesorregiao=inst["mesorregiao"],
                microrregiao=inst["microrregiao"],
                entidade=inst.get("entidade"),
                cod_entidade=inst.get("cod_entidade"),
                qt_mat_bas=inst.get("qt_mat_bas", 0)
            )
            for inst in insts_json
        ]

        for i in range(0, len(inst_objects), batch_size):
            chunk = inst_objects[i:i + batch_size]
            db.session.bulk_save_objects(chunk)
            db.session.commit()
            print(f"Commit batch com {len(chunk)} registros (total: {i + len(chunk)}/{len(inst_objects)})")

        total_inst += len(inst_objects)

    print(f"Total de instituições inseridas: {total_inst}")

    # Método 1: Reativar índices/constraints após inserção
    try:
        db.session.execute(text("""
            ALTER TABLE tb_instituicao 
            ADD PRIMARY KEY (ano_censo, cod_entidade);
        """))
        db.session.execute(text("""
            ALTER TABLE tb_instituicao 
            ADD CONSTRAINT tb_instituicao_cod_estado_fkey 
            FOREIGN KEY (cod_estado) REFERENCES tb_uf(cod_uf);
        """))
        db.session.execute(text("""
            ALTER TABLE tb_instituicao 
            ADD CONSTRAINT tb_instituicao_cod_municipio_fkey
            FOREIGN KEY (cod_municipio) REFERENCES tb_municipio(cod_municipio);
        """))
        db.session.execute(text("""
            ALTER TABLE tb_instituicao 
            ADD CONSTRAINT tb_instituicao_mesorregiao_cod_estado_fkey 
            FOREIGN KEY (mesorregiao, cod_estado) REFERENCES tb_mesorregiao(nome, cod_uf);
        """))
        db.session.execute(text("""
            ALTER TABLE tb_instituicao 
            ADD CONSTRAINT tb_instituicao_microrregiao_cod_estado_fkey 
            FOREIGN KEY (microrregiao, cod_estado) REFERENCES tb_microrregiao(nome, cod_uf);
        """))
        db.session.commit()
        print("Constraints reativadas para tb_instituicao")
    except SQLAlchemyError:
        db.session.rollback()
        log_exception("Erro SQLAlchemy ao reativar as constraints de tb_instituicao")
    except Exception:
        db.session.rollback()
        log_exception("Erro inesperado ao reativar as constraints de tb_instituicao")

    # Sincroniza a sequência com o valor máximo do cod_entidade
    db.session.execute(text("SELECT setval('public.tb_instituicao_cod_entidade_seq', (SELECT MAX(cod_entidade) FROM tb_instituicao))"))
    db.session.commit()

    # 6. Inserir dados consolidados na tabela censo_escolar
    print("Populando tabela censo_escolar com dados consolidados...")

    try:
        db.session.execute(text("""
            INSERT INTO censo_escolar (ano_censo, estado, sigla, cod_estado, total_matriculas)
            SELECT
                i.ano_censo,
                u.nome as estado,
                u.sigla,
                u.cod_uf as cod_estado,
                COALESCE(SUM(i.qt_mat_bas), 0) as total_matriculas
            FROM tb_instituicao i
            JOIN tb_uf u ON i.cod_estado = u.cod_uf
            WHERE i.ano_censo = 2023
            GROUP BY i.ano_censo, u.nome, u.sigla, u.cod_uf
        """))
        
        db.session.execute(text("""
            INSERT INTO censo_escolar (ano_censo, estado, sigla, cod_estado, total_matriculas)
            SELECT
                i.ano_censo,
                u.nome as estado,
                u.sigla,
                u.cod_uf as cod_estado,
                COALESCE(SUM(i.qt_mat_bas), 0) as total_matriculas
            FROM tb_instituicao i
            JOIN tb_uf u ON i.cod_estado = u.cod_uf
            WHERE i.ano_censo = 2024
            GROUP BY i.ano_censo, u.nome, u.sigla, u.cod_uf
        """))
        
        db.session.commit()
        print("Tabela censo_escolar populada com sucesso.")

    except SQLAlchemyError as e:
        db.session.rollback()
        log_exception("Erro SQLAlchemy ao popular censo_escolar")
    except Exception:
        db.session.rollback()
        log_exception("Erro inesperado ao popular censo_escolar")

print("Banco inicializado com sucesso.")