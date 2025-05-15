import requests
import json

url = "https://servicodados.ibge.gov.br/api/v1/localidades/regioes/2/estados"
resposta = requests.get(url)

dados_ufs = []

if resposta.status_code == 200:
    ufs = resposta.json()
    for uf in ufs:
        dados_ufs.append({
            'id': uf['id'],
            'sigla': uf['sigla'],
            'nome': uf['nome']
        })

with open('ufs_nordeste.json', 'w', encoding='utf-8') as f:
    json.dump(dados_ufs, f, ensure_ascii=False, indent=2)

print("UFs do Nordeste salvas em ufs_nordeste.json")

# Ufs: https://servicodados.ibge.gov.br/api/v1/localidades/regioes/2/estados
# Municipios: https://servicodados.ibge.gov.br/api/v1/localidades/regioes/2/municipios


# Com todos os campos #

# import requests
# import json

# url = "https://servicodados.ibge.gov.br/api/v1/localidades/regioes/2/estados"
# resposta = requests.get(url)

# if resposta.status_code == 200:
#     dados_ufs = resposta.json()
#     with open('ufs_nordeste.json', 'w', encoding='utf-8') as f:
#         json.dump(dados_ufs, f, ensure_ascii=False, indent=2)
#     print("UFs do Nordeste salvas em ufs_nordeste.json")
# else:
#     print("Erro ao acessar a API:", resposta.status_code)