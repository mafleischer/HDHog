from .inventory import Inventory
from .item import DirItem, FileItem, Item


def createItem(item_type: str, *args, **kwargs) -> Item:
    if item_type == "file":
        return FileItem(*args, **kwargs)
    elif item_type == "dir":
        return DirItem(*args, inventory=Inventory(), **kwargs)
    else:
        raise ValueError
