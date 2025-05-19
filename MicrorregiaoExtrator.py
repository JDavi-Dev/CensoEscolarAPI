# import requests
# import json

# url = "https://servicodados.ibge.gov.br/api/v1/localidades/microrregioes"
# resposta = requests.get(url)

# dados_microrregioes = []

# if resposta.status_code == 200:
#     microrregioes = resposta.json()
#     for micro in microrregioes:
#         if micro['mesorregiao']['UF']['regiao']['id'] == 2:  # Nordeste
#             dados_microrregioes.append({
#                 'id': micro['id'],
#                 'nome': micro['nome']
#             })

# with open('microrregioes_nordeste.json', 'w', encoding='utf-8') as f:
#     json.dump(dados_microrregioes, f, ensure_ascii=False, indent=2)

# print("Microrregiões do Nordeste salvas em microrregioes_nordeste.json")


# Com todos os campos #

# import requests
# import json

# url = "https://servicodados.ibge.gov.br/api/v1/localidades/microrregioes"
# resposta = requests.get(url)

# if resposta.status_code == 200:
#     todas_microrregioes = resposta.json()
#     microrregioes_nordeste = [
#         micro for micro in todas_microrregioes
#         if micro['mesorregiao']['UF']['regiao']['id'] == 2
#     ]
#     with open('microrregioes_nordeste.json', 'w', encoding='utf-8') as f:
#         json.dump(microrregioes_nordeste, f, ensure_ascii=False, indent=2)
#     print("Microrregiões do Nordeste salvas em microrregioes_nordeste.json")
# else:
#     print("Erro ao acessar a API:", resposta.status_code)

# Renomeado id # 

import requests
import json

url = "https://servicodados.ibge.gov.br/api/v1/localidades/microrregioes"
resposta = requests.get(url)

if resposta.status_code == 200:
    microrregioes = resposta.json()
    # Filtrar apenas microrregiões da região Nordeste (id regiao == 2)
    microrregioes_nordeste = [
        micro for micro in microrregioes
        if micro['mesorregiao']['UF']['regiao']['id'] == 2
    ]
    # Renomear 'id' para 'cod_microrregiao' e colocar no início
    for i, micro in enumerate(microrregioes_nordeste):
        novo_micro = {
            'cod_microrregiao': micro['id'],
            'nome': micro['nome'],
            'mesorregiao': micro['mesorregiao']
        }
        microrregioes_nordeste[i] = novo_micro
    with open('microrregioes_nordeste.json', 'w', encoding='utf-8') as f:
        json.dump(microrregioes_nordeste, f, ensure_ascii=False, indent=2)
    print("Microrregiões do Nordeste salvas em microrregioes_nordeste.json")
else:
    print("Erro ao acessar a API:", resposta.status_code)