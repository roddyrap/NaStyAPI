# NaStyAPI - A NationStates wrapper
![PyPi status](https://github.com/Nimi142/NaStyAPI/workflows/PyPi%20status/badge.svg)
[![Documentation Status](https://readthedocs.org/projects/nastyapi/badge/?version=latest)](https://nastyapi.readthedocs.io/en/latest/?badge=latest)
<br/>
A Python wrapper for the [NationStates](https://www.nationstates.net/) [api](https://www.nationstates.net/pages/api.html). <br/>
Works with a rate limit so as not to exceed NationState's API's rate limit. <br/>
[GitHub Link](https://github.com/Nimi142/NaStyAPI)
## Table of Contents:
- [NaStyAPI - A NationState wrapper](#nastyapi---a-nationstates-wrapper)
  - [Table of Contents:](#table-of-contents)
  - [Installation](#installation)
  - [Documentation](#documentation)
  - [General Use](#general-use)
    - [Warning](#warning)
    - [Examples](#examples)
      - [Get a shard on a nation](#get-a-shard-on-a-nation)
      - [Log in to your nation](#log-in-to-your-nation)
      - [Write a dispatch using the api](#write-a-dispatch-using-the-api)
  - [How to contribute](#how-to-contribute)
  - [To-do](#to-do)

## Installation
The package is available on PyPi! simply write:<br/>
```pip install NaStyAPI```

## Documentation
[Link to full documentation (extremely outdated)](https://nastyapi.readthedocs.io/en/stable/)
## General Use
The NationStates API is divided into parts, and so is the wrapper.
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
I take no responsibility for mistakes and errors that are caused by the use of this software. This is still in development and should not be used to handle sensitive or important information. 

### Examples

### Recommendation
NationStates requires ("must") api users to specify a User-Agent.
The default User-Agent is "A NaStyAPI User. Contact Roddy.Rappaport@gmail.com for issues.", and NationStates requires that the user agent will be "something informative, such as the URL of your site or your e-mail address. It can be whatever you want, so long as it allows us to contact you if something goes wrong with your script."
```python
from NaStyAPI import APICall
APICall.set_user_agent("Your Email")
```
#### Log in to your nation
```python
from NaStyAPI import Nation
your_nation = Nation.Nation("NATION_NAME")
your_nation.log_password("YOUR_PASSWORD")
```
#### Get a shard on a nation
```python
from NaStyAPI import Nation
your_nation = Nation.Nation("nation_name")
your_nation.log_password("YOUR_PASSWORD")  # If shard is private, else not needed
your_nation.shard
```
#### Get multiple shards
```python
from NaStyAPI import Nation
your_nation = Nation.Nation("nation_name")
your_nation.get_shards(["shards"])
```
#### Write a dispatch using the api
```python
from NaStyAPI import Nation
your_nation = Nation.Nation("nation_name")
your_nation.log_password("password")
new_dispatch = your_nation.add_dispatch("title", "text", "category", "sub_category")
```


## To-do
This is a list of the features I am currently working on that should be ready quite soon.
- Finding bugs.
- Handling edge cases.
- Adding descriptions and updating docs.

## How to contribute
Thank you for looking at this!
If you want to contribute, feel free to update the docs in the /docs/ folder. I am still adding features, so I didn't have the time to do it myself.

## Show Support
My in-game nation is "Khiralia", if you want to show support feel free to telegram a nice message :)
