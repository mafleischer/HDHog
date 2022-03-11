import unittest
import os
import sys
import shutil
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

from fsaction import FSActionDelete
from container import DirItem, FileItem


class TestFSAction(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dirtree, cls.dirs_sizes, cls.files_sizes = createFSDirTree()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.dirtree)

    def testDeleteFile(self):
        f = list(self.files_sizes.keys())[0]
        parent = os.path.dirname(f)
        fname = os.path.basename(f)
        item = FileItem("F0", parent, fname)
        fsa = FSActionDelete()
        fsa.execute(item)

        self.assertFalse(os.path.isfile(f))

    def testDeleteDir(self):
        d = list(self.dirs_sizes.keys())[2]
        parent = os.path.dirname(d)
        dname = os.path.basename(d)
        item = DirItem("D0", parent, dname)
        fsa = FSActionDelete()
        fsa.execute(item)

        self.assertFalse(os.path.isdir(d))


if __name__ == "__main__":
    unittest.main()
