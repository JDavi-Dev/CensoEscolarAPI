import requests
import json

from helpers.logging import logger

url = "https://servicodados.ibge.gov.br/api/v1/localidades/regioes/2/estados"
resposta = requests.get(url)

if resposta.status_code == 200:
    ufs = resposta.json()
    for i, uf in enumerate(ufs):
        novo_uf = {
            'cod_uf': uf['id'],
            'sigla': uf['sigla'],
            'nome': uf['nome'],
            'regiao': uf['regiao']['nome']
        }
        ufs[i] = novo_uf
    with open('ufs_nordeste.json', 'w', encoding='utf-8') as f:
        json.dump(ufs, f, ensure_ascii=False, indent=2)
    logger.info("UFs do Nordeste salvas em ufs_nordeste.json")
else:
    logger.error("Erro ao acessar a API:", resposta.status_code)