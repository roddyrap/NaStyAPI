import requests
from typing import Union, List
from .APICall import call_api

def get_shards(shards: Union[List[str], str]) -> str:
    if type(shards) is str:
        shards = [shards]
    payloads = {"q": "+".join(shards)}
    res = call_api(parameters=payloads)
    return res.content.decode()
