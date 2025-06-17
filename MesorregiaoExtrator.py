import requests
import json

from helpers.logging import logger

url = "https://servicodados.ibge.gov.br/api/v1/localidades/mesorregioes"
resposta = requests.get(url)

if resposta.status_code == 200:
    todas_mesorregioes = resposta.json()
    mesorregioes_brasil = []

    for meso in todas_mesorregioes:
        nova_meso = {
            'cod_mesorregiao': meso['id'],
            'nome': meso['nome'],
            'UF': meso['UF']
        }
        mesorregioes_brasil.append(nova_meso)

    with open('mesorregioes_brasil.json', 'w', encoding='utf-8') as f:
        json.dump(mesorregioes_brasil, f, ensure_ascii=False, indent=2)

    logger.info("Mesorregiões do Brasil salvas em mesorregioes_brasil.json")
else:
    logger.error("Erro ao acessar a API:", resposta.status_code)
