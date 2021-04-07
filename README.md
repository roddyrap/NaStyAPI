# NaStyAPI - A NationState wrapper
![PyPi status](https://github.com/Nimi142/NaStyAPI/workflows/PyPi%20status/badge.svg)
[![Documentation Status](https://readthedocs.org/projects/nastyapi/badge/?version=latest)](https://nastyapi.readthedocs.io/en/latest/?badge=latest)
<br/>
!Note: This package is still highly in development and is really not recommended for public use yet!<br/>
A Python wrapper for the [NationStates](https://www.nationstates.net/) [api](https://www.nationstates.net/pages/api.html).<br/>
Works with a rate limit so as not to exceed NationState's API's rate limit.<br/>
NaStyAPI only handles communication, it does not parse the result in any way!
[GitHub Link](https://github.com/Nimi142/NaStyAPI)
## Table of Contents:
- [NaStyAPI - A NationState wrapper](#nastyapi---a-nationstate-wrapper)
  - [Table of Contensts:](#table-of-contents)
  - [Installation](#installation)
  - [Documentation](#documentation)
  - [General Use](#general-use)
    - [Warning](#warning)
    - [Examples](#examples)
      - [Get a public shard on a nation](#get-a-public-shard-on-a-nation)
      - [Log in to your nation](#log-in-to-your-nation)
      - [Access to private shards](#access-to-private-shards)
      - [Write a dispatch using the api](#write-a-dispatch-using-the-api)
  - [How to contribute](#how-to-contribute)

## Installation
The package is available on PyPi! simply write:<br/>
```pip install NaStyAPI```

## Documentation
[Link to full documentation (in progress)](https://nastyapi.readthedocs.io/en/stable/)
## General Use
The NationState API is divided into parts, and so is the wrapper.
The parts are:

- Nation
- Region
- Telegrams
- TradingCards
- World
- WorldAssembly<br/>

To use a part, simply write:<br/>
```python
from NaStyAPI import Part
```
### Warning
The wrapper is usable already, as you can see by the examples below. That, however, does not mean it's recommended to use.
The wrapper is largely undocumented and is not yet great at managing errors. You can use it, but it's not going to be to pleasant.

### Examples
#### Get a public shard on a nation
```python
from NaStyAPI import Nation
Nation.get_shards("NATION_NAME",["SHARDS"])
```
#### Log in to your nation
```python
from NaStyAPI import Nation
your_nation = Nation.Nation("NATION_NAME")
your_nation.log_password("YOUR_PASSWORD")
```
#### Access to private shards
```python
your_nation.get_shards("YOUR_PRIVATE_SHARDS")
```
#### Write a dispatch using the api
```python
new_dispatch = your_nation.do_command("dispatch", additional_params={"dispatch": "add", "title": "YOUR POST TITLE", "text": "DISPATCH TEXT", "category": "CATEGORY_NUM", "subcategory": "SUBCATEGORY_NUM"})
```

## How to contribute
Thank you for looking at this!
As mentioned earlier, the library does not yet contain meaningful parse functions in the parse module. Any help would be appreciated.