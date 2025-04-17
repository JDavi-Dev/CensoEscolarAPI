from flask import Flask, jsonify, request, abort
import json

app = Flask(__name__)

# Carregar dados do arquivo JSON
def load_data():
    with open('censo_pb_pe_rn_2024.json', 'r') as file:
        return json.load(file)

# Salvar dados no arquivo JSON
def save_data(data):
    with open('censo_pb_pe_rn_2024.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

# Listar todas as instituições
@app.route('/instituicoesensino', methods=['GET'])
def get_instituicoes():
    instituicoes = load_data()
    return jsonify(instituicoes)

# Recuperar instituição pelo código da instituição de ensino
@app.route('/instituicoesensino/<string:co_instituicao>', methods=['GET'])
def get_instituicao(co_instituicao):
    instituicoes = load_data()
    for instituicao in instituicoes:
        if instituicao['co_instituicao'] == co_instituicao:
            return jsonify(instituicao)
    abort(404)

# Inserir instituição através do json enviado na requisição
@app.route('/instituicoesensino', methods=['POST'])
def add_instituicao():
    new_instituicao = request.json
    instituicoes = load_data()
    instituicoes.append(new_instituicao)
    save_data(instituicoes)
    return jsonify(new_instituicao), 201

# Atualizar instituição através do json enviado na requisição
@app.route('/instituicoesensino/<string:co_instituicao>', methods=['PUT'])
def update_instituicao(co_instituicao):
    updated_data = request.json
    instituicoes = load_data()

    for i, instituicao in enumerate(instituicoes):
        if instituicao['co_instituicao'] == co_instituicao:
            # Garante que o campo co_instituicao continue correto
            updated_data['co_instituicao'] = co_instituicao
            instituicoes[i] = updated_data
            save_data(instituicoes)
            return jsonify(updated_data)

    abort(404)

# Remover instituição pelo código da instituição de ensino
@app.route('/instituicoesensino/<string:co_instituicao>', methods=['DELETE'])
def delete_instituicao(co_instituicao):
    instituicoes = load_data()
    for i, instituicao in enumerate(instituicoes):
        if instituicao['co_instituicao'] == co_instituicao:
            del instituicoes[i]
            save_data(instituicoes)
            return jsonify({'message': 'Instituição removida com sucesso.'})
    
    abort(404)

if __name__ == '__main__':
    app.run()
