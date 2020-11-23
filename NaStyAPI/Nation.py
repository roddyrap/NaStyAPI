from typing import Union, List, Dict
import requests
from .APICall import call_api
from .Telegrams import send_telegram, send_recruitment_telegram
import re
# I need to use the user's actual userAgent
userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"


class Nation:
    """
    A basic Nation class used to represent a user's log in.
    :param nation_name: The nation's name
    :type nation_name: str
    :ivar x_pin: A user's password the server uses for rapid authentication
    :type x_pin: str
    """
    def __init__(self, nation_name: str):  # Just to initialize, isn't able to do much until logged in.
        self.nation_name = nation_name
        self.x_pin = "-1"

    def __log_in(self, param_name: str, param_value: str) -> bool:
        """
        Logs in the user by issuing a request with a header of para_name with a value of param_value.
        :param param_name: The header name, should be one of: "X-Password", "X-AutoLogin" or "X-Pin", if advanced.
        :param param_value: The value of the header, an authentication token of some sort.
        :return: if login was successful or not, through bool.
        """
        parameters = {"nation": self.nation_name, "q": "ping"}
        headers = {
            "User-Agent": userAgent, param_name: param_value}
        res = call_api(parameters=parameters, headers=headers)
        try:
            self.x_pin = res.headers["X-Pin"]
        except KeyError:
            return False
        return True

    def log_password(self, password: str) -> bool:
        """
        Logs the nation in using a supplied password
        :param password: The password the user uses to log-in to the country.
        :return: bool if login was successful or not.
        """
        return self.__log_in("X-Password", password)

    def log_encrypted_password(self, password: str) -> bool:
        """
        Logs the nation in using a supplied token
        :param password: The token the user uses to log-in to the country.
        :return: bool if login was successful or not.
        :rtype: bool
        """
        return self.__log_in("X-AutoLogin", password)

    def get_shards(self, shards: Union[List[str], str], get_request: bool = False):
        """
        :param shards: A list of shard names a user wants to find about the nation, a string if only one shard is wanted
        :param get_request: getting the request or it's contents
        :return: A request or its contents
        :rtype: Union[str, requests.request]
        """
        if type(shards) is str:
            shards = [shards]
        payloads = {"nation": self.nation_name, "q": "+".join(shards)}
        res = call_api(parameters=payloads)
        return res if get_request else str(res.content)

    def prepare_command(self, command: str, additional_params:Dict[str, str] = None) -> str:
        if additional_params is None:
            additional_params = {}
        if not self.logged():
            return "Not authenticated"
        parameters = {"nation": self.nation_name, "c": command, "mode": "prepare"}
        headers = {"X-Pin": self.x_pin}
        parameters.update(additional_params)
        res = call_api(parameters=parameters, headers=headers)
        return re.search("<.+>.*<.+>(.+)<.+>.*<.+>", str(res.content)).groups(1)

    def execute_command(self, command: str, token: str, additional_params:Dict[str, str] = None, get_request: bool = False):
        if not self.logged():
            return "Not authenticated"
        parameters = {"nation": self.nation_name, "c": command, "mode": "prepare"}
        headers = {"X-Pin": self.x_pin}
        parameters.update(additional_params)
        parameters["mode"] = "execute"
        parameters["token"] = token
        res = call_api(parameters=parameters, headers=headers)
        return res if get_request else res.content

    def do_command(self, command: str, additional_params:Dict[str, str] = None, get_request: bool = False):
        return self.execute_command(command, self.prepare_command(command, additional_params), additional_params, get_request)

    def logged(self) -> bool:
        payloads = {"nation": self.nation_name, "q": "ping"}
        headers = {
            "User-Agent": userAgent, "X-Pin": self.x_pin}
        res = call_api(headers, payloads)
        return res.status_code == 200

    def send_telegram(self, client: str, tgid: str, key: str) -> bytes:
        return send_telegram(client, tgid, key, self.nation_name)

    def sand_recruitment_telegram(self, client: str, tgid: str, key: str) -> bytes:
        return send_recruitment_telegram(client, tgid, key, self.nation_name)


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
    res = call_api(headers=headers, base_url="https://www.nationstates.net/pages/nations.xml.gz")
    return res.content
