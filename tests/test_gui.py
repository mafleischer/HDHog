from typing import Generator
from hdhog.gui import GUI, humanReadableSize


def testFilesDirsList(test_catalogue: Generator) -> None:
    dirtree, dirs_sizes, files_sizes = test_catalogue
    gui = GUI()
    gui.startdir_entry.insert(0, dirtree)
    gui.bntList()

    len_files = len(gui.tv_files.get_children(0))
    assert len_files == len(files_sizes)

    len_dirs = len(gui.tv_dirs.get_children(0))
    assert len_dirs == len(dirs_sizes)


def testHumanReadableSize(test_catalogue: Generator) -> None:
    dirtree, dirs_sizes, files_sizes = test_catalogue
    assert humanReadableSize(0) == str(0)
    assert humanReadableSize(200) == str(200)
    assert humanReadableSize(1100) == "1.1K"
    assert humanReadableSize(5500000) == "5.5M"
    assert humanReadableSize(60000000) == "60M"
    assert humanReadableSize(70000000000) == "70G"
