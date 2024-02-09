import pytest
from anytree.search import find_by_attr
from typing import Tuple, Generator
from utils import (
    renderTreeStr,
)

from hdhog.tree import FSTree
from hdhog.item import Item, DirItem, FileItem


class TestFSTree:
    """Test only the tree-related logic."""

    def testConstructedTree(self, constructed_tree) -> None:
        """Quick check if the dummy tree of ``createSimpleTree()`` looks as intended."""

        tree = constructed_tree
        true_init_tree = """D0    10    d0/
├── F0    5    f0
└── D1    5    d1/
    └── F1    5    f1
"""

        assert renderTreeStr(tree.root_node) == true_init_tree

    def testDeleteSubtree(self, constructed_tree):
        rm_iid = "F1"
        tree = constructed_tree
        tree.deleteSubtree(rm_iid)

        true_del_tree = """D0    5    d0/
├── F0    5    f0
└── D1    0    d1/
"""
        assert renderTreeStr(tree.root_node) == true_del_tree


#
# def testDeleteFileNode() -> None:
#     root, file_container, dir_container = createSimpleTree()
#     tree = FSTree(root)
#     del_iid = "f1"
#
#     node = find_by_attr(root, del_iid, name="iid")
#     parent = node.parent
#
#     try:
#         tree.deleteSubtree(node, file_container, dir_container, [])
#     except FileNotFoundError:
#         # exception thrown by file / dir delete
#         # OK, since here only abstract functionality of
#         # the tree is tested
#         pass
#
#     assert find_by_attr(root, del_iid, name="iid") is None
#
#     with pytest.raises(ValueError):
#         parent.files.itemcontainer.index(node)
#
#     with pytest.raises(ValueError):
#         parent.dirs_files.itemcontainer.index(node)
#
#     true_del_tree = """d0    150000    /bla/d0/
# ├── f0    100000    /bla/d0/f0
# └── d1    50000    /bla/d0/d1/
#     └── d2    50000    /bla/d1/d2/
#         └── f2    50000    /bla/d2/f2
# """
#     assert renderTreeStr(root) == true_del_tree
#
#
# def testdeleteDirNode() -> None:
#     root, file_container, dir_container = createSimpleTree()
#     tree = FSTree(root)
#     del_iid = "d2"
#
#     node = find_by_attr(root, del_iid, name="iid")
#     parent = node.parent
#     try:
#         tree.deleteSubtree(node, file_container, dir_container, [])
#     except FileNotFoundError:
#         # exception thrown by file / dir delete
#         # OK, since here only abstract functionality of
#         # the tree is tested
#         pass
#
#     assert find_by_attr(root, del_iid, name="iid") is None
#
#     with pytest.raises(ValueError):
#         parent.dirs.itemcontainer.index(node)
#
#     with pytest.raises(ValueError):
#         parent.dirs_files.itemcontainer.index(node)
#
#     true_del_tree = """d0    150000    /bla/d0/
# ├── f0    100000    /bla/d0/f0
# └── d1    50000    /bla/d0/d1/
#     └── f1    50000    /bla/d1/f1
# """
#
#     assert renderTreeStr(root) == true_del_tree
#
#
# def testCreateTreeFromFS(create_tree_on_fs: Generator) -> None:
#     dirtree, dirs_sizes, files_sizes = create_tree_on_fs
#     tree = FSTree()
#     for (
#         _,
#         _,
#     ) in tree.createTreeFromFS(dirtree):
#         pass
#
#     assert renderTreeStr(tree.root_node) == render_init
