import os
from sortedcontainers import SortedKeyList
from anytree.search import findall
from abc import ABC, abstractclassmethod
from typing import Tuple

from .tree import DataTree
from .container import CatalogueContainer, FileItem, DirItem
from .fsaction import FSActionDelete
from .logger import logger


class Catalogue:
    """This represents the walking of the directory tree and holding the resulting
    information, as well as actions taken on catalogue items, i.e. files and directories.
    This class holds three structures / elements:
        1. A CatalogueContainer for files, which is just for file-based sorting
        2. A CatalogueContainer for directories, which is just for
        directory-based sorting
        3. The DataTree. Nodes in the tree are
        FileItems or DirItems which inherit from anytree's NodeMixin.
        Each node in turn holds CatalogueContainers for holding children
        items.
    """

    def __init__(self, mirror_trees=[], hash_files=False):
        # self.filter_checks = []
        self.files = CatalogueContainer()
        self.dirs = CatalogueContainer()
        self.tree = DataTree()
        self.mirror_trees = mirror_trees
        self.hash_files = hash_files

    def createCatalogue(self, start):
        """Have the directory tree built up as structure and put items into containers.

        Args:
            start (str, optional): Top directory.
        """

        self.files = CatalogueContainer()
        self.dirs = CatalogueContainer()

        logger.info("Start creating catalogue (bottom up).")

        try:
            for parent_item, file_items, dir_items in self.tree.treeFromFSBottomUp(
                start=start
            ):
                self.dirs.addItem(parent_item)
                for item in file_items:
                    self.files.addItem(item)
                for item in dir_items:
                    self.dirs.addItem(item)
        except Exception as e:
            logger.error(f"Error when walking the directory tree: {e}")

        logger.info("Finished creating catalogue.")

    # def addFilterCheck(self, filter_check: FilterCheck):
    #     """Register a check object.

    #     Args:
    #         filter_check (FilterCheck): Check object
    #     """

    #     # check if a check of that kind was already added
    #     if self.filter_checks:
    #         for ix, registered_check in enumerate(self.filter_checks):
    #             if type(filter_check) == type(registered_check):
    #                 del self.filter_checks[ix]

    #     self.filter_checks.append(filter_check)

    def deleteByIDs(self, selection: Tuple[str]):
        """Executes a files system action on file or directory paths.

        Remove the items representing the paths from the respective
        containers.
        Update the tree:
            Remove the nodes and recalculate the parent's, grand parent's
            etc. sizes up the tree

        Args:
            fs_action (Action): Action object
            paths (List[str]): full paths to files or dirs
        """
        items = self.tree.deleteByIDs(selection)

        for item in items:

            logger.debug(f"Deleting item {item}.")

            if isinstance(item, FileItem):
                logger.debug(f"Removing {item} from file list.")
                self.files.removeItemByValue(item)

            if isinstance(item, DirItem):
                logger.debug(f"Removing {item} from dir list.")
                self.dirs.removeItemByValue(item)

            fs_action = FSActionDelete()
            fs_action.execute(item)

        logger.info(f"Removed {len(items)} from catalogue and disk.")


# class FilterCheck(ABC):
#     """This is the ABC class for a filter check used
#     when walking the directory tree in the Catalogue.
#     """

#     @abstractclassmethod
#     def check(self, filepath: str):
#         pass


# class FilterCheckFileExt(FilterCheck):
#     def __init__(self, extensions: List[str]):
#         self.extensions = extensions

#     def check(self, filepath: str):
#         fname, ext = os.path.splitext(filepath)

#         if ext.strip(".") in self.extensions:
#             return False
#         else:
#             return True
