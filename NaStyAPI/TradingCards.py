import requests
from typing import Union, List
from .APICall import call_api
import gzip


def get_trading_cards(season_number: int) -> str:
    res = call_api(base_url=f"https://www.nationstates.net/pages/cardlist_S{season_number}.xml.gz")
    return gzip.decompress(res.content)


def get_info_on_card(card_id: Union[str, int], season, shards: Union[List[str], str]) -> str:
    if type(shards) is str:
        shards = [shards]
    shards = ["card"] + shards
    payloads = {"q": "card+" + "+".join(shards), "cardid": card_id, "season": season}
    res = call_api(parameters=payloads)
    return res.content.decode()


def get_deck_information(identifier: Union[str, int], shards: Union[str, List[str]] = None) -> str:
    id_type = "nationname"
    if type(shards) == str:
        shards = [shards]
    elif shards is None:
        shards = ["deck"]
    if type(identifier) == int:
        id_type = "nationid"
    shards = ["cards"] + shards
    res = call_api(parameters={"q": "+".join(shards), id_type: identifier})
    return res.content.decode()


def get_auctions() -> str:
    res = call_api(parameters={"q": "cards+auctions"})
    return res.content.decode()


def get_trades() -> str:
    res = call_api(parameters={"q": "cards+trades"})
    return res.content.decode()
