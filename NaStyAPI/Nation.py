from typing import Union, List
import requests
from .APICall import call_api
from .Telegrams import send_telegram
# I need to use the user's actual userAgent
userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"


class Nation:
    def __init__(self, nation_name: str):  # Just to initialize, isn't able to do much until logged in.
        self.nation_name = nation_name
        self.x_pin = "-1"

    def __log_in(self, param_name, param_value) -> bool:
        parameters = {"nation": self.nation_name, "q": "ping"}
        headers = {
            "User-Agent": userAgent, param_name: param_value}
        res = requests.get("https://www.nationstates.net/cgi-bin/api.cgi?", params=parameters, headers=headers)
        try:
            self.x_pin = res.headers["X-Pin"]
        except KeyError:
            return False
        return True

    def log_password(self, password: str) -> bool:
        return self.__log_in("X-Password", password)

    def log_encrypted_password(self, password: str) -> bool:
        return self.__log_in("X-AutoLogin", password)

    def get_shards(self, shards: Union[List[str], str]) -> str:
        if type(shards) is str:
            shards = [shards]
        payloads = {"nation": self.nation_name, "q": "+".join(shards)}
        headers = {
            "User-Agent": userAgent, "X-Pin": self.x_pin}
        res = requests.get("https://www.nationstates.net/cgi-bin/api.cgi", params=payloads, headers=headers)
        return str(res.content)

    def logged(self) -> bool:
        payloads = {"nation": self.nation_name, "q": "ping"}
        headers = {
            "User-Agent": userAgent, "X-Pin": self.x_pin}
        res = call_api(headers, payloads)
        return res.status_code == 200

    def send_telegram(self, client: str, tgid: str, key: str) -> bytes:
        return send_telegram(client, tgid, key, self.nation_name)


def get_shards(nation_name: str, shards: Union[List[str], str]) -> str:
    if type(shards) is str:
        shards = [shards]
    payloads = {"nation": nation_name, "q": "+".join(shards)}
    headers = {
        "User-Agent": userAgent}
    res = call_api(headers, payloads)
    return str(res.content)


def get_nations():
    headers = {
        "User-Agent": userAgent}
    res = requests.get("https://www.nationstates.net/pages/nations.xml.gz", headers=headers)
    return res.content
