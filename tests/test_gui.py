import unittest
import shutil
import os
import sys

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

from gui import GUI


class TestGUI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dirtree, cls.dirs_sizes, cls.files_sizes = createFSDirTree()
        cls.gui = GUI()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.dirtree)

    def testFilesDirsList(self):
        self.gui.startdir_entry.insert(0, self.dirtree)
        self.gui.bntList()

        len_files = len(self.gui.tv_files.get_children(0))
        self.assertEqual(len(self.files_sizes), len_files)

        len_dirs = len(self.gui.tv_dirs.get_children(0))
        self.assertEqual(len(self.dirs_sizes), len_dirs)

    def testHumanReadableSize(self):
        self.assertEqual(str(0), self.gui.humanReadableSize(0))
        self.assertEqual(str(200), self.gui.humanReadableSize(200))
        self.assertEqual("1.1K", self.gui.humanReadableSize(1100))
        self.assertEqual("5.5M", self.gui.humanReadableSize(5500000))
        self.assertEqual("60M", self.gui.humanReadableSize(60000000))
        self.assertEqual("70G", self.gui.humanReadableSize(70000000000))


if __name__ == "__main__":
    unittest.main()
