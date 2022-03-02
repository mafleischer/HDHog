from __future__ import annotations
import os
import shutil
import logging

from sortedcontainers import SortedKeyList
from anytree import NodeMixin
from anytree.search import findall

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
    """This represents the walking of the directory tree as well as actions
    taken on catalogue items, i.e. files and directories.
    This class holds three central structures / elements:
        1. A CatalogueContainer for files, which is just for file-based sorting
        2. A CatalogueContainer for directories, which is just for
        directory-based sorting
        3. The root node of the directory tree. Nodes in the tree are
        FileItems or DirItems which inherit from anytree's NodeMixin.
        Each node in turn holds CatalogueContainers for holding children
        items.
    """

    def __init__(self, hash_files=False):
        # self.filter_checks = []
        self.files = CatalogueContainer()
        self.dirs = CatalogueContainer()
        self.rootdir = None
        self.hash_files = hash_files

    def createCatalogue(self, start="/"):
        """Walk the directory tree and put items into containers and the tree.

        This wraps os.walk() with topdown=False, so it builds the tree bottom up.
        This is so the sizes of the directories can be calculated directly
        when building the tree.

        Algorithm:

        1. Go over the files and put them in FileItems, insert into the
        files container

        2. Go over the directories.
            If it has no subdirectories create a DirItem for the parent
            directoy with just the files as children and store the
            DirItem as a root. Insert into directory container.
            This is in "leaf directories", so the algorithm starts with
            these as the bottom-most roots.
            
            Else create a DirItem with the subdirectories, which are now not
            roots anymore and are removed from the roots dict, as children as
            well, make it their parent and store it in the roots dict.
            Insert into directory container.
        
        Size calculation of the items is handled by the objects on creation.

        Args:
            start (str, optional): Start of the walk. Defaults to "/".
        """

        self.files = CatalogueContainer()
        self.dirs = CatalogueContainer()
        roots = {}

        # do a rstrip, otherwise basename below will be empty
        for parent, dirs, files in os.walk(
            start.rstrip("/"), topdown=False, followlinks=False
        ):

            file_children = []

            for file in sorted(files):
                if os.path.islink(os.path.join(parent, file)):
                    continue
                fi = FileItem(parent, file, hash_files=self.hash_files)
                file_children.append(fi)

                self.files.addItem(fi)

            # make directories always have a / or \ after name for easy distinction
            parent_name = f"{os.path.basename(parent)}{os.path.sep}"
            parent_dirpath = os.path.dirname(parent)

            if not dirs:  # this is in "leaf directories"
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

    def actionOnPaths(self, fs_action: Action, paths: List[str]):
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
        items = findall(self.rootdir, filter_=lambda item: item.getFullPath() in paths)

        for item in items:

            logger.debug(f"Action on {item.getFullPath()}")

            parent = item.parent

            if isinstance(item, FileItem):
                self.files.removeItemByValue(item)
                if parent:
                    parent.files.removeItemByValue(item)

            if isinstance(item, DirItem):
                self.dirs.removeItemByValue(item)
                if parent:
                    parent.dirs.removeItemByValue(item)

            # recalculate and set size of all parents up the tree

            if parent:
                parent.dirs_files.removeItemByValue(item)
                parent.children = [child for child in parent.children if child != item]
                parent.calcSetDirSize()

                parent = parent.parent
                while parent:
                    parent.calcSetDirSize()
                    parent = parent.parent

            fs_action.execute(item)


class CatalogueItem(ABC, NodeMixin):
    """This is the ABC class for an item held in the catalogue
    container. It's an anytree node as well.

    size = size in bytes
    """

    __slots__ = ["size", "dirpath", "name"]

    def __init__(self, dirpath: str, name: str):
        super().__init__()
        self.dirpath = dirpath
        self.name = name

    def __str__(self):
        return self.getFullPath()

    def __repr__(self):
        return self.getFullPath()

    def getFullPath(self) -> str:
        return os.path.join(self.dirpath, self.name)


class FileItem(CatalogueItem):
    __slots__ = ["type", "hash"]

    def __init__(self, dirpath: str, name: str, hash_files: bool):
        super().__init__(dirpath, name)
        self.setFileInfo(dirpath, name, hash_files)

    def setFileInfo(self, dirpath: str, name: str, hash: bool):
        self.size = os.path.getsize(os.path.join(dirpath, name))
        self.type = os.path.splitext(self.name)[1]


class DirItem(CatalogueItem):
    """Holds children as well.
    It has three CatalogueContainers, two for holding and sorting files and
    directories separately, and one for holding and sorting both together.
    
    The size is calculated on creation from all direct children.
    """

    __slots__ = ["files"]

    def __init__(
        self,
        dirpath: str,
        name: str,
        file_children: List[FileItem],
        dir_children: List[DirItem],
    ):
        super().__init__(dirpath, name)
        self.files = CatalogueContainer()
        self.dirs = CatalogueContainer()
        self.dirs_files = CatalogueContainer()
        self.children = file_children + dir_children

        for file_child in file_children:
            file_child.parent = self
            self.files.addItem(file_child)
            self.dirs_files.addItem(file_child)

        for dir_child in dir_children:
            dir_child.parent = self
            self.dirs.addItem(dir_child)
            self.dirs_files.addItem(dir_child)

        self.calcSetDirSize()

    def calcSetDirSize(self):
        """Calculate size from all direct children and set it.
        """
        sum_size = 0
        sum_size += sum([child.size for child in self.children])
        self.size = sum_size


class CatalogueContainer:
    """Holds CatalogueItems (actual objects) and provides sorting thereof.
    """

    def __init__(self):
        self.container = SortedKeyList(
            key=lambda item: (-item.size, item.dirpath, item.name,)
        )

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

    # def popItemsFromIndices(self, indices: List[int]) -> List[CatalogueItem]:
    #     items = []

    #     for ix in indices:
    #         items.append(self.container.pop(ix))

    #     return items

    def removeItemByValue(self, item: CatalogueItem):
        self.container.remove(item)

    def getAllPathsAndSizes(self) -> List[Tuple[str, str]]:
        paths_size = []

        for item in self.container:
            paths_size.append((item.getFullPath(), item.getSize()))

        return paths_size


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


class Action(ABC):
    """Base class for file system actions"""

    @abstractclassmethod
    def execute(self, catalogue_item: CatalogueItem):
        pass


class ActionDelete(Action):
    def execute(self, item: CatalogueItem):
        path = item.getFullPath()
        try:
            os.remove(path)
        except FileNotFoundError:
            logger.error("Error deleting file: File not found.")
            raise FileNotFoundError
        except IsADirectoryError:
            shutil.rmtree(path)


class ActionMoveTo(Action):
    def __init__(self, dest_path: str):
        self.dest_path = dest_path

    def execute(self, item: CatalogueItem):
        path = item.getFullPath()
        shutil.move(path, self.dest_path)
