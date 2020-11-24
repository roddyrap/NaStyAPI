import requests
from typing import Union, List
from .APICall import call_api
userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"


def get_shards(shards: Union[List[str], str], get_request: bool = False) -> Union[bytes, requests.request]:
    if type(shards) is str:
        shards = [shards]
    payloads = {"q": "+".join(shards)}
    headers = {
        "User-Agent": userAgent}
    res = call_api(parameters=payloads, headers=headers)
    return res if get_request else res.content
