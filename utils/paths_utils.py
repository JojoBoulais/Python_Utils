import os
import logging

class PathMaker():

    def __init__(self, root_path, permission=None):

        self.create_folder(root_path, permission)
        self.__root_path = root_path
        self.__current_path = root_path

    @property
    def root_path(self):
        return self.__root_path

    @staticmethod
    def dict_folder(name, permission=None):

        return {name: {permission: "permission", 'subtree': {} }}

    def build_dict_folder(self, path, dict_folder):
        print("heeeere")
        for folder in dict_folder.items():
            full_path = os.path.join(path, folder[0])
            self.create_folder(full_path, folder[1]["permission"])
            if folder[1]["subtree"]:
                self.build_dict_folder(full_path, dict_folder)

    def build_tree_from_dict(self, dict_folder):
        """
        From root path, create tree based on provided tree_dict argument.
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

        self.build_dict_folder(self.__root_path, dict_folder)


    def create_folder(self, path, permission=None):

        if os.path.isdir(path):
            logging.error(f"Provided path: '{path}' is not a directory.")
            return

        if not os.path.exists(path):
            try:
                os.makedirs(path)
                if permission:
                    os.chmod(path, permission)
            except Exception as e:
                logging.error(e)

        return path

from locations import DESKTOP

pmaker = PathMaker(DESKTOP)


first_root = PathMaker.dict_folder("first_root")
second_root = PathMaker.dict_folder("second_root")

inside_fist = PathMaker.dict_folder("first_root")
first_root["subtree"].update(inside_fist)

first_root.update(second_root)




pmaker.build_tree_from_dict(first_root)