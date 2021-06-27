import warnings
from typing import Union, List, Dict, Any
import requests
from .APICall import call_api
import re
import gzip


# An helper class for issue management
class NSIssue:
    """An helper class for issue management"""
    def __init__(self, issue_xml):
        """
        Creates an issue from an issue xml as provided by the NationStates API.

        :param issue_xml: the xml to generate the issue from
        """
        # id, title, text, author, editor, pics, options
        self.id = re.search("<ISSUE id=\"(.+)\">", issue_xml).group(1)
        for prop in ["title", "text", "author", "editor"]:
            setattr(self, prop, re.search(f"<{prop}>(.+)</{prop}>", issue_xml, flags=re.IGNORECASE).group(1))
        self.pics = re.findall("<PIC.>(.+)</PIC.>", issue_xml)

        # tuple of (id, text)
        self.options = re.findall("<OPTION id=\"(.)\">(.+)</OPTION>", issue_xml)

        self.nation = None

    # Accepts id, -1 to dismiss
    def answer(self, answer: int, nation=None):
        if nation is None:
            nation = self.nation
        if nation is None:
            return 400
        return nation.answer_issue(self.id, answer)

    # No real reason to do it but I prefer
    def __str__(self):
        out = ""
        for i in self.__dict__.keys():
            out += i + ": " + str(self.__dict__[i]) + "\n"
        return out


class Nation:
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
        headers = {param_name: param_value}
        res = call_api(parameters=parameters, headers=headers)
        status_code = res.status_code
        if status_code == 403:  # Forbidden
            warnings.warn(f"Password Incorrect, did not authenticate correctly", stacklevel=2)
            return False
        self.x_pin = res.headers["X-Pin"]
        return True

    def log_password(self, password: str) -> bool:
        """
        Authenticates the nation using a supplied password.

        :param password: The password the user uses to log-in to the country.
        :return: bool if login was successful or not.
        """
        return self.__log_in("X-Password", password)

    def log_encrypted_password(self, password: str) -> bool:
        """
        Authenticates the nation using a supplied token.

        :param password: The token the user uses to log-in to the country.
        :return: bool if login was successful or not.
        :rtype: bool
        """
        return self.__log_in("X-AutoLogin", password)

    # Commands

    def do_command(self, command: str, additional_params: Dict[str, str] = None) -> requests.Response:
        additional_params.update(c=command, nation=self.nation_name)
        additional_params.update(mode="prepare")
        req = call_api(parameters=additional_params, headers={"X-Pin": self.x_pin})
        try:
            token = re.search("<SUCCESS>(.+)</SUCCESS>", req.content.decode()).group(1)
        except IndexError:
            return req
        except AttributeError:
            return req

        additional_params.update(token=token, mode="execute")
        return call_api(parameters=additional_params, headers={"X-Pin": self.x_pin})

    def add_dispatch(self, title: str, text: str, category: int, sub_category: int) -> str:
        res = self.do_command("dispatch", {"dispatch": "add", "title": title, "text": text, "category": category, "subcategory": sub_category})
        if res.content is not None:
            return re.search("id=(\\d+)", res.content.decode()).group(1)
        return ""  # Returns empty string if fail

    def edit_dispatch(self, dispatch_id: int, title: str, text: str, category: int, sub_category: int) -> int:
        return self.do_command("dispatch", {"dispatch": "edit", "title": title, "text": text, "category": category, "subcategory": sub_category, "dispatchid": dispatch_id}).status_code

    def remove_dispatch(self, dispatch_id: int) -> int:
        return self.do_command("dispatch", {"dispatch": "remove", "dispatchid": dispatch_id}).status_code

    def giftcard(self, card_id: int, season: int, recipient_name: str) -> int:
        return self.do_command("giftcard", {"nation": self.nation_name, "cardid": card_id, "season": season, "to": recipient_name}).status_code

    # Issues have a special case because they don't require preparation, returns status code
    def answer_issue(self, issue_num, option_num) -> int:
        """Answer an available issue by specifying its id and option number"""
        return call_api(parameters={"c": "issue", "issue": issue_num, "option": option_num, "nation": self.nation_name}, headers={"X-Pin": self.x_pin}).status_code

    # Shards
    def _get_shards_request(self, shards: Union[List[str], str] = None, additional_params: Dict[str, str] = None) -> requests.Response:
        """
        This function uses the NationStates API to get a nation's shards, the complete list of shards is available on the API page.
        This function can also access private shards if the user is authenticated.

        :param shards: A list of shard names a user wants to find about the nation, a string if only one shard is wanted.
        :param additional_params: Some shards require more parameters, that's the place.

        :return: A request or its contents
        :rtype: Union[str, requests.request]
        """
        if additional_params is None:
            additional_params = {}
        if shards is None:
            shards = {}
        if type(shards) is str:
            shards = [shards]
        payloads = {"nation": self.nation_name, "q": "+".join(shards)}
        payloads.update(additional_params)
        res = call_api(parameters=payloads, headers={"X-Pin": self.x_pin})
        return res

    def _get_shards_string(self, shards: Union[List[str], str] = None, additional_params: Dict[str, str] = None) -> str:
        """Creates a shard request and takes its decoded content"""
        return self._get_shards_request(shards, additional_params).content.decode()

    # Returns the shard xml in *xml string form*, it sanitizes just the outside parts.
    def get_shards(self, shards: Union[List[str], str] = None, additional_params: Dict[str, str] = None, shard_tags: Dict[str, str] = None) -> Dict[str, str]:
        """Requests a shard and takes the string inside the outer xml tags"""
        if type(shards) == str:
            shards = [shards]
        shard_res = {}
        string_content = self._get_shards_string(shards, additional_params)
        for shard in shards:
            if shard_tags is not None and shard in shard_tags:
                shard_tag = shard_tags[shard]
            else:
                shard_tag = shard
            shard_res[shard] = re.search(f"<{shard_tag}>(.*)</{shard_tag}>", string_content, flags=re.IGNORECASE | re.DOTALL).group(1)

        return shard_res

    # List properties: [rdossier, issuessummary, dossier]
    # Essentially parsing for one extra layer
    def __list_shard_parsing(self, item) -> List[str]:
        """Ignores the tags and parses the seperated data to list"""
        str_content: str = self.get_shards(item)[item]
        ret_lis = re.findall("<.+>(.+)</.+>", str_content)
        return ret_lis

    # Needs a special class and case, returns list of issues
    @property
    def issues(self) -> List[NSIssue]:
        str_content: str = self.get_shards("issues")["issues"]
        ret_lis = []
        for issue_str in re.findall(r'<ISSUE id="\d+">.+?</ISSUE>', str_content, flags=re.DOTALL):
            new_issue = NSIssue(issue_str)
            new_issue.nation = self
            ret_lis.append(new_issue)
        return ret_lis

    # Needs a special case.
    @property
    def notices(self) -> List[Dict[str, str]]:
        notices = []
        str_content = self.get_shards("notices")["notices"]
        matches = re.findall("<NOTICE>(.+?)</NOTICE>", str_content, re.DOTALL)
        for match in matches:
            notice = {}
            categories = re.findall("<(.+)>(.+?)</\\1>", match)
            for category in categories:
                notice[category[0]] = category[1]
            if len(categories) != 0:
                notices.append(notice)
        return notices

    # Needs a special case, doesn't use parameters
    @property
    def census(self) -> Dict[str, str]:
        shard_str = self.get_shards("census")["census"]
        props = {
            "scale": re.search("<SCALE id=\"(.+?)\">", shard_str).group(1),
            "score": re.search("<SCORE>(.+)</SCORE>", shard_str).group(1),
            "rank": re.search("<RANK>(.+)</RANK>", shard_str).group(1),
            "rrank": re.search("<RRANK>(.+)</RRANK>", shard_str).group(1)
        }
        return props

    # Need a special case, list (CDATA)
    @property
    def legislation(self) -> List[str]:
        return self.__list_shard_parsing("legislation")

    # List shards (Couldn't minize due to autocomplete) *I HATE IT*.
    @property
    def rdossier(self) -> List[str]:
        return self.__list_shard_parsing("rdossier")

    @property
    def issuesummary(self) -> List[str]:
        return self.__list_shard_parsing("issuesummary")

    @property
    def dossier(self) -> List[str]:
        return self.__list_shard_parsing("dossier")

    # Regular shards (Couldn't minimize to dynamic props due to autocomplete), argh
    @property
    def admirable(self) -> str:
        return self.get_shards("admirable")["admirable"]

    @property
    def animal(self) -> str:
        return self.get_shards("animal")["animal"]

    @property
    def animaltrait(self) -> str:
        return self.get_shards("animaltrait")["animaltrait"]

    @property
    def answered(self) -> str:
        return self.get_shards("answered", shard_tags={"answered": "issues_answered"})["answered"]

    @property
    def banner(self) -> str:
        return self.get_shards("banner")["banner"]

    @property
    def banners(self) -> str:
        return self.get_shards("banners")["banners"]

    @property
    def capital(self) -> str:
        return self.get_shards("capital")["capital"]

    @property
    def category(self) -> str:
        return self.get_shards("category")["category"]

    @property
    def crime(self) -> str:
        return self.get_shards("crime")["crime"]

    @property
    def currency(self) -> str:
        return self.get_shards("currency")["currency"]

    @property
    def customleader(self) -> str:
        return self.get_shards("customleader")["customleader"]

    @property
    def customcapital(self) -> str:
        return self.get_shards("customcapital")["customcapital"]

    @property
    def customreligion(self) -> str:
        return self.get_shards("customreligion")["customreligion"]

    @property
    def dbid(self) -> str:
        return self.get_shards("dbid")["dbid"]

    @property
    def deaths(self) -> str:
        return self.get_shards("deaths")["deaths"]

    @property
    def demonym(self) -> str:
        return self.get_shards("demonym")["demonym"]

    @property
    def demonym2(self) -> str:
        return self.get_shards("demonym2")["demonym2"]

    @property
    def demonym2plural(self) -> str:
        return self.get_shards("demonym2plural")["demonym2plural"]

    @property
    def dispatches(self) -> str:
        return self.get_shards("dispatches")["dispatches"]

    @property
    def dispatchlist(self) -> str:
        return self.get_shards("dispatchlist")["dispatchlist"]

    @property
    def endorsements(self) -> str:
        return self.get_shards("endorsements")["endorsements"]

    @property
    def factbooks(self) -> str:
        return self.get_shards("factbooks")["factbooks"]

    @property
    def factbooklist(self) -> str:
        return self.get_shards("factbooklist")["factbooklist"]

    @property
    def firstlogin(self) -> str:
        return self.get_shards("firstlogin")["firstlogin"]

    @property
    def flag(self) -> str:
        return self.get_shards("flag")["flag"]

    @property
    def founded(self) -> str:
        return self.get_shards("founded")["founded"]

    @property
    def foundedtime(self) -> str:
        return self.get_shards("foundedtime")["foundedtime"]

    @property
    def freedom(self) -> str:
        return self.get_shards("freedom")["freedom"]

    @property
    def fullname(self) -> str:
        return self.get_shards("fullname")["fullname"]

    @property
    def gavote(self) -> str:
        return self.get_shards("gavote")["gavote"]

    @property
    def gdp(self) -> str:
        return self.get_shards("gdp")["gdp"]

    @property
    def govt(self) -> str:
        return self.get_shards("govt")["govt"]

    @property
    def govtdesc(self) -> str:
        return self.get_shards("govtdesc")["govtdesc"]

    @property
    def govtpriority(self) -> str:
        return self.get_shards("govtpriority")["govtpriority"]

    @property
    def happenings(self) -> str:
        return self.get_shards("happenings")["happenings"]

    @property
    def income(self) -> str:
        return self.get_shards("income")["income"]

    @property
    def industrydesc(self) -> str:
        return self.get_shards("industrydesc")["industrydesc"]

    @property
    def influence(self) -> str:
        return self.get_shards("influence")["influence"]

    @property
    def lastactivity(self) -> str:
        return self.get_shards("lastactivity")["lastactivity"]

    @property
    def lastlogin(self) -> str:
        return self.get_shards("lastlogin")["lastlogin"]

    @property
    def leader(self) -> str:
        return self.get_shards("leader")["leader"]

    @property
    def majorindustry(self) -> str:
        return self.get_shards("majorindustry")["majorindustry"]

    @property
    def motto(self) -> str:
        return self.get_shards("motto")["motto"]

    @property
    def name(self) -> str:
        return self.get_shards("name")["name"]

    @property
    def notable(self) -> str:
        return self.get_shards("notable")["notable"]

    @property
    def policies(self) -> str:
        return self.get_shards("policies")["policies"]

    @property
    def poorest(self) -> str:
        return self.get_shards("poorest")["poorest"]

    @property
    def population(self) -> str:
        return self.get_shards("population")["population"]

    @property
    def publicsector(self) -> str:
        return self.get_shards("publicsector")["publicsector"]

    @property
    def rcensus(self) -> str:
        return self.get_shards("rcensus")["rcensus"]

    @property
    def region(self) -> str:
        return self.get_shards("region")["region"]

    @property
    def religion(self) -> str:
        return self.get_shards("religion")["religion"]

    @property
    def richest(self) -> str:
        return self.get_shards("richest")["richest"]

    @property
    def scvote(self) -> str:
        return self.get_shards("scvote")["scvote"]

    @property
    def sectors(self) -> str:
        return self.get_shards("sectors")["sectors"]

    @property
    def sensibilities(self) -> str:
        return self.get_shards("sensibilities")["sensibilities"]

    @property
    def tax(self) -> str:
        return self.get_shards("tax")["tax"]

    @property
    def tgcanrecruit(self) -> str:
        return self.get_shards("tgcanrecruit")["tgcanrecruit"]

    @property
    def tgcancampaign(self) -> str:
        return self.get_shards("tgcancampaign")["tgcancampaign"]

    @property
    def type(self) -> str:
        return self.get_shards("type")["type"]

    @property
    def wa(self) -> str:
        return self.get_shards("wa")["wa"]

    @property
    def wabadges(self) -> str:
        return self.get_shards("wabadges")["wabadges"]

    @property
    def wcensus(self) -> str:
        return self.get_shards("wcensus")["wcensus"]

    @property
    def zombie(self) -> str:
        return self.get_shards("zombie")["zombie"]

    @property
    def nextissue(self) -> str:
        return self.get_shards("nextissue")["nextissue"]

    @property
    def nextissuetime(self) -> str:
        return self.get_shards("nextissuetime")["nextissuetime"]

    @property
    def packs(self) -> str:
        return self.get_shards("packs")["packs"]

    @property
    def ping(self) -> str:
        return self.get_shards("ping")["ping"]

    @property
    def unread(self) -> str:
        return self.get_shards("unread")["unread"]


# Returns .gz compressed file with nations.xml in it, so decoding will not work. Using gzip to parse it.
def get_nations() -> str:
    """Gets the daily data dump of all the nations. The generated file is quite large, so long wait times may occur."""
    res = call_api(headers={}, base_url="https://www.nationstates.net/pages/nations.xml.gz")
    return gzip.decompress(res.content).decode()
