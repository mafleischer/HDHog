import shutil
import pytest
import unittest
from anytree.search import find_by_attr
from utils import (
    createFSDirTree,
    renderTreeStr,
    render_init,
    render_del_file,
    render_del_dir,
)

from hdhog.tree import FSTree
from hdhog.container import CatalogueContainer, CatalogueItem, DirItem, FileItem


def createSimpleTree():
    node_0 = DirItem("d0", "/bla/", "d0")
    node_1 = FileItem("f0", "/bla/d0/", "f0")
    node_1.size = 100000

    node_2 = DirItem("d1", "/bla/d0/", "d1")
    node_3 = FileItem("f1", "/bla/d1/", "f1")
    node_3.size = 50000

    node_4 = DirItem("d2", "/bla/d1/", "d2")
    node_5 = FileItem("f2", "/bla/d2/", "f2")
    node_5.size = 50000

    node_4.setChildren(file_children=[node_5])
    node_2.setChildren(file_children=[node_3], dir_children=[node_4])
    node_0.setChildren(file_children=[node_1], dir_children=[node_2])

    # containers as in Catalogue.files and Catalogue.dirs
    file_container = CatalogueContainer()
    dir_container = CatalogueContainer()

    for f_item in (node_1, node_3, node_5):
        file_container.addItem(f_item)
    for d_item in (node_0, node_2, node_4):
        dir_container.addItem(d_item)

    return node_0, file_container, dir_container


def testCreateManualTree():
    """Quick check if the dummy tree of ``createSimpleTree()`` looks as intended."""

    root, _, _ = createSimpleTree()
    true_init_tree = """d0    200000    /bla/d0/
├── f0    100000    /bla/d0/f0
└── d1    100000    /bla/d0/d1/
    ├── f1    50000    /bla/d1/f1
    └── d2    50000    /bla/d1/d2/
        └── f2    50000    /bla/d2/f2
"""

    assert renderTreeStr(root) == true_init_tree


def testDeleteFileNode():
    root, file_container, dir_container = createSimpleTree()
    tree = FSTree(root)
    del_iid = "f1"

    node = find_by_attr(root, del_iid, name="iid")
    parent = node.parent

    try:
        tree.deleteSubtree(node, file_container, dir_container, [])
    except FileNotFoundError:
        # exception thrown by file / dir delete
        # OK, since here only abstract functionality of
        # the tree is tested
        pass

    assert find_by_attr(root, del_iid, name="iid") is None

    with pytest.raises(ValueError):
        parent.files.container.index(node)

    with pytest.raises(ValueError):
        parent.dirs_files.container.index(node)

    true_del_tree = """d0    150000    /bla/d0/
├── f0    100000    /bla/d0/f0
└── d1    50000    /bla/d0/d1/
    └── d2    50000    /bla/d1/d2/
        └── f2    50000    /bla/d2/f2
"""
    assert renderTreeStr(root) == true_del_tree


def testdeleteDirNode():
    root, file_container, dir_container = createSimpleTree()
    tree = FSTree(root)
    del_iid = "d2"

    node = find_by_attr(root, del_iid, name="iid")
    parent = node.parent
    try:
        tree.deleteSubtree(node, file_container, dir_container, [])
    except FileNotFoundError:
        # exception thrown by file / dir delete
        # OK, since here only abstract functionality of
        # the tree is tested
        pass

    assert find_by_attr(root, del_iid, name="iid") is None

    with pytest.raises(ValueError):
        parent.dirs.container.index(node)

    with pytest.raises(ValueError):
        parent.dirs_files.container.index(node)

    true_del_tree = """d0    150000    /bla/d0/
├── f0    100000    /bla/d0/f0
└── d1    50000    /bla/d0/d1/
    └── f1    50000    /bla/d1/f1
"""

    assert renderTreeStr(root) == true_del_tree


def testCreateTreeFromFS(test_catalogue):
    dirtree, dirs_sizes, files_sizes = test_catalogue
    tree = FSTree()
    for _, _, in tree.treeFromFSBottomUp(dirtree):
        pass

    assert renderTreeStr(tree.root_node) == render_init
