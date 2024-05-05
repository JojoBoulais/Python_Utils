from locations import DESKTOP
from paths_utils import PathMaker
import xml.etree.ElementTree as xml_tree




pmaker = PathMaker(DESKTOP)

# BUILDING FROM DICT

subtree = {
    "blabla": {"permission": "0444", 'subtree': {}},
    "bloublou": {"permission": "0444", 'subtree': {}},
    "toto": {"permission": "0444", 'subtree': {}},
}

tree = {
    "layer_1": {"permission": "0444", 'subtree': subtree},
    "layer_2": {"permission": "0444", 'subtree': {}},
    "layer_3": {"permission": "0444", 'subtree': subtree}
}

pmaker.build_branches_from_dict(tree)

# BUILDING FROM XML
pmaker.build_branches_from_xml(r"C:\Users\Jordan\PycharmProjects\python_utils\utils\z__test_pathmaker.xml")

tree = xml_tree.parse(r"C:\Users\Jordan\PycharmProjects\python_utils\utils\z__test_pathmaker.xml")
root = tree.getroot()

print(root)