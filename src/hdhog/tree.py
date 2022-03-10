import os
from anytree.search import findall, find_by_attr
from abc import ABC, abstractclassmethod
from typing import Tuple, Optional

from container import CatalogueItem, FileItem, DirItem
from logger import logger


class Tree(ABC):
    @abstractclassmethod
    def deleteByIDs(self, iids: Tuple[str]) -> CatalogueItem:
        pass

    @abstractclassmethod
    def deleteSubtree(self, node: CatalogueItem):
        pass

    @abstractclassmethod
    def moveSubtree(self, node: CatalogueItem):
        pass

    @abstractclassmethod
    def updateAncestorsSize(node: CatalogueItem):
        pass

    @abstractclassmethod
    def rmNodeFromParent(node):
        pass


class DataTree(Tree):
    def __init__(self, root_node: CatalogueItem = None):
        self.root_node = root_node
        self.file_iid = 0
        self.dir_iid = 0
        self.mirror_trees = []

    def deleteByIDs(self, iids: Tuple[str]) -> CatalogueItem:
        deleted = []
        for iid in sorted(iids):
            node = find_by_attr(self.root_node, iid, name="iid")
            if node:
                deleted.append(node)
                self.deleteSubtree(node)
        return deleted

    def deleteSubtree(self, node: CatalogueItem):
        if node.children:
            for file_item in node.files:
                if file_item in node.parent.files:
                    logger.debug(f"del file in parent.files")
                file_item.parent = None
                if file_item in node.parent.files:
                    logger.debug(f"del file in parent.files")
            for dir_item in node.dirs:
                if dir_item.dirs:
                    self.deleteSubtree(dir_item)
                else:
                    dir_item.parent = None

        self.rmNodeFromParent(node)
        self.updateAncestorsSize(node)
        node.parent = None

    def moveSubtree(self, node: CatalogueItem):
        pass

    def rmNodeFromParent(self, node: CatalogueItem):
        if node.parent:
            p_children = [ch for ch in node.parent.children if ch != node]
            node.parent.children = tuple(p_children)

            node.parent.dirs_files.removeItemByValue(node)

            logger.debug(f"Removing node {node}")
            logger.debug(f"Parent {node.parent}")
            logger.debug(f"node type {type(node)}")

            for file in node.parent.files:
                logger.debug(f"file in parent files {file}")

            if node in node.parent.files:
                node.parent.files.removeItemByValue(node)
            else:
                node.parent.dirs.removeItemByValue(node)

    def updateAncestorsSize(self, node: CatalogueItem):
        parent = node.parent
        while parent:
            parent.calcSetDirSize()
            parent = parent.parent

    def findByID(self, iid: str) -> Optional[CatalogueItem]:
        item = find_by_attr(self.root_node, iid, name="iid")
        logger.debug(f"DataTree findByID item {iid} {item}")
        if item:
            return item
        else:
            return None

    def treeFromFSBottomUp(self, start):
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

        roots = {}
        dir_iids = 0
        file_iids = 0

        def _raiseWalkError(oserror: OSError):
            """By default os.walk ignores errors. With this
            function passed as onerror= parameter exceptions are
            raised.

            Args:
                oserror (OSError): instance

            Raises:
                oserror:
            """
            raise oserror

        # do a rstrip, otherwise basename below will be empty
        for parent, dirs, files in os.walk(
            start.rstrip("/"), topdown=False, followlinks=False, onerror=_raiseWalkError
        ):

            # make directories always have a / or \ after name for easy distinction
            parent_name = f"{os.path.basename(parent)}{os.path.sep}"
            parent_dirpath = os.path.dirname(parent)

            file_children = []

            for file in sorted(files):

                if os.path.islink(os.path.join(parent, file)):
                    continue

                fi = FileItem(f"F{self.file_iid}", parent, file)
                fi.size = os.path.getsize(os.path.join(parent, file))

                file_children.append(fi)
                self.file_iid += 1

            # this is in "leaf directories"; no dir children
            if not dirs:
                d_id = f"D{self.dir_iid}"
                parent_di = DirItem(
                    d_id, parent_dirpath, parent_name, file_children, []
                )
                roots[parent] = parent_di

                yield (parent_di, file_children, [])

                for mirror_tree in self.mirror_trees:
                    mirror_tree.insertDirItem(parent_di)

            # in upper directories subdirectories are roots at first
            else:
                dir_children = []
                symlink_dirs = []
                for d in sorted(dirs):
                    dirpath = os.path.join(parent, d)

                    if os.path.islink(dirpath):
                        symlink_dirs.append(dirpath)
                        continue

                    dir_children.append(roots[dirpath])

                # the former roots have a parent now, so remove from them from roots
                for d in dirs:
                    dirpath = os.path.join(parent, d)
                    if dirpath not in symlink_dirs:
                        del roots[dirpath]

                d_iid = f"D{self.dir_iid}"
                parent_di = DirItem(
                    d_iid, parent_dirpath, parent_name, file_children, dir_children,
                )

                roots[parent] = parent_di

                yield (parent_di, file_children, [])

                for mirror_tree in self.mirror_trees:
                    mirror_tree.insertDirItem(parent_di)

            self.dir_iid += 1

        self.root_node = list(roots.items())[0][1]

    def registerMirrorTree(self, tree: Tree):
        self.mirror_trees.append(tree)
