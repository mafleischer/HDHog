import os
import logging

from sortedcontainers import SortedKeyList
from abc import ABC, abstractclassmethod
from hashlib import sha256

from typing import List, Dict, Tuple

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
ch = logging.StreamHandler()
ch.setFormatter(formatter)

logger.addHandler(ch)


class Catalogue:
    """This represents the walking of the directory tree.
    """

    def __init__(self):
        self.filter_checks = []
        self.file_container = CatalogueFileContainer()

    def createCatalogue(self, start="/", hash_files=False):
        """Walk the directory tree and put items into container.

        So far this only goes over the files, grabs the info,
        puts it into FileItem objects and puts those into the
        file container.
        Upon action it also deletes the selected items from the
        catalogue.

        Args:
            start (str, optional): Start of the walk. Defaults to "/".
            hash_files (bool, optional): Whether hash sum of files shall be computed. Defaults to False.
        """

        for root, dirs, files in os.walk(start):

            for file in files:
                filepath = os.path.join(root, file)

                for filter_check in self.filter_checks:
                    if not filter_check.check(filepath):
                        break
                else:
                    fi = FileItem(filepath, hash_files=hash_files)

                    self.file_container.addItem(fi)

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

        filter_checks.append(filter_check)

    def fileActionOnIndices(action: Action, indices: List[int]):
        items = self.file_container.popItemsFromIndices(indices)
        for item in items:
            action.execute(item)


class CatalogueItem(ABC):
    """This is the ABC class for an item held in the catalogue
    container.
    """

    __slots__ = ["size", "dirpath", "name"]

    def getFullPath(self) -> str:
        return os.path.join(self.dirpath, self.name)

    def displayHRSize(self) -> str:
        """From size in bytes compute K, M or G.

        Returns:
            str: human readable size
        """
        return hrsize


class FileItem(CatalogueItem):
    __slots__ = ["type", "hash"]

    def __init__(self, filepath: str, hash_files: bool):
        self.setFileInfo(filepath, hash_files)

    def setFileInfo(filepath: str, hash: bool):
        self.size = os.path.getsize(filepath)
        dirname, fname = os.path.split(filepath)
        self.dirpath = dirname
        self.name = fname
        self.type = os.path.splitext(filepath)[1]


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
    """Holds CatalogueItems and provides sorting therof.
    """

    container: SortedKeyList

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
            paths_size.append((item.getFullPath(), item.displayHRSize()))

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
    def execute(self, file_item, dest):
        pass
