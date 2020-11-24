import requests
from .APICall import call_api
from typing import Union, List, Dict
userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"


# Council id: 1 for GA 2 for SC.
def get_shards(council_id: str, shards: Union[List[str], str], additional_params: Dict[str, str] = None, get_request: bool = False) -> Union[bytes, requests.request]:
    if type(shards) is str:
        shards = [shards]
    payloads = {"wa": council_id, "q": "+".join(shards)}
    if additional_params is None:
        additional_params = {}
    payloads.update(additional_params)
    res = call_api(parameters=payloads)
    return res if get_request else res.content
