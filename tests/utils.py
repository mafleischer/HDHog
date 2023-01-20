import os
import sys
import json
from anytree import RenderTree
from pathlib import Path
from typing import Tuple, Dict

currentdir = Path(__file__)
parentdir = currentdir.parent
sys.path.append(str(Path(parentdir, "src/hdhog/")))

from hdhog.container import CatalogueItem

render_init = """dirtree/    55555000    /home/linuser/data/code/HDHog/tests/dirtree/
├── dir_0/    500000    /home/linuser/data/code/HDHog/tests/dirtree/dir_0/
│   ├── file1.txt    400000    /home/linuser/data/code/HDHog/tests/dirtree/dir_0/file1.txt
│   └── file2.txt    100000    /home/linuser/data/code/HDHog/tests/dirtree/dir_0/file2.txt
└── dir_1/    55055000    /home/linuser/data/code/HDHog/tests/dirtree/dir_1/
    ├── file1.pdf    1000000    /home/linuser/data/code/HDHog/tests/dirtree/dir_1/file1.pdf
    ├── file2.mp3    4000000    /home/linuser/data/code/HDHog/tests/dirtree/dir_1/file2.mp3
    └── dir_2/    50055000    /home/linuser/data/code/HDHog/tests/dirtree/dir_1/dir_2/
        ├── file2.mp3    40000    /home/linuser/data/code/HDHog/tests/dirtree/dir_1/dir_2/file2.mp3
        ├── file3.odt    10000    /home/linuser/data/code/HDHog/tests/dirtree/dir_1/dir_2/file3.odt
        ├── dir_3/    50000000    /home/linuser/data/code/HDHog/tests/dirtree/dir_1/dir_2/dir_3/
        │   ├── file4.iso    40000000    /home/linuser/data/code/HDHog/tests/dirtree/dir_1/dir_2/dir_3/file4.iso
        │   └── file5.mp4    10000000    /home/linuser/data/code/HDHog/tests/dirtree/dir_1/dir_2/dir_3/file5.mp4
        └── dir_4/    5000    /home/linuser/data/code/HDHog/tests/dirtree/dir_1/dir_2/dir_4/
            ├── code100.py    4000    /home/linuser/data/code/HDHog/tests/dirtree/dir_1/dir_2/dir_4/code100.py
            └── code101.c    1000    /home/linuser/data/code/HDHog/tests/dirtree/dir_1/dir_2/dir_4/code101.c
"""


render_del_file = """dirtree/    15555000    /home/linuser/data/code/HDHog/tests/dirtree/
├── dir_0/    500000    /home/linuser/data/code/HDHog/tests/dirtree/dir_0/
│   ├── file1.txt    400000    /home/linuser/data/code/HDHog/tests/dirtree/dir_0/file1.txt
│   └── file2.txt    100000    /home/linuser/data/code/HDHog/tests/dirtree/dir_0/file2.txt
└── dir_1/    15055000    /home/linuser/data/code/HDHog/tests/dirtree/dir_1/
    ├── file1.pdf    1000000    /home/linuser/data/code/HDHog/tests/dirtree/dir_1/file1.pdf
    ├── file2.mp3    4000000    /home/linuser/data/code/HDHog/tests/dirtree/dir_1/file2.mp3
    └── dir_2/    10055000    /home/linuser/data/code/HDHog/tests/dirtree/dir_1/dir_2/
        ├── file2.mp3    40000    /home/linuser/data/code/HDHog/tests/dirtree/dir_1/dir_2/file2.mp3
        ├── file3.odt    10000    /home/linuser/data/code/HDHog/tests/dirtree/dir_1/dir_2/file3.odt
        ├── dir_3/    10000000    /home/linuser/data/code/HDHog/tests/dirtree/dir_1/dir_2/dir_3/
        │   └── file5.mp4    10000000    /home/linuser/data/code/HDHog/tests/dirtree/dir_1/dir_2/dir_3/file5.mp4
        └── dir_4/    5000    /home/linuser/data/code/HDHog/tests/dirtree/dir_1/dir_2/dir_4/
            ├── code100.py    4000    /home/linuser/data/code/HDHog/tests/dirtree/dir_1/dir_2/dir_4/code100.py
            └── code101.c    1000    /home/linuser/data/code/HDHog/tests/dirtree/dir_1/dir_2/dir_4/code101.c
"""

render_del_dir = """dirtree/    5555000    /home/linuser/data/code/HDHog/tests/dirtree/
├── dir_0/    500000    /home/linuser/data/code/HDHog/tests/dirtree/dir_0/
│   ├── file1.txt    400000    /home/linuser/data/code/HDHog/tests/dirtree/dir_0/file1.txt
│   └── file2.txt    100000    /home/linuser/data/code/HDHog/tests/dirtree/dir_0/file2.txt
└── dir_1/    5055000    /home/linuser/data/code/HDHog/tests/dirtree/dir_1/
    ├── file1.pdf    1000000    /home/linuser/data/code/HDHog/tests/dirtree/dir_1/file1.pdf
    ├── file2.mp3    4000000    /home/linuser/data/code/HDHog/tests/dirtree/dir_1/file2.mp3
    └── dir_2/    55000    /home/linuser/data/code/HDHog/tests/dirtree/dir_1/dir_2/
        ├── file2.mp3    40000    /home/linuser/data/code/HDHog/tests/dirtree/dir_1/dir_2/file2.mp3
        ├── file3.odt    10000    /home/linuser/data/code/HDHog/tests/dirtree/dir_1/dir_2/file3.odt
        └── dir_4/    5000    /home/linuser/data/code/HDHog/tests/dirtree/dir_1/dir_2/dir_4/
            ├── code100.py    4000    /home/linuser/data/code/HDHog/tests/dirtree/dir_1/dir_2/dir_4/code100.py
            └── code101.c    1000    /home/linuser/data/code/HDHog/tests/dirtree/dir_1/dir_2/dir_4/code101.c
"""

# set paths accordingly if you call pytest in tests dir or via IDE runner in HDHog
cwd = Path.cwd()
if str(cwd)[-5:] == "HDHog":
    json_subpath = Path("tests/dirtree.json")
    root_parent = Path(cwd, "tests")
if str(cwd)[-5:] == "tests":
    json_subpath = Path("dirtree.json")
    root_parent = cwd

with open(json_subpath) as f:
    dirtree_json = json.load(f)


def createFSDirTree(
    root_path: Path = root_parent,
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

    def recurseCreateItems(parent_path: Path, dir_dict: dict) -> None:
        subtree = dir_dict["subtree"]
        dir_children = subtree["dir_children"]
        file_children = subtree["file_children"]

        this_dir_path = Path(parent_path, dir_dict["dirname"])
        this_dir_path.mkdir()
        dirs_sizes[f"{this_dir_path}{os.path.sep}"] = 0

        for sub_dict in sorted(dir_children, key=lambda d: d["dirname"]):

            recurseCreateItems(this_dir_path, sub_dict)

            subd_path = f"{Path(this_dir_path, sub_dict['dirname'])}{os.path.sep}"
            subd_size = dirs_sizes[subd_path]

            dirs_sizes[f"{this_dir_path}{os.path.sep}"] += subd_size

        for fname, size in sorted(file_children.items()):
            fpath = str(Path(this_dir_path, fname))

            with open(fpath, "w") as f:
                f.write("X" * size)

            files_sizes[fpath] = size
            dirs_sizes[f"{this_dir_path}{os.path.sep}"] += size

    recurseCreateItems(root_parent, dirtree_json)

    dirtree_path = str(Path(root_parent, dirtree_json["dirname"]))
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
