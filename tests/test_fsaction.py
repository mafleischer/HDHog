import os
from typing import Generator

from hdhog.fsaction import FSActionDelete
from hdhog.container import DirItem, FileItem


def testDeleteFile(test_catalogue: Generator) -> None:
    dirtree, dirs_sizes, files_sizes = test_catalogue
    f = list(files_sizes.keys())[0]
    parent = os.path.dirname(f)
    fname = os.path.basename(f)
    item = FileItem("F0", parent, fname)
    fsa = FSActionDelete()
    fsa.execute(item)

    assert os.path.isfile(f) is False


def testDeleteDir(test_catalogue: Generator) -> None:
    dirtree, dirs_sizes, files_sizes = test_catalogue
    d = list(dirs_sizes.keys())[2]
    parent = os.path.dirname(d)
    dname = os.path.basename(d)
    item = DirItem("D0", parent, dname)
    fsa = FSActionDelete()
    fsa.execute(item)

    assert os.path.isdir(d) is False
