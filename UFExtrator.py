import requests
import json

url = "https://servicodados.ibge.gov.br/api/v1/localidades/regioes/2/estados"
resposta = requests.get(url)

if resposta.status_code == 200:
    ufs = resposta.json()
    # Renomear 'id' para 'cod_uf' e colocar no início
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
    print("UFs do Nordeste salvas em ufs_nordeste.json")
else:
    print("Erro ao acessar a API:", resposta.status_code)