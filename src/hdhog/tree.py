import os
from anytree.search import findall, find_by_attr
from abc import ABC, abstractclassmethod
from typing import Tuple, List, Optional

from .container import CatalogueItem, FileItem, DirItem
from .logger import logger


class Tree(ABC):
    @abstractclassmethod
    def deleteByIDs(self, iids: Tuple[str]) -> CatalogueItem:
        pass

    @abstractclassmethod
    def deleteSubtree(self, node: CatalogueItem):
        pass

    @abstractclassmethod
    def updateAncestorsSize(node: CatalogueItem):
        pass


class DataTree(Tree):
    def __init__(self, root_node: CatalogueItem = None):
        self.root_node = root_node
        self.file_iid = 0  # counter for file iids
        self.dir_iid = 0  # counter for dir iids
        self.mirror_trees = []

    def deleteByIDs(self, iids: Tuple[str]) -> List[CatalogueItem]:
        deleted = []
        logger.debug(f"Deleting iids {iids} from tree.")
        for iid in sorted(iids):
            node = find_by_attr(self.root_node, iid, name="iid")
            if node:
                deleted.append(node)
                self.deleteSubtree(node)
        logger.debug(f"Deleted items {deleted} and children from tree.")
        return deleted

    def deleteSubtree(self, node: CatalogueItem):
        logger.debug(f"Detaching node {node}.")
        if node.children:
            logger.debug(f"Detaching all children of {node}")
            for file_item in node.files:
                file_item.parent = None
            for dir_item in node.dirs:
                if dir_item.dirs:
                    self.deleteSubtree(dir_item)
                else:
                    dir_item.parent = None

        self.rmNodeFromParent(node)
        self.updateAncestorsSize(node)
        node.parent = None

    def rmNodeFromParent(self, node: CatalogueItem):
        """Remove a node from all of its parent's structures

        Args:
            node (CatalogueItem): To-be-remove-node
        """
        if node.parent:
            logger.debug(f"Remove node {node} from parent structures.")
            p_children = [ch for ch in node.parent.children if ch != node]
            node.parent.children = tuple(p_children)

            node.parent.dirs_files.removeItemByValue(node)

            if node in node.parent.files:
                node.parent.files.removeItemByValue(node)
            else:
                node.parent.dirs.removeItemByValue(node)

    def updateAncestorsSize(self, node: CatalogueItem):
        """Update sizes of all ancestors of a node that has already been removed
        from parent's structures

        Args:
            node (CatalogueItem): removed node
        """
        logger.debug(f"Update ancestors of {node}")
        parent = node.parent
        while parent:
            logger.debug(f"Updating size of ancestor {parent}.")
            parent.calcSetDirSize()
            parent = parent.parent

    def findByID(self, iid: str) -> Optional[CatalogueItem]:
        """Find node by its iid string and return it.

        Args:
            iid (str): iid

        Returns:
            Optional[CatalogueItem]: item or None
        """
        item = find_by_attr(self.root_node, iid, name="iid")
        if item:
            return item
        else:
            return None

    def treeFromFSBottomUp(self, start):
        """Generator that walks the directory tree and builds the tree from the items.

        This wraps os.walk() with topdown=False, so it builds the tree bottom up.
        This is so the sizes of the directories can be calculated directly
        when building the tree.

        Implemented as generator so outside calling functions can keep track
        simultaneously and do stuff with the created items.

        Algorithm:

        1. Iterate over the files and put them in FileItems.

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
        item / node.
  
        Symlinks are skipped.

        Args:
            start (str, optional): Start of the walk..
        """

        roots = {}

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
                    logger.debug(f"Skipping link {os.path.join(parent, file)}.")
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
                        logger.debug(f"Skipping link {dirpath}.")
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
