import xml.etree.ElementTree as ET
import xml


def parse_to_element(res) -> xml.etree.ElementTree.Element:
    res = res.replace("\\n", "\n")[2:-1]
    root = ET.fromstring(res)
    return root
