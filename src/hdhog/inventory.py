from typing import List, Tuple

from sortedcontainers import SortedKeyList

from .item import DirItem, FileItem, Item, itemSortFn
from .logger import logger


class Inventory:
    """This represents the walking of the directory tree and holding the resulting
    information, as well as actions taken on catalogue items, i.e. files and directories.
    This class holds three structures / elements:
        1. A CatalogueContainer for files, which is just for file-based sorting
        2. A CatalogueContainer for directories, which is just for
        directory-based sorting
        3. The FSTree. Nodes in the tree are
        FileItems or DirItems which inherit from anytree's NodeMixin.
        Each node in turn holds CatalogueContainers for holding children
        items.
    """

    def __init__(self):
        self.per_type_lists = {
            FileItem: SortedKeyList(key=itemSortFn),
            DirItem: SortedKeyList(key=itemSortFn),
        }
        self.dirs_files = SortedKeyList(key=itemSortFn)

    def addItem(self, item: Item):
        item_list = self.per_type_lists[type(item)]
        item_list.add(item)
        self.dirs_files.add(item)

    def removeItem(self, item: Item):
        logger.debug(f"Removing {item} ....")
        try:
            item_list = self.per_type_lists[type(item)]
            item_list.remove(item)
            self.dirs_files.remove(item)
        except ValueError as ve:
            logger.error(f"Error removing item from container: {ve}")
