import pytest
import shutil
from typing import Generator

from hdhog.factory import createItem
from hdhog.globalinventory import GlobalInventory

# from typing import Generator
from hdhog.inventory import Inventory
from hdhog.item import DirItem, FileItem, Item, addChildToDir

from utils import createFSDirTree

#
# from utils import (
#     createFSDirTree,
#     renderTreeStr,
#     render_init,
#     render_del_file,
#     render_del_dir,
# )
from hdhog.tree import FSTree


@pytest.fixture
def createItems():
    """Create basic items."""
    fi0 = createItem(
        "file", iid="F0", _dirpath="/test/path", _item_name="fname0", item_size=1
    )
    di0 = createItem(
        "dir",
        iid="D0",
        _dirpath="/test/path",
        _item_name="dname0",
        item_size=0,
    )
    return (fi0, di0)


@pytest.fixture
def global_inventory():
    return GlobalInventory()


@pytest.fixture
def constructed_tree(global_inventory) -> FSTree:
    """Create raw anytree tree data structure with FileItems and DirItems,
    the global file_container (from the files tab) and dir_container (from the
    dir tab)"""

    global_inv = global_inventory

    node_0 = createItem("dir", "/bla", "d0")
    node_1 = createItem("file", "/bla/d0", "f0")
    node_0.item_size = 10
    node_1.item_size = 5

    node_2 = createItem("dir", "/bla/d0", "d1")
    node_3 = createItem("file", "/bla/d0/d1", "f1")
    node_2.item_size = 5
    node_3.item_size = 5

    addChildToDir(node_0, node_1)
    addChildToDir(node_0, node_2)
    addChildToDir(node_2, node_3)

    tree = FSTree(root_node=node_0)

    for n in (node_0, node_1, node_2, node_3):
        global_inv.addItem(n)

    tree.global_inventory = global_inv
    return tree


@pytest.fixture
def create_tree_on_fs(tmp_path) -> Generator:
    dirtree, dirs_and_sizes, files_and_sizes = createFSDirTree(tmp_path)
    yield dirtree, dirs_and_sizes, files_and_sizes
    shutil.rmtree(dirtree)
