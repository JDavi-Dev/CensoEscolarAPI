# import requests
# import json

# url = "https://servicodados.ibge.gov.br/api/v1/localidades/mesorregioes"
# resposta = requests.get(url)

# dados_mesorregioes = []

# if resposta.status_code == 200:
#     mesorregioes = resposta.json()
#     for meso in mesorregioes:
#         if meso['UF']['regiao']['id'] == 2:  # Nordeste
#             dados_mesorregioes.append({
#                 'id': meso['id'],
#                 'nome': meso['nome']
#             })

# with open('mesorregioes_nordeste.json', 'w', encoding='utf-8') as f:
#     json.dump(dados_mesorregioes, f, ensure_ascii=False, indent=2)

# print("Mesorregiões do Nordeste salvas em mesorregioes_nordeste.json")


# Com todos os campos #

# import requests
# import json

# url = "https://servicodados.ibge.gov.br/api/v1/localidades/mesorregioes"
# resposta = requests.get(url)

# if resposta.status_code == 200:
#     todas_mesorregioes = resposta.json()
#     mesorregioes_nordeste = [
#         meso for meso in todas_mesorregioes
#         if meso['UF']['regiao']['id'] == 2
#     ]
#     with open('mesorregioes_nordeste.json', 'w', encoding='utf-8') as f:
#         json.dump(mesorregioes_nordeste, f, ensure_ascii=False, indent=2)
#     print("Mesorregiões do Nordeste salvas em mesorregioes_nordeste.json")
# else:
#     print("Erro ao acessar a API:", resposta.status_code)

# Renomeado id #

import requests
import json

url = "https://servicodados.ibge.gov.br/api/v1/localidades/mesorregioes"
resposta = requests.get(url)

if resposta.status_code == 200:
    todas_mesorregioes = resposta.json()
    mesorregioes_nordeste = []

    for meso in todas_mesorregioes:
        if meso['UF']['regiao']['id'] == 2:  # Nordeste
            nova_meso = {
                'cod_mesorregiao': meso['id'],
                'nome': meso['nome'],
                'UF': meso['UF']
            }
            mesorregioes_nordeste.append(nova_meso)

    with open('mesorregioes_nordeste.json', 'w', encoding='utf-8') as f:
        json.dump(mesorregioes_nordeste, f, ensure_ascii=False, indent=2)

    print("Mesorregiões do Nordeste salvas em mesorregioes_nordeste.json")
else:
    print("Erro ao acessar a API:", resposta.status_code)
