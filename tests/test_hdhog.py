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

from models import Catalogue, ActionDelete
from gui import GUI

unittest.TestLoader.sortTestMethodsUsing = None


class TestCatalogue(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dirtree, cls.dirs_sizes, cls.files_sizes = createFSDirTree()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.dirtree)

    def test0CreateCatalogue(self):
        catalogue = Catalogue(hash_files=False)
        catalogue.createCatalogue(start=self.dirtree)

        # all files and dirs in catalogue?
        self.assertEqual(len(self.files_sizes), len(catalogue.files))
        self.assertEqual(len(self.dirs_sizes), len(catalogue.dirs))

        # check IDs
        f_ids = sorted([item.iid for item in catalogue.files])
        d_ids = sorted([item.iid for item in catalogue.dirs])
        f_ids_true = sorted([f"F{iid}" for iid in list(range(0, len(f_ids)))])
        self.assertEqual(f_ids_true, f_ids)
        d_ids_true = sorted([f"D{iid}" for iid in list(range(0, len(d_ids)))])
        self.assertEqual(d_ids_true, d_ids)

        # sorting by size works?
        files_sorted = sorted(
            self.files_sizes.items(), key=lambda tup: tup[1], reverse=True
        )

        for ix, item in enumerate(catalogue.files):
            self.assertEqual(
                files_sorted[ix][0], catalogue.files[ix].getFullPath(),
            )

        dirs_sorted = sorted(
            self.dirs_sizes.items(), key=lambda tup: tup[1], reverse=True
        )

        for ix, item in enumerate(catalogue.dirs):
            self.assertEqual(
                dirs_sorted[ix][0], catalogue.dirs[ix].getFullPath(),
            )

        # is the tree correct
        result_render = renderTreeStr(catalogue.rootdir)
        print(result_render)

        self.assertEqual(render_init, result_render)

    def test1DeleteFile(self):
        catalogue = Catalogue(hash_files=False)
        catalogue.createCatalogue(start=self.dirtree)

        action = ActionDelete()

        # delete biggest file
        files_sorted = sorted(
            self.files_sizes.items(), key=lambda tup: tup[1], reverse=True
        )
        path = files_sorted[0][0]

        catalogue.actionOnPaths(action, [path])

        self.assertFalse(os.path.isfile(path))

        # is the tree correct
        result_render = renderTreeStr(catalogue.rootdir)

        self.assertEqual(render_del_file, result_render)

    def test2DeleteDir(self):
        catalogue = Catalogue(hash_files=False)
        catalogue.createCatalogue(start=self.dirtree)

        action = ActionDelete()

        # delete smallest subdir
        dirs_sorted = sorted(
            self.dirs_sizes.items(), key=lambda tup: tup[1], reverse=True
        )
        path = dirs_sorted[-1][0]

        catalogue.actionOnPaths(action, [path])

        self.assertFalse(os.path.isdir(path))

        # is the tree correct
        result_render = renderTreeStr(catalogue.rootdir)

        self.assertEqual(render_del_dir, result_render)


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
