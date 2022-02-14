import os
import sys
import shutil
import unittest
from utils import createDirTree, files


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
        catalogue = Catalogue()
        catalogue.createCatalogue(start=self.dirtree)

        # all files in catalogue?
        self.assertEqual(len(files), len(catalogue.files))

        # sorting by size works?
        files_sorted = sorted(files, key=lambda tup: tup[2], reverse=True)

        for ix, item in enumerate(catalogue.files):
            self.assertEqual(
                f"{self.dirtree}{files_sorted[ix][0]}",
                catalogue.files[ix].getFullPath(),
            )

    def testCreateCatalogueFilter(self):
        ext = "txt"
        catalogue = Catalogue()
        catalogue.addFilterCheck(FilterCheckFileExt([ext]))
        catalogue.createCatalogue(start=self.dirtree)

        files_sub = [
            tup for tup in files if os.path.splitext(tup[0])[1].strip(".") != ext
        ]

        # all files in catalogue?
        self.assertEqual(len(files_sub), len(catalogue.files))

    def testDeleteFile(self):
        catalogue = Catalogue()
        catalogue.createCatalogue(start=self.dirtree)

        action = ActionDeleteFile()

        catalogue.fileActionOnIndices(action, [0])

        # res = [
        #     p[0]
        #     for p in catalogue.files.getPathAndSize()
        #     if p[0] == "/home/linuser/data/code/BigFileFinder/tests/dirtree/b/file2.mp3"
        # ]

        files_sorted = sorted(files, key=lambda tup: tup[2], reverse=True)

        self.assertFalse(f"{self.dirtree}{files_sorted[0][0]}" in catalogue.files)


if __name__ == "__main__":
    unittest.main()
