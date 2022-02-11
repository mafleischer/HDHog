from sortedcontainers import SortedKeyList
from abc import ABC, abstractclassmethod
from hashlib import sha256


class Catalogue:

    filter_checks = []

    def createCatalogue(self, start="/"):
        pass

    def addFilterCheck(self, filter_check: FilterCheck):
        pass


class CatalogueItem(ABC):
    __slots__ = ["size", "dirpath", "name"]


class FileItem(CatalogueItem):
    __slots__ = ["type", "hash"]

    def __init__(self, filepath: str, with_hash: bool):
        pass

    def setFileInfo(filepath: str, hash: bool):
        pass


class FilterCheck(ABC):
    @abstractclassmethod
    def check(self, filepath: str):
        pass


class FilterCheckFileExt(FilterCheck):
    def check(self, filepath: str, *extensions):
        pass


class CatalogueContainer(ABC):

    container: SortedKeyList

    def addItem(self, item: CatalogueItem):
        container.add(item)

    def deleteContent(self, indices: list):
        pass

    def viewContent(self):
        pass


class CatalogueFileContainer(CatalogueContainer):
    container = SortedKeyList(
        key=lambda file_item: (
            file_item.size,
            file_item.dirpath,
            file_item.type,
            file_item.name,
        )
    )


class Action(ABC):
    @abstractclassmethod
    def execute(self):
        pass


class ActionDeleteFiles(Action):
    def execute(self, paths):
        pass


class ActionMoveFiles(Action):
    def execute(self, paths, dest):
        pass
