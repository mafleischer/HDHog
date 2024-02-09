from functools import partial

from .globalinventory import GlobalInventory
from .item import Item


def reinsertItem(item_update_fn):
    def wrapper(item: Item, value: str | int, global_inventory: GlobalInventory):
        global_inventory._removeItemNoCount(item)

        parent = item.parent
        if parent:
            parent.inventory.removeItem(parent)

        item_update_fn(item, value, global_inventory)

        if parent:
            parent.inventory.addItem(parent)

        global_inventory._addItemNoCount(item)

    return wrapper


def updateItemAttr(item: Item, attr: str, value: int | str, fn=setattr) -> None:
    fn(item, attr, value)


@reinsertItem
def updateItemSize(item: Item, size: int, global_inventory: GlobalInventory) -> None:
    updateItemAttr(item, "item_size", size)
