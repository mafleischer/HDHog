import shutil
import os
from abc import ABC, abstractclassmethod

from container import CatalogueItem
from logger import logger


class FSAction(ABC):
    """Base class for file system actions"""

    @abstractclassmethod
    def execute(self, catalogue_item: CatalogueItem):
        pass


class FSActionDelete(FSAction):
    def execute(self, item: CatalogueItem):
        path = item.getFullPath()
        try:
            os.remove(path)
        except FileNotFoundError:
            logger.error("Error deleting file: File not found.")
            raise
        except IsADirectoryError:
            shutil.rmtree(path)


class FSActionMoveTo(FSAction):
    def __init__(self, dest_path: str):
        self.dest_path = dest_path

    def execute(self, item: CatalogueItem):
        path = item.getFullPath()
        try:
            shutil.move(path, self.dest_path)
        except NotADirectoryError:
            logger.error(
                f"Error moving {path}: Destination {self.dest_path} does not exist."
            )
            raise
        except FileNotFoundError:
            logger.error(f"Error moving {path}: Source {path} does not exist.")
            raise