import requests
import ratelimit
from typing import Union
userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"


# Possibly make a wrapper
@ratelimit.sleep_and_retry
@ratelimit.limits(calls=1, period=30)
def send_telegram(client: str, tgid: str, key: str, to: str, get_request: bool = False) -> Union[bytes, requests.request]:
    headers = {"User-Agent": userAgent}
    parameters = {"a": "sendTG", "client": client, "tgid": tgid, "key": key, "to": to}
    res = requests.get("https://www.nationstates.net/cgi-bin/api.cgi", params=parameters, headers=headers)
    return res if get_request else res.content


@ratelimit.sleep_and_retry
@ratelimit.limits(calls=1, period=180)
def send_recruitment_telegram(client: str, tgid: str, key: str, to: str, get_request: bool = False) -> Union[bytes, requests.request]:
    headers = {"User-Agent": userAgent}
    parameters = {"a": "sendTG", "client": client, "tgid": tgid, "key": key, "to": to}
    res = requests.get("https://www.nationstates.net/cgi-bin/api.cgi", params=parameters, headers=headers)
    return res if get_request else res.content