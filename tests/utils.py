import os
import sys
from anytree import RenderTree

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from models import CatalogueItem

files = {
    "a/file1.txt": 1000000,
    "a/file2.txt": 800000,
    "b/file1.pdf": 700000,
    "b/file2.mp3": 6000000,
    "b/c/file2.mp3": 40000,
    "b/c/file3.odt": 30000,
}

rendered_tree_true = """dirtree   8570000  /home/linuser/data/code/BigFileFinder/tests/dirtree\n├── b   6770000  /home/linuser/data/code/BigFileFinder/tests/dirtree/b\n│   ├── file2.mp3   6000000  /home/linuser/data/code/BigFileFinder/tests/dirtree/b/file2.mp3\n│   ├── file1.pdf   700000  /home/linuser/data/code/BigFileFinder/tests/dirtree/b/file1.pdf\n│   └── c   70000  /home/linuser/data/code/BigFileFinder/tests/dirtree/b/c\n│       ├── file2.mp3   40000  /home/linuser/data/code/BigFileFinder/tests/dirtree/b/c/file2.mp3\n│       └── file3.odt   30000  /home/linuser/data/code/BigFileFinder/tests/dirtree/b/c/file3.odt\n└── a   1800000  /home/linuser/data/code/BigFileFinder/tests/dirtree/a\n    ├── file1.txt   1000000  /home/linuser/data/code/BigFileFinder/tests/dirtree/a/file1.txt\n    └── file2.txt   800000  /home/linuser/data/code/BigFileFinder/tests/dirtree/a/file2.txt\n"""


def createDirTree(parent=os.getcwd()) -> str:

    dirtree = f"{parent}/dirtree/"

    os.mkdir(f"{dirtree}")

    for path, size in files.items():
        dirpath = os.path.dirname(path)
        os.makedirs(f"{dirtree}/{dirpath}", exist_ok=True)

        with open(f"{dirtree}/{path}", "w") as f:
            f.write("X" * size)

    return dirtree


def renderTreeStr(root: CatalogueItem) -> str:
    treestr = ""
    for pre, _, node in RenderTree(root):
        treestr += f"{pre}{node.name}   {node.size}  {node.getFullPath()}\n"
    return treestr

