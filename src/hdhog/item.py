import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Optional, Tuple

from anytree import NodeMixin
from anytree.resolver import re
from six import Iterator
from sortedcontainers import SortedKeyList

from .logger import logger


@dataclass(slots=True)
class Item(NodeMixin, ABC):
    """This is the AB class for an item held in the catalogue container.

    It's an anytree node as well.
    size = size in bytes
    """

    _dirpath: str
    _item_name: str
    item_size: int = 0
    iid: Optional[str] = None

    def __repr__(self):
        return self.iid if self.iid else ""

    @property
    def dirpath(self) -> str:
        return f"{self._dirpath}{os.path.sep}"

    @dirpath.setter
    def dirpath(self, dirpath: str) -> None:
        self._dirpath = dirpath

    @property
    def item_name(self):
        raise NotImplementedError

    @item_name.setter
    def item_name(self, item_name):
        self._item_name = item_name


class FileItem(Item):
    @property
    def item_name(self):
        return self._item_name

    def getFullPath(self) -> str:
        """Helper that returns the full path."""
        return f"{Path(self.dirpath, self.item_name)}"


def setFileSizeFromFS(file_item: FileItem) -> None:
    path = file_item.getFullPath()
    file_size = Path(path).stat().st_size
    file_item.item_size = file_size


@dataclass(kw_only=True, repr=False)
class DirItem(Item):
    """Holds children as well.
    It has three ItemContainers, two for holding and sorting files and
    directories separately, and one for holding and sorting both together.

    The size is calculated on creation from all direct children.
    With no subdirectories in it the size of a directory for now
    is only the sum of the size of it's files. The additional
    4K, or whatever the filesystem says, of any directory are not added.
    """

    inventory: "Inventory"

    @property
    def item_name(self):
        # make directories always have a path separator after name for easy distinction
        return f"{self._item_name}{os.path.sep}"

    def getFullPath(self) -> str:
        """Return the full path.

        For dirs with a separator at the end for distinction.
        """
        return f"{Path(self.dirpath, self.item_name)}{os.path.sep}"


def itemSortFn(item: Item) -> Tuple:
    return (-item.item_size, item.dirpath, item.item_name)


def addChildToDir(dir_item: DirItem, child: Item) -> None:
    dir_item.children += (child,)
    dir_item.inventory.addItem(child)
