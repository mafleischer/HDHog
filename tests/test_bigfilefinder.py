import os
import sys
import shutil
import unittest
from anytree import RenderTree
from utils import createDirTree, files, renderTreeStr, rendered_tree_true


currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from models import Catalogue, ActionDeleteFile, FilterCheckFileExt


class TestCatalogueFiles(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dirtree = createDirTree()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.dirtree)

    def testCreateCatalogue(self):
        catalogue = Catalogue(hash_files=False)
        catalogue.createCatalogue(start=self.dirtree)

        # all files in catalogue?
        self.assertEqual(len(files), len(catalogue.files))

        # sorting by size works?
        files_sorted = sorted(files.items(), key=lambda tup: tup[1], reverse=True)

        for ix, item in enumerate(catalogue.files):
            self.assertEqual(
                f"{self.dirtree}{files_sorted[ix][0]}",
                catalogue.files[ix].getFullPath(),
            )

        # is the tree correct

        result_render = renderTreeStr(catalogue.rootdir)
        print(result_render)

        self.assertEqual(rendered_tree_true, result_render)

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

    # def testDeleteFile(self):
    #     catalogue = Catalogue()
    #     catalogue.createCatalogue(start=self.dirtree)

    #     action = ActionDeleteFile()

    #     catalogue.actionOnIndices(action, [0])

    #     files_sorted = sorted(files, key=lambda tup: tup[2], reverse=True)

    #     self.assertFalse(f"{self.dirtree}{files_sorted[0][0]}" in catalogue.files)


if __name__ == "__main__":
    unittest.main()
