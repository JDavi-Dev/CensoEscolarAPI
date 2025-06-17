import requests
import json

from helpers.logging import logger

url = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios"
resposta = requests.get(url)

if resposta.status_code == 200:
    municipios = resposta.json()
    municipios_brasil = []

    for mun in municipios:
        microrregiao = mun.get('microrregiao')
        if not microrregiao:
            logger.warning(f"Município {mun['nome']} (ID: {mun['id']}) sem microrregião. Pulando...")
            continue

        mesorregiao = microrregiao.get('mesorregiao')
        if not mesorregiao:
            logger.warning(f"Microrregião do município {mun['nome']} (ID: {mun['id']}) sem mesorregião. Pulando...")
            continue
        
        novo_mun = {
            'cod_municipio': mun['id'],
            'nome': mun['nome'],
            'microrregiao': mun['microrregiao']
        }
        municipios_brasil.append(novo_mun)

    with open('municipios_brasil.json', 'w', encoding='utf-8') as f:
        json.dump(municipios_brasil, f, ensure_ascii=False, indent=2)
    logger.info("Municípios do Brasil salvos em municipios_brasil.json")
else:
    logger.error("Erro ao acessar a API:", resposta.status_code)