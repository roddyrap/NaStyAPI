import requests
from typing import Union, List
from .APICall import call_api
import gzip


def get_regions() -> str:
    """Gets the daily data dump of all the nations. The generated file is quite large, so long wait times may occur."""
    res = requests.get("https://www.nationstates.net/pages/regions.xml.gz")
    return gzip.decompress(res.content)


def get_shards(nation_name: str, shards: Union[List[str], str] = None) -> str:
    if type(shards) is str:
        shards = [shards]
    elif shards is None:
        shards = []
    payloads = {"region": nation_name, "q": "+".join(shards)}
    res = call_api(parameters=payloads)
    return res.content.decode()
