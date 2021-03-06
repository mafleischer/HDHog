import unittest
import shutil

from utils import (
    createFSDirTree,
    renderTreeStr,
    render_init,
    render_del_file,
    render_del_dir,
)

from hdhog.gui import GUI, humanReadableSize


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
        self.assertEqual(str(0), humanReadableSize(0))
        self.assertEqual(str(200), humanReadableSize(200))
        self.assertEqual("1.1K", humanReadableSize(1100))
        self.assertEqual("5.5M", humanReadableSize(5500000))
        self.assertEqual("60M", humanReadableSize(60000000))
        self.assertEqual("70G", humanReadableSize(70000000000))


if __name__ == "__main__":
    unittest.main()
