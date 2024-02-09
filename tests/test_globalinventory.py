from hdhog.globalinventory import GlobalInventory
from hdhog.item import DirItem, FileItem
from hdhog.logger import logger

class TestGlobalInventory:
    def testAddItem(self, global_inventory, createItems):
        fi, di = createItems
        global_inv = global_inventory
        global_inventory.addItem(fi)
        global_inventory.addItem(di)
        assert global_inv.item_obj_store == {fi.iid: fi, di.iid: di}
        assert global_inv.total_occupied_space == 1
        assert global_inv.item_counters == {FileItem: 1, DirItem: 1}
        assert global_inv.iid_counters == {FileItem: 1, DirItem: 1}

    def testRemoveItem(self, global_inventory, createItems):
        fi, di = createItems
        global_inv = global_inventory
        global_inventory.addItem(fi)
        global_inventory.addItem(di)
        global_inventory.removeItem(fi.iid)
        global_inventory.removeItem(di.iid)
        assert global_inv.item_obj_store == {}
        assert global_inv.total_occupied_space == 0
        assert global_inv.item_counters == {FileItem: 0, DirItem: 0}
        assert global_inv.iid_counters == {FileItem: 1, DirItem: 1}
