import requests
from core.config import client_config as config


def authenticate(username, password):
    """
    Authenticate the user with the given username and password.
    """
    pass

BASE_URL = f"{config.server.host}:{config.server.port}"

def post(url, headers=None, *args, **kwargs):
    # auth_headers = authenticate(config.server.username, config.server.password)
    headers = headers or {}
    # headers.update(auth_headers)
    url = BASE_URL + url
    return requests.post(url, headers=headers,
                         auth=(config.server.username, config.server.password),
                         *args, **kwargs)

def get(url, params=None, headers=None, ):
    # auth_headers = authenticate(config.server.username, config.server.password)
    headers = headers or {}
    # headers.update(auth_headers)
    url = BASE_URL + url
    return requests.get(url, headers=headers, params=params
                        , auth=(config.server.username, config.server.password))

def delete(url, headers=None, *args, **kwargs):
    # auth_headers = authenticate(config.server.username, config.server.password)
    headers = headers or {}
    # headers.update(auth_headers)
    url = BASE_URL + url
    return requests.delete(url, headers=headers,
                           auth=(config.server.username, config.server.password),
                           *args, **kwargs)

def register_cups_client(body: dict):
    """
    Register the client with the given client_id.
    :param client_id:
    :return:
    """
    url = "/api/cups/task/register/printer-cli"
    return post(url, json=body)

def unregister_cups_client(client_id: str):
    pass

def fetch_all_requested_print_jobs():
    """
    Fetch all the requested print jobs from the server.
    """
    url = "/api/cups/task/jobs"
    return get(url)

def delete_requested_print_job(job_id: str):
    url = f"/api/v2/printjob/cancel"
    params = { "job_id": job_id}
    return delete(url, params=params)