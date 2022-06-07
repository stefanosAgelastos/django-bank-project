import requests


def entity_authenticate(entity):
    base_url = entity.api_url
    url = f'{base_url}/rest-auth/'
    creds = {
        'username': entity.api_username,
        'password': entity.api_password
    }
    resp = requests.post(url, data=creds)
    data = resp.json()
    return data['token'], base_url


def check_account(entity, account_id):
    token, base_url = entity_authenticate(entity)
    url = f'{base_url}/account/{account_id}'
    headers = {"Authorization": f'Token {token}',
               'content-type': 'application/json'}
    resp = requests.get(url, headers=headers)
    return resp.ok
