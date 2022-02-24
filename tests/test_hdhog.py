import os
import sys
import shutil
import unittest
from anytree import RenderTree
from utils import (
    createDirTree,
    files_sizes,
    renderTreeStr,
    rendered_tree_true,
    rendered_tree_delete_file,
    rendered_tree_delete_dir,
)


currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(os.path.join(parentdir, "src/hdhog/"))

from models import Catalogue, ActionDelete

unittest.TestLoader.sortTestMethodsUsing = None


class TestCatalogueFiles(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dirtree = createDirTree()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.dirtree)
        # pass

    def test0CreateCatalogue(self):
        catalogue = Catalogue(hash_files=False)
        catalogue.createCatalogue(start=self.dirtree)

        # is the tree correct
        # result_render = renderTreeStr(catalogue.rootdir)
        # print(result_render)

        # all files in catalogue?
        self.assertEqual(len(files_sizes), len(catalogue.files))

        # sorting by size works?
        files_sorted = sorted(files_sizes.items(), key=lambda tup: tup[1], reverse=True)

        for ix, item in enumerate(catalogue.files):
            self.assertEqual(
                files_sorted[ix][0], catalogue.files[ix].getFullPath(),
            )

        # is the tree correct
        result_render = renderTreeStr(catalogue.rootdir)
        print(result_render)

        self.assertEqual(rendered_tree_true, result_render)

    def test1DeleteFile(self):
        catalogue = Catalogue(hash_files=False)
        catalogue.createCatalogue(start=self.dirtree)

        action = ActionDelete()

        path = catalogue.files[0].getFullPath()

        catalogue.actionOnPaths(action, [path])

        self.assertFalse(os.path.isfile(path))

        # is the tree correct
        result_render = renderTreeStr(catalogue.rootdir)
        print(result_render)

        self.assertEqual(rendered_tree_delete_file, result_render)

    def test2DeleteDir(self):
        catalogue = Catalogue(hash_files=False)
        catalogue.createCatalogue(start=self.dirtree)

        action = ActionDelete()

        path = catalogue.dirs[3].getFullPath()

        catalogue.actionOnPaths(action, [path])

        self.assertFalse(os.path.isdir(path))

        # is the tree correct
        result_render = renderTreeStr(catalogue.rootdir)
        print(result_render)

        self.assertEqual(rendered_tree_delete_dir, result_render)

    # def testCreateCatalogueFilter(self):
    #     ext = "txt"
    #     catalogue = Catalogue()
    #     catalogue.addFilterCheck(FilterCheckFileExt([ext]))
    #     catalogue.createCatalogue(start=self.dirtree)

    #     files_sub = [
    #         tup for tup in files if os.path.splitext(tup[0])[1].strip(".") != ext
    #     ]

    #     # all files in catalogue?
    #     self.assertEqual(len(files_sub), len(catalogue.files))


if __name__ == "__main__":
    unittest.main()
