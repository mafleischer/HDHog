from .inventory import Inventory
from .item import DirItem, FileItem, Item


class GlobalInventory(Inventory):
    ID_PREFIXES = {FileItem: "F", DirItem: "D"}

    def __init__(self):
        super().__init__()
        self.item_obj_store = {}
        self.total_occupied_space = 0
        self.item_counters = {FileItem: 0, DirItem: 0}
        self.iid_counters = {FileItem: 0, DirItem: 0}

    def addItem(self, item: Item) -> None:
        ty = type(item)
        item_iid = self.ID_PREFIXES[ty] + str(self.iid_counters[ty])
        self.iid_counters[ty] += 1
        self.item_counters[ty] += 1

        item.iid = item_iid
        super().addItem(item)

        self.item_obj_store[item_iid] = item
        self.total_occupied_space += item.item_size

    def removeItem(self, iid: str) -> Item:
        item = self.item_obj_store.pop(iid)
        super().removeItem(item)
        ty = type(item)
        self.item_counters[ty] -= 1
        self.total_occupied_space -= item.item_size

        return item

    def _addItemNoCount(self, item: Item):
        """Add item without assigning iid and touching counts.

        Only intended for use in decorator below.
        """
        super().addItem(item)

    def _removeItemNoCount(self, item: Item) -> None:
        """Remove item without touching counts.

        Only intended for use in decorator below.
        """
        super().removeItem(item)
