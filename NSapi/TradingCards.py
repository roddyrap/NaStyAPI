import requests
from typing import Union, List
userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"


def get_trading_cards(season_number: int):
    headers = {
        "User-Agent": userAgent}
    res = requests.get(f"https://www.nationstates.net/pages/cardlist_S{season_number}.xml.gz", headers=headers)
    return res.content


def get_info_on_card(card_name: str, shards: Union[List[str], str]) -> str:
    if type(shards) is str:
        shards = [shards]
    shards = ["card"] + shards
    payloads = {"card": card_name, "q": "+".join(shards)}
    headers = {
        "User-Agent": userAgent}
    res = requests.get("https://www.nationstates.net/cgi-bin/api.cgi", params=payloads, headers=headers)
    return str(res.content)
