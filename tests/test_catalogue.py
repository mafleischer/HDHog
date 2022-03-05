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

from catalogue import Catalogue
from fsaction import FSActionDelete

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

        # quick IDs check
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
        result_render = renderTreeStr(catalogue.tree.root_node)
        print(result_render)

        self.assertEqual(render_init, result_render)

    def test1DeleteFile(self):
        catalogue = Catalogue(hash_files=False)
        catalogue.createCatalogue(start=self.dirtree)

        fs_action = FSActionDelete()

        # delete biggest file
        files_sorted = sorted(
            self.files_sizes.items(), key=lambda tup: tup[1], reverse=True
        )
        path = files_sorted[0][0]

        catalogue.actionOnPaths(fs_action, [path])

        self.assertFalse(os.path.isfile(path))

        # is the tree correct
        result_render = renderTreeStr(catalogue.tree.root_node)

        self.assertEqual(render_del_file, result_render)

    def test2DeleteDir(self):
        catalogue = Catalogue(hash_files=False)
        catalogue.createCatalogue(start=self.dirtree)

        fs_action = FSActionDelete()

        # delete smallest subdir
        dirs_sorted = sorted(
            self.dirs_sizes.items(), key=lambda tup: tup[1], reverse=True
        )
        path = dirs_sorted[-1][0]

        catalogue.actionOnPaths(fs_action, [path])

        self.assertFalse(os.path.isdir(path))

        # is the tree correct
        result_render = renderTreeStr(catalogue.tree.root_node)

        self.assertEqual(render_del_dir, result_render)


if __name__ == "__main__":
    unittest.main()
