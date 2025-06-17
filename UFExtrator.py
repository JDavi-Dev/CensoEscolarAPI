import requests
import json

from helpers.logging import logger

url = "https://servicodados.ibge.gov.br/api/v1/localidades/estados"
resposta = requests.get(url)

if resposta.status_code == 200:
    ufs = resposta.json()
    ufs_brasil = []

    for uf in ufs:
        novo_uf = {
            'cod_uf': uf['id'],
            'sigla': uf['sigla'],
            'nome': uf['nome'],
            'regiao': uf['regiao']['nome']
        }
        ufs_brasil.append(novo_uf)

    with open('ufs_brasil.json', 'w', encoding='utf-8') as f:
        json.dump(ufs_brasil, f, ensure_ascii=False, indent=2)
    logger.info("UFs do Brasil salvas em ufs_brasil.json")
else:
    logger.error("Erro ao acessar a API:", resposta.status_code)