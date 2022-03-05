import os
import sys
import shutil
import unittest
from utils import (
    createFSDirTree,
    renderTreeStr,
    render_init,
    render_del_file,
    render_del_dir,
)


currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(os.path.join(parentdir, "src/hdhog/"))

from tree import Tree
from catalogue import CatalogueItem, DirItem, FileItem


class TestTree(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dirtree, cls.dirs_sizes, cls.files_sizes = createFSDirTree()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.dirtree)

    def testCreateTree(self):
        # node_a = DirItem()
        pass


if __name__ == "__main__":
    unittest.main()
