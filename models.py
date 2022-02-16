from __future__ import annotations
import os
import logging

from sortedcontainers import SortedKeyList
from anytree import NodeMixin

from abc import ABC, abstractclassmethod
from hashlib import sha256

from typing import List, Tuple

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
ch = logging.StreamHandler()
ch.setFormatter(formatter)

logger.addHandler(ch)


class Catalogue:
    """This represents the walking of the directory tree.
    """

    def __init__(self, hash_files: bool):
        self.filter_checks = []
        self.files = CatalogueFileContainer()
        self.dirs = CatalogueDirContainer()
        self.rootdir = None
        self.hash_files = hash_files

    def createCatalogue(self, start="/"):
        """Walk the directory tree and put items into container.

        So far this only goes over the files, grabs the info,
        puts it into FileItem objects and puts those into the
        file container.
        Upon action it also deletes the selected items from the
        catalogue.

        Args:
            start (str, optional): Start of the walk. Defaults to "/".
            hash_files (bool, optional): Whether hash sum of files
            shall be computed. Defaults to False.
        """

        roots = {}

        # do a rstrip, otherwise basename below will be empty
        for parent, dirs, files in os.walk(start.rstrip("/"), topdown=False):

            file_children = []

            for file in files:
                fi = FileItem(parent, file, hash_files=self.hash_files)
                file_children.append(fi)

                self.files.addItem(fi)

            parent_name = os.path.basename(parent)
            parent_dirpath = os.path.dirname(parent)

            logger.debug(
                f"parent_dirpath: {parent_dirpath},  parent name: {parent_name}"
            )

            if not dirs:
                parent_di = DirItem(parent_dirpath, parent_name, file_children, [])
                roots[parent] = parent_di
                self.dirs.addItem(parent_di)
            else:
                dir_children = []
                for d in dirs:
                    for root in roots:
                        dirpath = os.path.join(parent, d)
                        if root == dirpath:
                            dir_children.append(roots[root])

                for d in dirs:
                    dirpath = os.path.join(parent, d)
                    del roots[dirpath]

                parent_di = DirItem(
                    parent_dirpath, parent_name, file_children, dir_children
                )
                roots[parent] = parent_di
                self.dirs.addItem(parent_di)

        self.rootdir = list(roots.items())[0][1]

    def addFilterCheck(self, filter_check: FilterCheck):
        """Register a check object.

        Args:
            filter_check (FilterCheck): Check object
        """

        # check if a check of that kind was already added
        if self.filter_checks:
            for ix, registered_check in enumerate(self.filter_checks):
                if type(filter_check) == type(registered_check):
                    del self.filter_checks[ix]

        self.filter_checks.append(filter_check)

    def actionOnIndices(self, action: Action, indices: List[int]):
        items = self.files.popItemsFromIndices(indices)
        for item in items:
            action.execute(item)


class CatalogueItem(ABC, NodeMixin):
    """This is the ABC class for an item held in the catalogue
    container.
    """

    __slots__ = ["size", "dirpath", "name"]

    def __init__(self, dirpath: str, name: str):
        super().__init__()
        self.dirpath = dirpath
        self.name = name

    def getFullPath(self) -> str:
        return os.path.join(self.dirpath, self.name)

    def getSize(self):
        return self.size


class FileItem(CatalogueItem):
    __slots__ = ["type", "hash"]

    def __init__(self, dirpath: str, name: str, hash_files: bool):
        super().__init__(dirpath, name)
        self.setFileInfo(dirpath, name, hash_files)

    def setFileInfo(self, dirpath: str, name: str, hash: bool):
        self.size = os.path.getsize(os.path.join(dirpath, name))

        logger.debug(f"File size for {os.path.join(dirpath, name)} is {self.size}")

        self.type = os.path.splitext(self.name)[1]


class DirItem(CatalogueItem):
    __slots__ = ["files"]

    def __init__(
        self,
        dirpath: str,
        name: str,
        file_children: List[FileItem],
        dir_children: List[DirItem],
    ):
        super().__init__(dirpath, name)
        self.files = CatalogueFileContainer()
        self.children = file_children + dir_children

        for file_child in file_children:
            file_child.parent = self
            self.files.addItem(file_child)

        for dir_child in dir_children:
            dir_child.parent = self

        self.calcSetDirSize()

    def calcSetDirSize(self):
        sum_size = 0
        sum_size += sum([child.getSize() for child in self.children])
        self.size = sum_size


class FilterCheck(ABC):
    """This is the ABC class for a filter check used
    when walking the directory tree in the Catalogue.
    """

    @abstractclassmethod
    def check(self, filepath: str):
        pass


class FilterCheckFileExt(FilterCheck):
    def __init__(self, extensions: List[str]):
        self.extensions = extensions

    def check(self, filepath: str):
        fname, ext = os.path.splitext(filepath)

        if ext.strip(".") in self.extensions:
            return False
        else:
            return True


class CatalogueContainer(ABC):
    """Holds CatalogueItems and provides sorting thereof.
    """

    container: SortedKeyList

    def __len__(self):
        return len(self.container)

    def __contains__(self, path):
        for item in self.container:
            if item.getFullPath() == path:
                return True
        return False

    def __iter__(self):
        return iter(self.container)

    def __getitem__(self, ix):
        return self.container[ix]

    def addItem(self, item: CatalogueItem):
        self.container.add(item)

    def popItemsFromIndices(self, indices: List[int]) -> List[CatalogueItem]:

        items = []

        for ix in indices:
            items.append(self.container.pop(ix))

        return items

    def getPathAndSize(self) -> List[Tuple[str, str]]:
        paths_size = []

        for item in self.container:
            paths_size.append((item.getFullPath(), item.getSize()))

        return paths_size


class CatalogueFileContainer(CatalogueContainer):
    def __init__(self):
        self.container = SortedKeyList(
            key=lambda file_item: (
                -file_item.size,
                file_item.dirpath,
                file_item.type,
                file_item.name,
            )
        )


class CatalogueDirContainer(CatalogueContainer):
    def __init__(self):
        self.container = SortedKeyList(
            key=lambda dir_item: (-dir_item.size, dir_item.dirpath, dir_item.name,)
        )


class Action(ABC):
    @abstractclassmethod
    def execute(self, catalogue_item: CatalogueItem):
        pass


class ActionDeleteFile(Action):
    def execute(self, file_item: FileItem):
        try:
            os.remove(file_item.getFullPath())
        except FileNotFoundError:
            logger.error("Error deleting file: File not found.")


class ActionMoveFileTo(Action):
    def __init__(self, dest):
        self.dest = dest

    def execute(self, file_item):
        pass
