from requests.structures import CaseInsensitiveDict

from constants import notion_secret


def init_headers():
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = f"Bearer {notion_secret}"
    headers["Notion-Version"] = "2021-05-13"
    headers["Content-Type"] = "application/json"
    return headers