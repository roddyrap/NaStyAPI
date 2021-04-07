import requests
from typing import Union, List
from .APICall import call_api


def get_trading_cards(season_number: int, get_request:  bool = False) -> Union[bytes, requests.request]:
    res = call_api(base_url=f"https://www.nationstates.net/pages/cardlist_S{season_number}.xml.gz")
    return res if get_request else res.content


def get_info_on_card(card_id: Union[str, int], season, shards: Union[List[str], str], get_response=False) -> Union[str, requests.request]:
    if type(shards) is str:
        shards = [shards]
    shards = ["card"] + shards
    payloads = {"q": "card+" + "+".join(shards), "cardid": card_id, "season": season}
    res = call_api(parameters=payloads)
    return res if get_response else str(res.content)


def get_deck_information(identifier: Union[str, int], shards: Union[str, List[str]] = None, get_response=False) -> Union[str, requests.request]:
    id_type = "nationname"
    if type(shards) == str:
        shards = [shards]
    elif shards is None:
        shards = ["deck"]
    if type(identifier) == int:
        id_type = "nationid"
    shards = ["cards"] + shards
    res = call_api(parameters={"q": "+".join(shards), id_type: identifier})
    return res if get_response else str(res.content)


def get_auctions(get_response=False) -> Union[str, requests.request]:
    res = call_api(parameters={"q": "cards+auctions"}).content
    return res if get_response else str(res.content)


def get_trades(get_response=False) -> Union[str, requests.request]:
    res = call_api(parameters={"q": "cards+trades"}).content
    return res if get_response else str(res.content)
