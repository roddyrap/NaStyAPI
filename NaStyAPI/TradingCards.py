import requests
from typing import Union, List
from .APICall import call_api


def get_trading_cards(season_number: int, get_request: bool = False) -> Union[bytes, requests.request]:
    res = call_api(base_url=f"https://www.nationstates.net/pages/cardlist_S{season_number}.xml.gz")
    return res if get_request else res.content


def get_info_on_card(card_name: str, shards: Union[List[str], str]) -> str:
    if type(shards) is str:
        shards = [shards]
    shards = ["card"] + shards
    payloads = {"card": card_name, "q": "+".join(shards)}
    res = call_api(payloads=payloads)
    return str(res.content)
