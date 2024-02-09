from collections.abc import Iterable
import os
from abc import ABC, abstractmethod
from types import new_class
from anytree.search import find_by_attr
from pathlib import Path
from typing import List, Sequence, Optional, Generator, Callable

from .item import Item, FileItem, DirItem
from .factory import createItem
from .itemupdate import updateItemSize
from .globalinventory import GlobalInventory
from .logger import logger


class FSTree:
    def __init__(
        self,
        root_node: Optional[Item] = None,
    ):
        self.root_node = root_node
        self.global_inventory = GlobalInventory()

    def createTreeFromFS(self, full_start_path: str) -> None:
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
            This is in "leaf directories", so the algorithm full_start_paths with
            these as the bottom-most roots.

            Else create a DirItem with the subdirectories, which are now not
            roots anymore and are removed from the roots dict, as children as
            well, make it their parent and store it in the roots dict.
            Insert into directory container.

        The algorithm terminates with setting the topmost directory as the root
        item / node.

        Symlinks are skipped.

        Args:
            full_start_path (str, optional): full_start_path of the walk..

        Raises:
            oserror: when os.walk fails

        Yields:
            Tuple[DirItem, List[FileItem]]: A parent DirItem and its file children
        """

        roots = {}

        def _raiseWalkError(oserror: OSError) -> None:
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
        for parent_path, dirs, files in os.walk(
            str(full_start_path).rstrip("/"),
            topdown=False,
            followlinks=False,
            onerror=_raiseWalkError,
        ):
            # the string in parent_path are full paths
            # dirs and files are only the names

            parent_name = Path(parent_path).name
            grandparent_path = Path(parent_path).parent
            parent_dir_item = createItem("dir", grandparent_path, parent_name)

            file_children = []

            for file_name in sorted(files):
                file_path = Path(parent_path, file_name)

                if file_path.is_symlink():
                    logger.debug(f"Skipping link {file_path}.")
                    continue

                file_item = createItem("file", parent_path, file_name)
                file_item.setSizeFromFS()

                self.global_inventory.addItem(file_item)
                file_children.append(file_item)

            if not dirs:
                # this is in leaf directories; no dir children
                self.global_inventory.addItem(parent_dir_item)
                roots[parent_path] = parent_dir_item
            else:
                # in upper directories subdirectories were roots in prior iterations
                # get the objects from roots dict
                dir_children = []
                symlink_dirs = []
                # TODO: refactor vvv
                for dir_name in sorted(dirs):
                    dir_path = Path(parent_path, dir_name)

                    if dir_path.is_symlink():
                        symlink_dirs.append(dir_path)
                        logger.debug(f"Skipping link {dir_path}.")
                        continue

                    # the former roots have a parent now, so remove from them from roots
                    del roots[str(dir_path)]

                    dir_children.append(roots[str(dir_path)])

                self.global_inventory.addItem(parent_dir_item)

                roots[parent_path] = parent_dir_item

        self.root_node = list(roots.items())[0][1]

    def deleteSubtree(self, iid: str) -> None:
        item = self.global_inventory.removeItem(iid)
        parent = item.parent
        item.parent = None

        # update all ancestors
        while parent:
            new_parent_size = parent.item_size - item.item_size
            updateItemSize(parent, new_parent_size, self.global_inventory)
            parent = parent.parent

    def getMinDelItems(iid_list: Sequence[str]):
        """Of a sequence of to-be-deleted items remove unnecessary items.

        Remove items ancestors of which are to be deleted as well.
        The result is one or several unconnected items. For dirs the whole
        sub-tree will then be deleted.
        """
