from requests.structures import CaseInsensitiveDict

from constants import notion_secret, rapid_api_host, rapid_api_key


def init_headers():
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = f"Bearer {notion_secret}"
    headers["Notion-Version"] = "2021-05-13"
    headers["Content-Type"] = "application/json"
    return headers

def init_headers_convert_currency():
    headers = CaseInsensitiveDict()
    headers['X-RapidAPI-Key'] = rapid_api_key
    headers['X-RapidAPI-Host'] = rapid_api_host
    return headers