import requests
import ratelimit
from typing import Union
from NaStyAPI import APICall

userAgent = APICall.userAgent
# Possibly make a wrapper
@ratelimit.sleep_and_retry
@ratelimit.limits(calls=1, period=30)
def send_telegram(client: str, tgid: Union[str, int], key: str, to: str) -> str:
    """Sends a non-recruitment telegram through the NationStatesAPI.

    Non-recruitment telegrams are limited to only one per 30 seconds, and this method enforces it.
    It is recommended to keep those variables a secret as their exposure can lead to abuse.

    :param client: This is the client key that should be used, this represents the reason for access in most cases, such as a regional client key.
    :param tgid: This is the unique identifier of the telegram template that should be sent.
    :param key: This is the telegram key that represents the sender of the telegram.
    :param to: The name of the receiver of the telegram.
    :param get_request: Should the request object be returned or the content it contains.
    """
    headers = {"User-Agent": userAgent}
    parameters = {"a": "sendTG", "client": client, "tgid": tgid, "key": key, "to": to}
    res = requests.get("https://www.nationstates.net/cgi-bin/api.cgi", params=parameters, headers=headers)
    return res.content.decode()


@ratelimit.sleep_and_retry
@ratelimit.limits(calls=1, period=180)
def send_recruitment_telegram(client: str, tgid: Union[str, int], key: str, to: str) -> str:
    """Sends a recruitment telegram through the NationStatesAPI.

    Recruitment telegrams are limited to only one per 180 seconds, and this method enforces it.

    :param client: This is the client key that should be used, this represents the reason for access in most cases, such as a regional client key.
    :param tgid: This is the unique identifier of the telegram template that should be sent.
    :param key: This is the telegram key that represents the sender of the telegram.
    :param to: The name of the receiver of the telegram.
    :param get_request: Should the request object be returned or the content it contains.
    """
    headers = {"User-Agent": userAgent}
    parameters = {"a": "sendTG", "client": client, "tgid": tgid, "key": key, "to": to}
    res = requests.get("https://www.nationstates.net/cgi-bin/api.cgi", params=parameters, headers=headers)
    return res.content.decode()
