from typing import Generator, Tuple

import pytest
from anytree.search import find_by_attr
from utils import renderTreeStr

from hdhog.item import DirItem, FileItem, Item
from hdhog.tree import FSTree


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


class TestWithFS:
    """Test functionality with files on the FS."""

    def testTreeFromFS(self, create_tree_on_fs):
        """Test tree creation from FS."""
        root, dir_sizes, files_sizes = create_tree_on_fs
        tree = FSTree()
        tree.createTreeFromFS(root)
        true_fs_tree = """D5    55555000    dirtree/
├── D4    500000    dir_0/
│   ├── F8    400000    file1.txt
│   └── F9    100000    file2.txt
└── D3    55055000    dir_1/
    ├── F6    1000000    file1.pdf
    ├── F7    4000000    file2.mp3
    └── D2    50055000    dir_2/
        ├── F4    40000    file2.mp3
        ├── F5    10000    file3.odt
        ├── D1    50000000    dir_3/
        │   ├── F2    40000000    file4.iso
        │   └── F3    10000000    file5.mp4
        └── D0    5000    dir_4/
            ├── F0    4000    code100.py
            └── F1    1000    code101.c
"""
        render_tree = renderTreeStr(tree.root_node)
        assert true_fs_tree == render_tree
        # print(render_tree)
        # print(dir_sizes)
        # print(files_sizes)

        # node = find_by_attr(root, del_iid, name="iid")
        # parent = node.parent

    def testDeleteFile(self, create_tree_on_fs):
        """Test tree creation from FS."""
        root, dir_sizes, files_sizes = create_tree_on_fs
        tree = FSTree()
        tree.createTreeFromFS(root)
        true_fs_tree = """D5    45555000    dirtree/
├── D4    500000    dir_0/
│   ├── F8    400000    file1.txt
│   └── F9    100000    file2.txt
└── D3    45055000    dir_1/
    ├── F6    1000000    file1.pdf
    ├── F7    4000000    file2.mp3
    └── D2    40055000    dir_2/
        ├── F4    40000    file2.mp3
        ├── F5    10000    file3.odt
        ├── D1    40000000    dir_3/
        │   └── F2    40000000    file4.iso
        └── D0    5000    dir_4/
            ├── F0    4000    code100.py
            └── F1    1000    code101.c
"""
        del_iid = "F3"
        tree.deleteSubtree(del_iid)
        render_tree = renderTreeStr(tree.root_node)
        assert true_fs_tree == render_tree


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
