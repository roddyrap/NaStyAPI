import requests
from typing import Dict
import ratelimit
# TODO: Get actual userAgent
userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"


def set_user_agent(new_user_agent):
    global userAgent
    userAgent = new_user_agent


@ratelimit.sleep_and_retry
@ratelimit.limits(calls=50, period=30)
def call_api(headers: Dict[str, str] = None, parameters: Dict[str, str] = None, base_url="https://www.nationstates.net/cgi-bin/api.cgi") -> requests.request:
    if parameters is None:
        parameters = {}
    if headers is None:
        headers = {}
    headers["User-Agent"] = userAgent
    return requests.get(base_url, params=parameters, headers=headers)
