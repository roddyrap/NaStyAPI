import xml.etree.ElementTree as ET
import xml
from typing import Dict, Union, Iterable
import re

recurse_dict = Union[Dict, Iterable[Dict]]


def parse_to_element(res) -> xml.etree.ElementTree.Element:
    res = res.replace("\\n", "\n")[2:-1]
    root = ET.fromstring(res)
    return root


def parse_to_dict(res: Union[str, bytes]) -> recurse_dict:
    if res is bytes:
        res = res.decode('utf-8')
    res = re.sub(r"<([A-Z]+)\s*.*?=\"(.+?)\">([^<>]*)</\1>", r"<\2>\3</\2>", res)
    print(res)
    return __dict_top_level(res)


def __dict_top_level(data) -> recurse_dict:
    title_pattern = r"<(.*?)>(.*)</\1>"
    title_match = re.search(title_pattern, data, re.DOTALL)
    if title_match is None:
        raise Exception("Couldn't parse request")
    in_data = title_match.group(2)
    in_match = re.finditer("<(.*?)>(.*?)</\1>", in_data)
    groups = re.search("<(.*?)>(.*?)</\1>", in_data, re.DOTALL)
    if not [i for i in in_match]:
        return {title_match.group(1): in_data}
    else:
        return {title_match.group(1): [__dict_top_level(match_string) for match_string in in_match]}
