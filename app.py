from flask import Flask, request, jsonify
import sqlite3
from models.InstituicaoEnsino import InstituicaoEnsino

app = Flask(__name__)

@app.get("/instituicoes")
def instituicoesResource():
    print("Get - Instituições")
    
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))

    try:
        instituicoesEnsino = []
        conn = sqlite3.connect('censo_escolar.db')
        cursor = conn.cursor()

        # Calcular o offset para a consulta
        offset = (page - 1) * per_page

        cursor.execute('SELECT * FROM tb_instituicao LIMIT ? OFFSET ?', (per_page, offset))
        resultSet = cursor.fetchall()

        for row in resultSet:
            instituicaoEnsino = InstituicaoEnsino(
                id_instituicao=row[0],
                regiao=row[1],
                cod_regiao=row[2],
                estado=row[3],
                sigla=row[4],
                cod_estado=row[5],
                municipio=row[6],
                cod_municipio=row[7],
                mesorregiao=row[8],
                cod_mesorregiao=row[9],
                microrregiao=row[10],
                cod_microrregiao=row[11],
                entidade=row[12],
                cod_entidade=row[13],
                qt_mat_bas=row[14]
            )
            instituicoesEnsino.append(instituicaoEnsino.toDict())

    except sqlite3.Error as e:
        return jsonify({"mensagem": "Problema com o banco de dados."}), 500
    finally:
        conn.close()

    return jsonify(instituicoesEnsino), 200


def validarInstituicao(content):
    isValido = True
    if (len(content['entidade']) < 3 or content['entidade'].isdigit()):
        isValido = False
    if (not (content['cod_entidade'].isdigit())):
        isValido = False
    if (not (content['qt_mat_bas'].isdigit())):
        isValido = False
    return isValido

@app.post("/instituicoes")
def instituicaoInsercaoResource():
    print("Post - Instituição")
    instituicaoJson = request.get_json()
    isValido = validarInstituicao(instituicaoJson)
    if isValido:
        conn = sqlite3.connect('censo_escolar.db')
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO tb_instituicao (regiao, cod_regiao, estado, sigla, cod_estado, municipio, cod_municipio, mesorregiao, cod_mesorregiao, microrregiao, cod_microrregiao, entidade, cod_entidade, qt_mat_bas) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', 
            (instituicaoJson['regiao'], instituicaoJson['cod_regiao'], instituicaoJson['estado'], instituicaoJson['sigla'], instituicaoJson['cod_estado'], 
             instituicaoJson['municipio'], instituicaoJson['cod_municipio'], instituicaoJson['mesorregiao'], instituicaoJson['cod_mesorregiao'], 
             instituicaoJson['microrregiao'], instituicaoJson['cod_microrregiao'], instituicaoJson['entidade'], instituicaoJson['cod_entidade'], 
             instituicaoJson['qt_mat_bas'])
        )
        conn.commit()
        id_instituicao = cursor.lastrowid
        instituicaoEnsino = InstituicaoEnsino(
            id_instituicao, 
            instituicaoJson['regiao'], 
            instituicaoJson['cod_regiao'], 
            instituicaoJson['estado'], 
            instituicaoJson['sigla'], 
            instituicaoJson['cod_estado'], 
            instituicaoJson['municipio'], 
            instituicaoJson['cod_municipio'], 
            instituicaoJson['mesorregiao'], 
            instituicaoJson['cod_mesorregiao'], 
            instituicaoJson['microrregiao'], 
            instituicaoJson['cod_microrregiao'], 
            instituicaoJson['entidade'], 
            instituicaoJson['cod_entidade'], 
            instituicaoJson['qt_mat_bas']
        )
        conn.close()
        return jsonify(instituicaoEnsino.toDict()), 200

    return jsonify({"mensagem": "Não cadastrado"}), 406

@app.route("/instituicoes/<int:cod_entidade>", methods=["DELETE"])
def instituicaoRemocaoResource(cod_entidade):
    print("Delete - Instituição")
    try:
        conn = sqlite3.connect('censo_escolar.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tb_instituicao WHERE cod_entidade = ?', (cod_entidade,))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"mensagem": "Instituição não encontrada."}), 404
    except sqlite3.Error as e:
        return jsonify({"mensagem": "Problema com o banco de dados."}), 500
    finally:
        conn.close()
    return jsonify({"mensagem": "Instituição removida com sucesso."}), 200

@app.route("/instituicoes/<int:cod_entidade>", methods=["PUT"])
def instituicaoAtualizacaoResource(cod_entidade):
    print("Put - Instituição")
    try:
        conn = sqlite3.connect('censo_escolar.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tb_instituicao WHERE cod_entidade = ?', (cod_entidade,))
        row = cursor.fetchone()

        if row is None:
            return jsonify({"mensagem": "Instituição não encontrada."}), 404

        instituicaoJson = request.get_json()
        isValido = validarInstituicao(instituicaoJson)
        if not isValido:
            return jsonify({"mensagem": "Dados inválidos."}), 406

        cursor.execute('UPDATE tb_instituicao SET regiao = ?, cod_regiao = ?, estado = ?, sigla = ?, cod_estado = ?, municipio = ?, cod_municipio = ?, mesorregiao = ?, cod_mesorregiao = ?, microrregiao = ?, cod_microrregiao = ?, entidade = ?, cod_entidade = ?, qt_mat_bas = ? WHERE cod_entidade = ?',
                       (instituicaoJson['regiao'], instituicaoJson['cod_regiao'], instituicaoJson['estado'], instituicaoJson['sigla'], instituicaoJson['cod_estado'], 
                        instituicaoJson['municipio'], instituicaoJson['cod_municipio'], instituicaoJson['mesorregiao'], instituicaoJson['cod_mesorregiao'], 
                        instituicaoJson['microrregiao'], instituicaoJson['cod_microrregiao'], instituicaoJson['entidade'], instituicaoJson['cod_entidade'], 
                        instituicaoJson['qt_mat_bas'], cod_entidade))
        conn.commit()

    except sqlite3.Error as e:
        return jsonify({"mensagem": "Problema com o banco de dados."}), 500
    finally:
        conn.close()

    return jsonify({"mensagem": "Instituição atualizada com sucesso."}), 200

@app.route("/instituicoes/<int:cod_entidade>", methods=["GET"])
def instituicoesByCodEntidadeResource(cod_entidade):
    try:
        conn = sqlite3.connect('censo_escolar.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tb_instituicao WHERE cod_entidade = ?', (cod_entidade,))
        row = cursor.fetchone()

        if row is None:
            return jsonify({"mensagem": "Instituição não encontrada."}), 404

        instituicaoEnsino = InstituicaoEnsino(
            id_instituicao=row[0],
            regiao=row[1],
            cod_regiao=row[2],
            estado=row[3],
            sigla=row[4],
            cod_estado=row[5],
            municipio=row[6],
            cod_municipio=row[7],
            mesorregiao=row[8],
            cod_mesorregiao=row[9],
            microrregiao=row[10],
            cod_microrregiao=row[11],
            entidade=row[12],
            cod_entidade=row[13],
            qt_mat_bas=row[14]
        )

    except sqlite3.Error as e:
        return jsonify({"mensagem": "Problema com o banco de dados."}), 500
    finally:
        conn.close()

    return jsonify(instituicaoEnsino.toDict()), 200
