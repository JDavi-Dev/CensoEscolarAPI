import requests
import json

from helpers.logging import logger

url = "https://servicodados.ibge.gov.br/api/v1/localidades/microrregioes"
resposta = requests.get(url)

if resposta.status_code == 200:
    microrregioes = resposta.json()
    microrregioes_brasil = []
    
    for micro in microrregioes:
        novo_micro = {
            'cod_microrregiao': micro['id'],
            'nome': micro['nome'],
            'mesorregiao': micro['mesorregiao']
        }
        microrregioes_brasil.append(novo_micro)

    with open('microrregioes_brasil.json', 'w', encoding='utf-8') as f:
        json.dump(microrregioes_brasil, f, ensure_ascii=False, indent=2)
    logger.info("Microrregiões do Brasil salvas em microrregioes_brasil.json")
else:
    logger.error("Erro ao acessar a API:", resposta.status_code)