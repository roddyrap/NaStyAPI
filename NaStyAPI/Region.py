import requests
from typing import Union, List
from .APICall import call_api
userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"


def get_regions():
    headers = {
        "User-Agent": userAgent}
    res = requests.get("https://www.nationstates.net/pages/regions.xml.gz", headers=headers)
    return res.content


def get_shards(nation_name: str, shards: Union[List[str], str]) -> str:
    if type(shards) is str:
        shards = [shards]
    payloads = {"region": nation_name, "q": "+".join(shards)}
    headers = {
        "User-Agent": userAgent}
    res = call_api(parameters=payloads, headers=headers)
    return str(res.content)
