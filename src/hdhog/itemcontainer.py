import os
from sortedcontainers import SortedKeyList
from anytree import NodeMixin
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List
from .logger import logger


class ItemContainer:
    """Holds Items (actual objects) and provides sorting thereof."""

    def __init__(self) -> None:
        self.itemcontainer = SortedKeyList(
            key=lambda item: (
                -item.size,
                item.dirpath,
                item.name,
            )
        )

    def __len__(self) -> int:
        return len(self.itemcontainer)

    def __bool__(self) -> bool:
        if self.itemcontainer:
            return True
        else:
            return False

    def __contains__(self, obj: "Item") -> bool:
        for item in self.itemcontainer:
            if item == obj:
                return True
        return False

    def __iter__(self) -> "ItemContainer":
        return iter(self.itemcontainer)

    def __getitem__(self, ix: int) -> "Item":
        return self.itemcontainer[ix]

    def addItem(self, item: "Item") -> None:
        self.itemcontainer.add(item)

    def removeItem(self, item: "Item") -> None:
        self.itemcontainer.remove(item)


class Item(NodeMixin, ABC):
    """This is the AB class for an item held in the catalogue
    container. It's an anytree node as well.

    size = size in bytes
    """

    __slots__ = ["size", "dirpath", "name"]

    def __init__(self, iid: str, dirpath: str, name: str, size: int = 0):
        super().__init__()
        self.iid = iid
        self.dirpath = f"{Path(dirpath)}{os.path.sep}"
        self.name = name
        self.size = size

    def __str__(self) -> str:
        return self.getFullPath()

    def __repr__(self) -> str:
        return self.getFullPath()

    @abstractmethod
    def _getSize(self) -> int:
        pass

    @abstractmethod
    def getFullPath(self) -> str:
        pass

    def rmNodeFromParent(self) -> None:
        """Remove this node from all of its parent's structures:
        as tree child and from the item container
        """
        if self.parent:
            logger.debug(f"Remove node {self} from parent structures.")
            parent_children = [ch for ch in self.parent.children if ch != self]
            self.parent.children = tuple(parent_children)

            self.parent.dirs_files.removeItem(self)

            if isinstance(self, FileItem):
                self.parent.files.removeItem(self)
            if isinstance(self, DirItem):
                self.parent.dirs.removeItem(self)


class FileItem(Item):
    __slots__ = ["type", "hash"]

    def __init__(
        self, iid: str, dirpath: str, name: str, size: int = 0, hash_files: bool = False
    ):
        super().__init__(iid, dirpath, name, size)
        self.setFileType(dirpath, name)

    def setFileType(self, dirpath: str, name: str) -> None:
        self.type = Path(self.name).suffix

    def _getSize(self) -> int:
        return self.size

    def getFullPath(self) -> str:
        return str(Path(self.dirpath, self.name))


class DirItem(Item):
    """Holds children as well.
    It has three ItemContainers, two for holding and sorting files and
    directories separately, and one for holding and sorting both together.

    The size is calculated on creation from all direct children.
    With no subdirectories in it the size of a directory for now
    is only the sum of the size of it's files. The additional
    4K, or whatever the filesystem says, of any directory are not added.
    """

    __slots__ = ["files", "dirs", "dirs_files", "children"]

    def __init__(
        self,
        iid: str,
        dirpath: str,
        name: str,
        file_children: List[FileItem] = [],
        dir_children: List["DirItem"] = [],
    ):
        super().__init__(iid, dirpath, name)
        self.files = ItemContainer()
        self.dirs = ItemContainer()
        self.dirs_files = ItemContainer()
        self.children = tuple(file_children + dir_children)

        if file_children or dir_children:
            logger.debug(f"Setting children of {self} on __init__ .")
            self.setChildren(file_children, dir_children)

    def setChildren(
        self, file_children: List[FileItem] = [], dir_children: List["DirItem"] = []
    ) -> None:
        for file_child in file_children:
            file_child.parent = self
            self.files.addItem(file_child)
            self.dirs_files.addItem(file_child)

        for dir_child in dir_children:
            dir_child.parent = self
            self.dirs.addItem(dir_child)
            self.dirs_files.addItem(dir_child)

        self.children = tuple(file_children + dir_children)

        logger.debug(f"File children of {self} are {file_children}.")
        logger.debug(f"Dir children of {self} are {dir_children}.")

        self.setDirSize()

    def _getSize(self) -> int:
        sum_size = 0
        sum_size += sum([child.size for child in self.children])
        return sum_size

    def getFullPath(self) -> str:
        return f"{Path(self.dirpath, self.name)}{os.path.sep}"

    def setDirSize(self) -> None:
        """Calculate size from all direct children and set it."""
        self.size = self._getSize()