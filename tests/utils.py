import json
import os
import sys
from pathlib import Path
from typing import Dict, Tuple

from anytree import RenderTree

currentdir = Path(__file__)
parentdir = currentdir.parent
sys.path.append(str(Path(parentdir, "src/hdhog/")))

from hdhog.item import DirItem, FileItem, Item

# render strings returned by anytree's render function, for comparison; see function renderTreeStr

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
    root_path: Path,
) -> Tuple[str, Dict[str, int], Dict[str, int]]:
    """Process the JSON for the test directory tree recursively
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

    recurseCreateItems(root_path, dirtree_json)

    dirtree_path = str(Path(root_path, dirtree_json["dirname"]))
    return dirtree_path, dirs_sizes, files_sizes


def renderTreeStr(root: Item) -> str:
    """Return a render string of anytree's RenderTree.

    Args:
        root (CatalogueItem): an anytree root node

    Returns:
        str: the render string
    """
    treestr = ""
    in_branch_space = " " * 4

    for pre, _, node in RenderTree(root):
        treestr += f"{pre}{node.iid}{in_branch_space}{node.item_size}{in_branch_space}{node.item_name}\n"
    return treestr
