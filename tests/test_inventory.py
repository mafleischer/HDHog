import os
import pytest
from anytree.search import find_by_attr
from typing import Generator

# from utils import (
#     renderTreeStr,
#     render_init,
#     render_del_file,
#     render_del_dir,
# )

from hdhog.inventory import Inventory
from hdhog.item import DirItem, FileItem
from hdhog.factory import createItem
from hdhog.logger import logger


class TestInventory:
    @pytest.fixture
    def createInventoryWithItems(self):
        inv = Inventory()
        # fi = FileItem(iid="F0", dirpath="/test/path/", item_name="fname0", item_size=1)
        fi = createItem("file", iid="F0", _dirpath="/test/path/", _item_name="fname0", item_size=1)
        # di = DirItem(iid="D0", dirpath="/test/path/", item_name="dname0", item_size=1)
        di = createItem("dir", iid="D0", _dirpath="/test/path/", _item_name="dname0", item_size=1)
        return inv, fi, di

    def testAddItemsToInventory(self, createInventoryWithItems):
        """Test whether in fixture items were added properly."""
        inv, fi, di = createInventoryWithItems
        inv.addItem(fi)
        inv.addItem(di)
        assert len(inv.per_type_lists[FileItem]) == 1
        assert len(inv.dirs_files) == 2

    def testRemoveItemsFromInventory(self, createInventoryWithItems):
        """Test whether in fixture items were added properly."""
        inv, fi, di = createInventoryWithItems
        inv.addItem(fi)
        inv.addItem(di)
        inv.removeItem(fi)
        assert len(inv.per_type_lists[FileItem]) == 0
        assert len(inv.dirs_files) == 1

        inv.removeItem(di)
        assert len(inv.per_type_lists[DirItem]) == 0
        assert len(inv.dirs_files) == 0

    def testRemoveLogError(self, createInventoryWithItems, caplog):
        """Test whether removing an item not in the inventory logs error."""
        inv, fi, di = createInventoryWithItems
        assert fi not in inv.per_type_lists[FileItem]
        inv.removeItem(fi)
        assert ["Error removing item from container: F0 not in list"] == [rec.message for rec in caplog.records]
