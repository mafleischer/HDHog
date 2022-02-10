from dataclasses import dataclass
from queue import PriorityQueue
from abc import ABC, abstractclassmethod
from hashlib import sha256


@dataclass(frozen=True, order=True)
class File:
    size: int
    path: str
    name: str
    filetype: str
    filehash: str


class Search:

    filter_checks = []

    def searchLargestFiles(self):
        pass

    def walkDir()

    def addFilterCheck(self, filter_check: FilterCheck):
        pass


class FilterCheck(ABC):
    @abstractclassmethod
    def check(self, filepath: str, *args):
        pass


class FilterCheckFileExt(FilterCheck):
    def check(self, filepath: str, *extensions):
        pass


class SearchResultsContainer:

    container = []

    def feedContent(self):
        pass

    def deleteContent(self):
        pass

    def returnContent(self):
        pass
