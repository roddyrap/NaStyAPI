import requests
userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"


# TODO: Add rate limit
def send_telegram(client: str, tgid: str, key: str, to: str) -> bytes:
    headers = {"User-Agent": userAgent}
    parameters = {"a": "sendTG", "client": client, "tgid": tgid, "key": key, "to": to}
    res = requests.get("https://www.nationstates.net/cgi-bin/api.cgi", params=parameters, headers=headers)
    return res.content