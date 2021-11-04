import requests
import json

# Referências sobre o uso do requests:

# Fazendo requisições:
# https://docs.python-requests.org/en/master/user/quickstart/#make-a-request
# Usando JSON retornado:
# https://docs.python-requests.org/en/master/user/quickstart/#json-response-content

# Checar se o pacote existe, considerando ou não a versão
def version_exists(package_name, version):
    url_base = 'https://pypi.org/pypi'
    url = f"{url_base}/{package_name}/{version}/json"
    
    json_raw = requests.get(url)
    
    if json_raw.status_code == 404:
        return False
    return True

def latest_version(package_name):
    # TODO
    # Fazer requisição na API do PyPI para descobrir a última versão
    # de um pacote. Retornar None se o pacote não existir.
    
    url_base = 'https://pypi.org/pypi'
    url = f"{url_base}/{package_name}/json"
    
    json_raw = requests.get(url)
    
    if json_raw.status_code == 404:
        return None
    
    json = json_raw.json()
    ultima_versao = json['info']['version']
    
    return ultima_versao
