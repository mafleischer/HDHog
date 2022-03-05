from anytree.search import findall, find_by_attr
from abc import ABC, abstractclassmethod

from typing import TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from catalogue import CatalogueItem


class Tree(ABC):
    @abstractclassmethod
    def deleteByIDs(self, iids: Tuple[str]) -> "CatalogueItem":
        pass

    @abstractclassmethod
    def deleteSubtree(self, node: "CatalogueItem"):
        pass

    @abstractclassmethod
    def moveSubtree(self, node: "CatalogueItem"):
        pass

    @abstractclassmethod
    def updateAncestorsSize(node: "CatalogueItem"):
        pass

    @abstractclassmethod
    def rmNodeFromParent(node):
        pass


class DataTree(Tree):
    def __init__(self, root_node: "CatalogueItem"):
        self.root_node = root_node
        self.file_iid = 0
        self.dir_iid = 0

    def deleteByIDs(self, iids: Tuple[str]) -> "CatalogueItem":
        deleted = []
        for iid in sorted(iids):
            node = find_by_attr(self.root_node, iid, name="iid")
            if node:
                deleted.append(node)
                self.deleteSubtree(node)
        return deleted

    def deleteSubtree(self, node: "CatalogueItem"):
        if node.children:
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

    def moveSubtree(self, node: "CatalogueItem"):
        pass

    def rmNodeFromParent(self, node: "CatalogueItem"):
        if node.parent:
            p_children = [ch for ch in node.parent.children if ch != node]
            node.parent.children = tuple(p_children)

            node.parent.dirs_files.removeItemByValue(node)

            logger.debug(f"Removing node {node}")
            logger.debug(f"Parent {node.parent}")

            for file in node.parent.files:
                logger.debug(f"file in parent files {file}")

            if node in node.parent.files:
                node.parent.files.removeItemByValue(node)
            else:
                node.parent.dirs.removeItemByValue(node)

    def updateAncestorsSize(self, node: "CatalogueItem"):
        parent = node.parent
        while parent:
            parent.calcSetDirSize()
            parent = parent.parent

    def insertData(self, directory, file_children, dir_children):
        pass
