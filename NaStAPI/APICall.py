import requests
from typing import Dict
userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"


# TODO: Add rate limit
def call_api(headers: Dict[str, str], parameters: Dict[str, str]) -> requests.request:
    headers["User-Agent"] = userAgent
    return requests.get("https://www.nationstates.net/cgi-bin/api.cgi", parameters=parameters, headers=headers)