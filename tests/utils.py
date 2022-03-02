import os
import sys
import json
from anytree import RenderTree
from typing import Tuple, Dict

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(os.path.join(parentdir, "src/hdhog/"))

from models import CatalogueItem

render_init = """dirtree/    55555000    /home/linuser/data/code/HDHog/tests/dirtree/
├── dir_1/    55055000    /home/linuser/data/code/HDHog/tests/dirtree/dir_1/
│   ├── file1.pdf    1000000    /home/linuser/data/code/HDHog/tests/dirtree/dir_1/file1.pdf
│   ├── file2.mp3    4000000    /home/linuser/data/code/HDHog/tests/dirtree/dir_1/file2.mp3
│   └── dir_2/    50055000    /home/linuser/data/code/HDHog/tests/dirtree/dir_1/dir_2/
│       ├── file2.mp3    40000    /home/linuser/data/code/HDHog/tests/dirtree/dir_1/dir_2/file2.mp3
│       ├── file3.odt    10000    /home/linuser/data/code/HDHog/tests/dirtree/dir_1/dir_2/file3.odt
│       ├── dir_3/    50000000    /home/linuser/data/code/HDHog/tests/dirtree/dir_1/dir_2/dir_3/
│       │   ├── file4.iso    40000000    /home/linuser/data/code/HDHog/tests/dirtree/dir_1/dir_2/dir_3/file4.iso
│       │   └── file5.mp4    10000000    /home/linuser/data/code/HDHog/tests/dirtree/dir_1/dir_2/dir_3/file5.mp4
│       └── dir_4/    5000    /home/linuser/data/code/HDHog/tests/dirtree/dir_1/dir_2/dir_4/
│           ├── code100.py    4000    /home/linuser/data/code/HDHog/tests/dirtree/dir_1/dir_2/dir_4/code100.py
│           └── code101.c    1000    /home/linuser/data/code/HDHog/tests/dirtree/dir_1/dir_2/dir_4/code101.c
└── dir_0/    500000    /home/linuser/data/code/HDHog/tests/dirtree/dir_0/
    ├── file1.txt    400000    /home/linuser/data/code/HDHog/tests/dirtree/dir_0/file1.txt
    └── file2.txt    100000    /home/linuser/data/code/HDHog/tests/dirtree/dir_0/file2.txt
"""

render_del_file = """dirtree/    15555000    /home/linuser/data/code/HDHog/tests/dirtree/
├── dir_1/    15055000    /home/linuser/data/code/HDHog/tests/dirtree/dir_1/
│   ├── file1.pdf    1000000    /home/linuser/data/code/HDHog/tests/dirtree/dir_1/file1.pdf
│   ├── file2.mp3    4000000    /home/linuser/data/code/HDHog/tests/dirtree/dir_1/file2.mp3
│   └── dir_2/    10055000    /home/linuser/data/code/HDHog/tests/dirtree/dir_1/dir_2/
│       ├── file2.mp3    40000    /home/linuser/data/code/HDHog/tests/dirtree/dir_1/dir_2/file2.mp3
│       ├── file3.odt    10000    /home/linuser/data/code/HDHog/tests/dirtree/dir_1/dir_2/file3.odt
│       ├── dir_3/    10000000    /home/linuser/data/code/HDHog/tests/dirtree/dir_1/dir_2/dir_3/
│       │   └── file5.mp4    10000000    /home/linuser/data/code/HDHog/tests/dirtree/dir_1/dir_2/dir_3/file5.mp4
│       └── dir_4/    5000    /home/linuser/data/code/HDHog/tests/dirtree/dir_1/dir_2/dir_4/
│           ├── code100.py    4000    /home/linuser/data/code/HDHog/tests/dirtree/dir_1/dir_2/dir_4/code100.py
│           └── code101.c    1000    /home/linuser/data/code/HDHog/tests/dirtree/dir_1/dir_2/dir_4/code101.c
└── dir_0/    500000    /home/linuser/data/code/HDHog/tests/dirtree/dir_0/
    ├── file1.txt    400000    /home/linuser/data/code/HDHog/tests/dirtree/dir_0/file1.txt
    └── file2.txt    100000    /home/linuser/data/code/HDHog/tests/dirtree/dir_0/file2.txt
"""

render_del_dir = """dirtree/    15550000    /home/linuser/data/code/HDHog/tests/dirtree/
├── dir_1/    15050000    /home/linuser/data/code/HDHog/tests/dirtree/dir_1/
│   ├── file1.pdf    1000000    /home/linuser/data/code/HDHog/tests/dirtree/dir_1/file1.pdf
│   ├── file2.mp3    4000000    /home/linuser/data/code/HDHog/tests/dirtree/dir_1/file2.mp3
│   └── dir_2/    10050000    /home/linuser/data/code/HDHog/tests/dirtree/dir_1/dir_2/
│       ├── file2.mp3    40000    /home/linuser/data/code/HDHog/tests/dirtree/dir_1/dir_2/file2.mp3
│       ├── file3.odt    10000    /home/linuser/data/code/HDHog/tests/dirtree/dir_1/dir_2/file3.odt
│       └── dir_3/    10000000    /home/linuser/data/code/HDHog/tests/dirtree/dir_1/dir_2/dir_3/
│           └── file5.mp4    10000000    /home/linuser/data/code/HDHog/tests/dirtree/dir_1/dir_2/dir_3/file5.mp4
└── dir_0/    500000    /home/linuser/data/code/HDHog/tests/dirtree/dir_0/
    ├── file1.txt    400000    /home/linuser/data/code/HDHog/tests/dirtree/dir_0/file1.txt
    └── file2.txt    100000    /home/linuser/data/code/HDHog/tests/dirtree/dir_0/file2.txt
"""

with open("dirtree.json") as f:
    dirtree_json = json.load(f)

root_parent = os.getcwd()


def createFSDirTree(
    root_path=root_parent,
) -> Tuple[str, Dict[str, int], Dict[str, int]]:
    """Process the JSON for the directory tree recursively
    and create files / directories.

    Returns two mappings that are referenced in tests.

    Args:
        root_path (str, optional): directory under which the tree
        will be created. Defaults to root_parent.

    Returns:
        tuple: path to the rootnode of the tree, mapping filepaths : sizes,
        mapping directory paths : sizes
    """

    dirs_sizes = {}
    files_sizes = {}

    def recurseCreateItems(parent_path: str, dir_dict: dict):
        subtree = dir_dict["subtree"]
        dir_children = subtree["dir_children"]
        file_children = subtree["file_children"]

        this_dir_path = os.path.join(parent_path, dir_dict["dirname"]) + os.path.sep
        os.mkdir(this_dir_path)
        dirs_sizes[this_dir_path] = 0

        for sub_dict in sorted(dir_children, key=lambda d: d["dirname"]):

            recurseCreateItems(this_dir_path, sub_dict)

            subd_path = os.path.join(this_dir_path, sub_dict["dirname"]) + os.path.sep
            subd_size = dirs_sizes[subd_path]

            dirs_sizes[this_dir_path] += subd_size

        for fname, size in sorted(file_children.items()):
            fpath = os.path.join(this_dir_path, fname)

            with open(fpath, "w") as f:
                f.write("X" * size)

            files_sizes[fpath] = size
            dirs_sizes[this_dir_path] += size

    recurseCreateItems(root_parent, dirtree_json)

    dirtree_path = os.path.join(root_parent, dirtree_json["dirname"]) + os.path.sep
    return dirtree_path, dirs_sizes, files_sizes


def renderTreeStr(root: CatalogueItem) -> str:
    """Return a render string of anytree's RenderTree.

    Args:
        root (CatalogueItem): an anytree root node

    Returns:
        str: the render string
    """
    treestr = ""
    in_branch_space = " " * 4

    for pre, _, node in RenderTree(root):
        treestr += f"{pre}{node.name}{in_branch_space}{node.size}{in_branch_space}{node.getFullPath()}\n"
    return treestr
