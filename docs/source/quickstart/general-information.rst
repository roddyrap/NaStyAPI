General Information
*******************
| NaStyAPI Version: 0.2.

The NationStates API is url based, and can be quite hard and uncomfortable to use.
That's why NaStyAPI is here!

NaStyAPI currently supports:

- Nation API
    - Standard
    - Public shards
    - Private information
        - Private shards
        - Private commands
    - Daily data dump
- Region API
    - Standard
    - Shards
    - Daily data dump
- World API
    - Shards
- World Assembly API
    - Shards
- Telegrams API
    - Recuitement telegrams
    - Non recuitement telegrams
- Trading Cards
    - Individual Cards
    - Daily data dump

| NaStyAPI has three different active rate limits, and when the requests are too much it will wait to ensure each request gets a response.
| The first rate limit is active on all requests, and is the regular 50 requests per 30 seconds.
| The second rate limit is active on non recuitement telegrams, the API only allows for 1 request every 30 seconds.
| The third rate limit is active on recuitement telegrams, the API only allows for 1 request every 180 seconds.
