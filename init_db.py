import json
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
from models.CensoEscolar import CensoEscolar
from datetime import datetime

print("Iniciando a criação e população do banco de dados...")

with app.app_context():
    
    print("Dropando todas as tabelas existentes (se houver)...")
    db.drop_all()

    print("Criando tabelas a partir dos modelos SQLAlchemy...")
    db.create_all()

    # --- Inserção de dados ---

    # 2. Inserir UFs
    print("Populando tabela tb_uf...")
    with open("data/ufs_brasil.json", "r", encoding="utf-8") as f:
        ufs_data = json.load(f)
    ufs_to_add = []
    for uf_item in ufs_data:
        uf_obj = UF(
            uf_item['cod_uf'],
            uf_item['sigla'],
            uf_item['nome'],
            uf_item['regiao']
        )
        ufs_to_add.append(uf_obj)
    db.session.bulk_save_objects(ufs_to_add)
    db.session.commit()
    print(f"Inseridos {len(ufs_to_add)} UFs.")

    # 3. Inserir Mesorregiões
    print("Populando tabela tb_mesorregiao...")
    with open("data/mesorregioes_brasil.json", "r", encoding="utf-8") as f:
        mesor_data = json.load(f)
    mesor_to_add = []
    for m_item in mesor_data:
        mesor_obj = Mesorregiao(
            m_item['cod_mesorregiao'],
            m_item['nome'],
            m_item['UF']['id']
        )
        mesor_to_add.append(mesor_obj)
    db.session.bulk_save_objects(mesor_to_add)
    db.session.commit()
    print(f"Inseridas {len(mesor_to_add)} Mesorregiões.")

    # 4. Inserir Microrregiões
    print("Populando tabela tb_microrregiao...")
    with open("data/microrregioes_brasil.json", "r", encoding="utf-8") as f: #
        micros_data = json.load(f)
    micros_to_add = []
    for micro_item in micros_data:
        micror_obj = Microrregiao(
            micro_item['cod_microrregiao'],
            micro_item['nome'],
            micro_item['mesorregiao']['id'],
            micro_item['mesorregiao']['UF']['id']
        )
        micros_to_add.append(micror_obj)
    db.session.bulk_save_objects(micros_to_add)
    db.session.commit()
    print(f"Inseridas {len(micros_to_add)} Microrregiões.")

    # 5. Inserir Municípios
    print("Populando tabela tb_municipio...")
    with open("data/municipios_brasil.json", "r", encoding="utf-8") as f:
        munis_data = json.load(f)
    
    muni_to_add = []
    skipped_munis = 0
    for mun_item in munis_data:
        microrregiao = mun_item.get('microrregiao') 
        mesorregiao = microrregiao.get('mesorregiao')

        muni_obj = Municipio(
            mun_item['cod_municipio'],
            mun_item['nome'],
            microrregiao['id'],
            mesorregiao['id'],
            mesorregiao['UF']['id']
        )
        muni_to_add.append(muni_obj)
    
    # Inserção em massa de municípios
    db.session.bulk_save_objects(muni_to_add)
    db.session.commit()
    print(f"Inseridos {len(muni_to_add)} municípios. {skipped_munis} municípios pulados.")    

    # 6. Inserir Instituições - OTIMIZADO (Métodos 1, 2 e 3)
    censo_files = ["data/censo_escolar_2023.json", "data/censo_escolar_2024.json"]

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

    for censo_file in censo_files:
        print(f"Processando arquivo: {censo_file}")

        with open(censo_file, "r", encoding="utf-8") as f:
            insts_json = json.load(f)

        inst_objects = []
        for inst in insts_json:
            inst_objects.append(Instituicao(
                ano_censo=inst['ano_censo'],
                regiao=inst['regiao'],
                cod_regiao=inst['cod_regiao'],
                estado=inst['estado'],
                sigla=inst['sigla'],
                cod_estado=inst['cod_estado'],
                municipio=inst['municipio'],
                cod_municipio=inst['cod_municipio'],
                mesorregiao=inst['mesorregiao'],
                microrregiao=inst['microrregiao'],
                entidade=inst.get('entidade'),
                cod_entidade=inst.get('cod_entidade'),
                qt_mat_bas=inst.get('qt_mat_bas') or 0
            ))

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

    # 7. Inserir dados consolidados na tabela censo_escolar
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