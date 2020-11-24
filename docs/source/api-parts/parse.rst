Parse
=====

Descripton
**********
In contrast to the other modules in the package, this part does not have any interaction with the NationState's API.
It's only purpose is to take the string responses of requests from the API and return them at a different format.

It's still under development, and it's advised not to use it at all as of now.

Methods
*******
As of version 0.2.1, NaStyAPI only has one function in the Parse module, and it is:

parse_to_element
################

.. code-block:: python

    def parse_to_element(res) -> xml.etree.ElementTree.Element:

This method takes the string response from the API and converts it to a xml.etree.ElementTree.Element instance.