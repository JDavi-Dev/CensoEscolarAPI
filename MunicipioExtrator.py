# import requests
# import json

# url = "https://servicodados.ibge.gov.br/api/v1/localidades/regioes/2/municipios"
# resposta = requests.get(url)

# dados_municipios = []

# if resposta.status_code == 200:
#     municipios = resposta.json()
#     for municipio in municipios:
#         dados_municipios.append({
#             'id': municipio['id'],
#             'nome': municipio['nome']
#         })

# with open('municipios_nordeste.json', 'w', encoding='utf-8') as f:
#     json.dump(dados_municipios, f, ensure_ascii=False, indent=2)

# print("Municípios do Nordeste salvos em municipios_nordeste.json")


# Com todos os campos #

# import requests
# import json

# url = "https://servicodados.ibge.gov.br/api/v1/localidades/regioes/2/municipios"
# resposta = requests.get(url)

# if resposta.status_code == 200:
#     dados_municipios = resposta.json()
#     with open('municipios_nordeste.json', 'w', encoding='utf-8') as f:
#         json.dump(dados_municipios, f, ensure_ascii=False, indent=2)
#     print("Municípios do Nordeste salvos em municipios_nordeste.json")
# else:
#     print("Erro ao acessar a API:", resposta.status_code)

# Renomeado id #

import requests
import json

url = "https://servicodados.ibge.gov.br/api/v1/localidades/regioes/2/municipios"
resposta = requests.get(url)

if resposta.status_code == 200:
    municipios = resposta.json()
    # Renomear 'id' para 'cod_municipio' e colocar no início
    for i, mun in enumerate(municipios):
        novo_mun = {
            'cod_municipio': mun['id'],
            'nome': mun['nome'],
            'microrregiao': mun['microrregiao']
        }
        municipios[i] = novo_mun
    with open('municipios_nordeste.json', 'w', encoding='utf-8') as f:
        json.dump(municipios, f, ensure_ascii=False, indent=2)
    print("Municípios do Nordeste salvos em municipios_nordeste.json")
else:
    print("Erro ao acessar a API:", resposta.status_code)