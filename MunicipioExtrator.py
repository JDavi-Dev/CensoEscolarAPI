import requests
import json

from helpers.logging import logger

url = "https://servicodados.ibge.gov.br/api/v1/localidades/regioes/2/municipios"
resposta = requests.get(url)

if resposta.status_code == 200:
    municipios = resposta.json()
    for i, mun in enumerate(municipios):
        novo_mun = {
            'cod_municipio': mun['id'],
            'nome': mun['nome'],
            'microrregiao': mun['microrregiao']
        }
        municipios[i] = novo_mun
    with open('municipios_nordeste.json', 'w', encoding='utf-8') as f:
        json.dump(municipios, f, ensure_ascii=False, indent=2)
    logger.info("Municípios do Nordeste salvos em municipios_nordeste.json")
else:
    logger.error("Erro ao acessar a API:", resposta.status_code)