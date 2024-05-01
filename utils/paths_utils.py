import logging
import math
import os
import re

import xml.etree.ElementTree as xml_tree


def search_files(path, depth=math.inf, regex=""):
    """
    Search files recursively from given path.
    add regex expression to filter files.
    e.g. "[^.]*\.jpg$" to find all jpg files.

    :param str path:
    :param int depth: how deep to search for files.
    :param str regex: filtering files to find based on regex
    :rtype: list[str]
    """

    elements = os.listdir(path)

    if not elements:
        return []

    if regex:
        if isinstance(regex, str):
            regex = re.compile(regex)

    folders = []
    files = []
    for item in elements:
        joined = os.path.join(path, item)
        if os.path.isfile(joined):
            if regex and not regex.match(joined):
                continue
            files.append(joined)
        elif os.path.isdir(joined):
            folders.append(joined)

    new_dept = depth - 1
    if new_dept >= 0:
        for folder in folders:
            files.extend(search_files(folder, new_dept, regex))

    return files


class PathMaker():

    def __init__(self, root_path, permission=None):

        self.create_folder(root_path, permission)
        self.__root_path = root_path

    @property
    def root_path(self):
        return self.__root_path

    # ------------------- BUILD FROM DICT -------------------

    @staticmethod
    def dict_folder(name, permission=None):

        return {name: {"permission": permission, 'subtree': {}}}

    def __build_dict_folder(self, path, dict_folder):
        """
        Recursively creates folders and subfolders from a "dict_folder"

        :param str path:
        :param dict dict_folder:
        """
        for folder in dict_folder.items():
            full_path = os.path.join(path, folder[0])
            self.create_folder(full_path, folder[1]["permission"])
            if folder[1]["subtree"]:
                self.__build_dict_folder(full_path, folder[1]["subtree"])

    def build_branches_from_dict(self, dict_folder):
        """
        From root path, creates tree based on provided tree_dict argument.
        Expected tree_dict format is:

        {
        "folder_name" : {"permission" : "permission", 'subtree': {"folder_name": {"permission" : "permission", "subtree": {}}}}

        "folder_name" : {"permission" : "permission",
                        'subtree': []}
        "folder_name" : {"permission" : "permission",
                        'subtree': []}
        }


        :param dict tree_dict:
        """

        if not isinstance(dict_folder, dict):
            logging.error(f"Provided argument: 'tree_dict' is not a dict.")
            return

        self.__build_dict_folder(self.__root_path, dict_folder)

    # ------------------- BUILD FROM XML -------------------

    def __build_xml_folders(self, root, folder):
        """
        Recursively creates folders and subfolders from a "dict_folder"

        :param str root: Current path from which to create folders structure.
        :param xml_tree.Element folder: Current xml_tree.Element from which to create folders structure.
        :return:
        """
        for element in folder:
            name = element.attrib["name"]
            permission = element.attrib["permission"]
            full_path = os.path.join(root, name)
            if element.tag == "folder":
                self.create_folder(full_path, permission)
                self.__build_xml_folders(full_path, element)
            elif element.tag == "file":
                self.create_file(full_path, permission)

    def build_branches_from_xml(self, xml_path, root_permission=None):
        """
        From root path, creates tree based on provided tree_dict argument.
        :param root_path:
        :param xml_path:
        :return:
        """

        if not os.path.exists(xml_path) and not re.match("\.xml$", xml_path):
            logging.error(f"{xml_path} does not exists or is not xml file.")
            return

        self.create_folder(self.__root_path, root_permission)

        tree = xml_tree.parse(xml_path)
        root = tree.getroot()

        self.__build_xml_folders(self.__root_path, root)

    # ------------------- BASE METHODS -------------------

    @staticmethod
    def create_folder(path, permission=None):
        """
        Created folders from given path if it doesn't already exists.

        :param str path:
        :param str permission:
        :rtype: str
        """
        if os.path.exists(path):
            return path

        try:
            os.makedirs(path)
            if permission:
                os.chmod(path, int(permission))
        except Exception as e:
            logging.error(e)
            return ""

        return path

    @staticmethod
    def create_file(filepath, permission=None):
        """
        Created folders from given filepath if it doesn't already exists.

        :param str path:
        :param str permission:
        :rtype: str
        """
        if os.path.exists(filepath):
            return filepath

        try:
            open(filepath, 'a').close()
            if permission:
                os.chmod(filepath, int(permission))
        except OSError:
            print('Failed creating the file')
            return ""
        return filepath


# ------------------- TESTING -------------------


from locations import DESKTOP

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
pmaker.build_branches_from_xml(r"C:\Users\Jordan\PycharmProjects\python_utils\utils\test_pathmaker.xml")

tree = xml_tree.parse(r"C:\Users\Jordan\PycharmProjects\python_utils\utils\test_pathmaker.xml")
root = tree.getroot()

print(root)
