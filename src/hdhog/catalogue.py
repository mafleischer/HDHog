from __future__ import annotations
import os
from sortedcontainers import SortedKeyList
from anytree.search import findall
from abc import ABC, abstractclassmethod

from tree import DataTree
from container import CatalogueContainer, FileItem, DirItem
from logger import logger


class Catalogue:
    """This represents the walking of the directory tree and holding the resulting
    information, as well as actions taken on catalogue items, i.e. files and directories.
    This class holds three central structures / elements:
        1. A CatalogueContainer for files, which is just for file-based sorting
        2. A CatalogueContainer for directories, which is just for
        directory-based sorting
        3. The root node of the directory tree. Nodes in the tree are
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
        """Walk the directory tree and put items into containers and the tree.

        This wraps os.walk() with topdown=False, so it builds the tree bottom up.
        This is so the sizes of the directories can be calculated directly
        when building the tree.

        Algorithm:

        1. Iterate over the files and put them in FileItems, insert into the
        files container

        2. Iterate over the directories.
            If it has no subdirectories create a DirItem for the parent
            directoy with just the files as children and store the
            DirItem as a root. Insert into directory container.
            This is in "leaf directories", so the algorithm starts with
            these as the bottom-most roots.
            
            Else create a DirItem with the subdirectories, which are now not
            roots anymore and are removed from the roots dict, as children as
            well, make it their parent and store it in the roots dict.
            Insert into directory container.

        The algorithm terminates with setting the topmost directory as the root
        item / node of self.tree
                
        Symlinks are skipped.

        Size calculation of the items is handled by the item objects on creation.

        Args:
            start (str, optional): Start of the walk. Defaults to "/".
        """

        self.files = CatalogueContainer()
        self.dirs = CatalogueContainer()

        for dir_item, file_items, dir_items in self.tree.treeFromFSBottomUp(
            start=start
        ):
            self.dirs.addItem(dir_item)
            for item in file_items:
                self.files.addItem(item)
            for item in dir_items:
                self.dirs.addItem(item)

        # roots = {}
        # dir_iids = 0
        # file_iids = 0

        # def _raiseWalkError(oserror: OSError):
        #     """By default os.walk ignores errors. With this
        #     function passed as onerror= parameter exceptions are
        #     raised.

        #     Args:
        #         oserror (OSError): instance

        #     Raises:
        #         oserror:
        #     """
        #     raise oserror

        # # do a rstrip, otherwise basename below will be empty
        # for parent, dirs, files in os.walk(
        #     start.rstrip("/"), topdown=False, followlinks=False, onerror=_raiseWalkError
        # ):

        #     # make directories always have a / or \ after name for easy distinction
        #     parent_name = f"{os.path.basename(parent)}{os.path.sep}"
        #     parent_dirpath = os.path.dirname(parent)

        #     file_children = []

        #     for file in sorted(files):

        #         if os.path.islink(os.path.join(parent, file)):
        #             continue

        #         fi = FileItem(f"F{file_iids}", parent, file, hash_files=self.hash_files)
        #         fi.size = os.path.getsize(os.path.join(parent, file))

        #         file_children.append(fi)

        #         self.files.addItem(fi)
        #         file_iids += 1

        #     # this is in "leaf directories"; no dir children
        #     if not dirs:
        #         d_id = f"D{dir_iids}"
        #         parent_di = DirItem(
        #             d_id, parent_dirpath, parent_name, file_children, []
        #         )
        #         roots[parent] = parent_di
        #         self.dirs.addItem(parent_di)

        #         for mirror_tree in self.mirror_trees:
        #             mirror_tree.insertDirItem(parent_di)

        #     # in upper directories subdirectories are roots at first
        #     else:
        #         dir_children = []
        #         symlink_dirs = []
        #         for d in dirs:
        #             dirpath = os.path.join(parent, d)

        #             if os.path.islink(dirpath):
        #                 symlink_dirs.append(dirpath)
        #                 continue

        #             dir_children.append(roots[dirpath])

        #         # the former roots have a parent now, so remove from them from roots
        #         for d in dirs:
        #             dirpath = os.path.join(parent, d)
        #             if dirpath not in symlink_dirs:
        #                 del roots[dirpath]

        #         d_iid = f"D{dir_iids}"
        #         parent_di = DirItem(
        #             d_iid, parent_dirpath, parent_name, file_children, dir_children,
        #         )

        #         roots[parent] = parent_di
        #         self.dirs.addItem(parent_di)

        #         for mirror_tree in self.mirror_trees:
        #             mirror_tree.insertDirItem(parent_di)

        #     dir_iids += 1

        # root_node = list(roots.items())[0][1]
        # self.tree = DataTree(root_node)

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

    # def deleteByIDs(selection: Tuple[str]):
    #     self.tree.deleteByIDs(selection)

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
        items = findall(
            self.tree.root_node, filter_=lambda item: item.getFullPath() in paths
        )

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
