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

from tree import DataTree
from container import CatalogueItem, DirItem, FileItem


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
    return node_0


class TestTree(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # cls.dirtree, cls.dirs_sizes, cls.files_sizes = createFSDirTree()
        pass

    @classmethod
    def tearDownClass(cls):
        # shutil.rmtree(cls.dirtree)
        pass

    def testCreateTree(self):
        root = createSimpleTree()
        true_init_tree = """d0    200000    /bla/d0
├── f0    100000    /bla/d0/f0
└── d1    100000    /bla/d0/d1
    ├── f1    50000    /bla/d1/f1
    └── d2    50000    /bla/d1/d2
        └── f2    50000    /bla/d2/f2
"""

        self.assertEqual(true_init_tree, renderTreeStr(root))

    def testdeleteFileNode(self):
        root = createSimpleTree()
        tree = DataTree(root)
        tree.deleteByIDs(("f1",))

        true_del_tree = """d0    150000    /bla/d0
├── f0    100000    /bla/d0/f0
└── d1    50000    /bla/d0/d1
    └── d2    50000    /bla/d1/d2
        └── f2    50000    /bla/d2/f2
"""

        self.assertEqual(true_del_tree, renderTreeStr(root))

    def testdeleteDirNode(self):
        root = createSimpleTree()
        tree = DataTree(root)
        tree.deleteByIDs(("d2",))

        true_del_tree = """d0    150000    /bla/d0
├── f0    100000    /bla/d0/f0
└── d1    50000    /bla/d0/d1
    └── f1    50000    /bla/d1/f1
"""
        print(renderTreeStr(root))

        self.assertEqual(true_del_tree, renderTreeStr(root))


if __name__ == "__main__":
    unittest.main()
