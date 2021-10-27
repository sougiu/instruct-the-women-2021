import requests
import json

# Referências sobre o uso do requests:

# Fazendo requisições:
# https://docs.python-requests.org/en/master/user/quickstart/#make-a-request
# Usando JSON retornado:
# https://docs.python-requests.org/en/master/user/quickstart/#json-response-content

# Checar se o pacote existe, considerando ou não a versão
def version_exists(package_name, version):
    dados_pacote = requests.get(f"https://pypi.org/pypi/{package_name}/{version}/json")
    if dados_pacote:
        return True
    else:
        return False

def latest_version(package_name):
    # TODO
    # Fazer requisição na API do PyPI para descobrir a última versão
    # de um pacote. Retornar None se o pacote não existir.

    dados_pacote = requests.get(f"https://pypi.odados_pacoteg/pypi/{package_name}/json")
    if dados_pacote.status_code == 404:
        return "None"
    else:
        dados_pacote = dados_pacote.json()
        return list(dados_pacote['releases'].keys())[-1]
