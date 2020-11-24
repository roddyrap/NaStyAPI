Code Snippets
*************

Get a public shard on a nation
##############################
.. code-block:: python

    from NaStyAPI import Nation
    Nation.get_shards("NATION_NAME",["SHARDS"])

Log in to your nation
#####################

.. code-block:: python

    from NaStyAPI import Nation
    your_nation = Nation.Nation("NATION_NAME")
    your_nation.log_password("YOUR_PASSWORD")

Access to private shards
########################

.. code-block:: python

    your_nation.get_shards("YOUR_PRIVATE_SHARDS")

Write a dispatch using the api
###############################

.. code-block:: python

    new_dispatch = your_nation.do_command("dispatch", additional_params={"dispatch": "add", "title": "YOUR POST TITLE", "text": "DISPATCH TEXT", "category": "CATEGORY_NUM", "subcategory": "SUBCATEGORY_NUM"})