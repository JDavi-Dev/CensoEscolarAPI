import requests
import json

from helpers.logging import logger

url = "https://servicodados.ibge.gov.br/api/v1/localidades/microrregioes"
resposta = requests.get(url)

if resposta.status_code == 200:
    microrregioes = resposta.json()
    microrregioes_nordeste = [
        micro for micro in microrregioes
        if micro['mesorregiao']['UF']['regiao']['id'] == 2
    ]
    for i, micro in enumerate(microrregioes_nordeste):
        novo_micro = {
            'cod_microrregiao': micro['id'],
            'nome': micro['nome'],
            'mesorregiao': micro['mesorregiao']
        }
        microrregioes_nordeste[i] = novo_micro
    with open('microrregioes_nordeste.json', 'w', encoding='utf-8') as f:
        json.dump(microrregioes_nordeste, f, ensure_ascii=False, indent=2)
    logger.info("Microrregiões do Nordeste salvas em microrregioes_nordeste.json")
else:
    logger.error("Erro ao acessar a API:", resposta.status_code)