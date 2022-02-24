import os
import sys
from anytree import RenderTree
from string import Template

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(os.path.join(parentdir, "src/hdhog/"))

from models import CatalogueItem

parent = os.getcwd()
dirtree_name = "dirtree"
dirtree = os.path.join(parent, dirtree_name) + os.path.sep

# a/ b/ c/ ...
dir_names = [f"{subd}{os.path.sep}" for subd in ["a", "b", "c"]]

# full dir paths
dirs = [
    f"{dirtree}{d}"
    for d in [dir_names[0], dir_names[1], os.path.join(dir_names[1], dir_names[2])]
]

files = [
    f"{dirs[0]}file1.txt",
    f"{dirs[0]}file2.txt",
    f"{dirs[1]}file1.pdf",
    f"{dirs[1]}file2.mp3",
    f"{dirs[2]}file2.mp3",
    f"{dirs[2]}file3.odt",
]

# files and sizes
files_sizes = dict(zip(files, [400000, 100000, 1000000, 4000000, 40000, 10000]))

dirs_files = {
    dirs[0]: [files[0], files[1]],
    dirs[1]: [files[2], files[3]],
    dirs[2]: [files[4], files[5]],
}

dir_sizes = {
    dirtree_name: sum(files_sizes.values()),
    dir_names[0]: 1800000,
    dir_names[1]: 6770000,
    dir_names[2]: 70000,
}

rendered_tree_true = """dirtree/   5550000  /home/linuser/data/code/HDHog/tests/dirtree/\n├── b/   5050000  /home/linuser/data/code/HDHog/tests/dirtree/b/\n│   ├── file2.mp3   4000000  /home/linuser/data/code/HDHog/tests/dirtree/b/file2.mp3\n│   ├── file1.pdf   1000000  /home/linuser/data/code/HDHog/tests/dirtree/b/file1.pdf\n│   └── c/   50000  /home/linuser/data/code/HDHog/tests/dirtree/b/c/\n│       ├── file2.mp3   40000  /home/linuser/data/code/HDHog/tests/dirtree/b/c/file2.mp3\n│       └── file3.odt   10000  /home/linuser/data/code/HDHog/tests/dirtree/b/c/file3.odt\n└── a/   500000  /home/linuser/data/code/HDHog/tests/dirtree/a/\n    ├── file1.txt   400000  /home/linuser/data/code/HDHog/tests/dirtree/a/file1.txt\n    └── file2.txt   100000  /home/linuser/data/code/HDHog/tests/dirtree/a/file2.txt\n"""
rendered_tree_delete_file = """dirtree/   1550000  /home/linuser/data/code/HDHog/tests/dirtree/\n├── b/   1050000  /home/linuser/data/code/HDHog/tests/dirtree/b/\n│   ├── file1.pdf   1000000  /home/linuser/data/code/HDHog/tests/dirtree/b/file1.pdf\n│   └── c/   50000  /home/linuser/data/code/HDHog/tests/dirtree/b/c/\n│       ├── file2.mp3   40000  /home/linuser/data/code/HDHog/tests/dirtree/b/c/file2.mp3\n│       └── file3.odt   10000  /home/linuser/data/code/HDHog/tests/dirtree/b/c/file3.odt\n└── a/   500000  /home/linuser/data/code/HDHog/tests/dirtree/a/\n    ├── file1.txt   400000  /home/linuser/data/code/HDHog/tests/dirtree/a/file1.txt\n    └── file2.txt   100000  /home/linuser/data/code/HDHog/tests/dirtree/a/file2.txt\n"""
rendered_tree_delete_dir = """dirtree/   1500000  /home/linuser/data/code/HDHog/tests/dirtree/\n├── b/   1000000  /home/linuser/data/code/HDHog/tests/dirtree/b/\n│   └── file1.pdf   1000000  /home/linuser/data/code/HDHog/tests/dirtree/b/file1.pdf\n└── a/   500000  /home/linuser/data/code/HDHog/tests/dirtree/a/\n    ├── file1.txt   400000  /home/linuser/data/code/HDHog/tests/dirtree/a/file1.txt\n    └── file2.txt   100000  /home/linuser/data/code/HDHog/tests/dirtree/a/file2.txt\n"""

# render_top_str = f"{dirtree_name}   {sum(files_sizes.values())}  {dirtree}\n"
# render_branch = Template("├── $name   $dirsize  $path\n")
# render_branch_last = Template("├── $name   $dirsize  $path\n")


def createDirTree() -> str:

    os.mkdir(f"{dirtree}")

    for d in dirs:
        os.makedirs(d, exist_ok=True)

    for file in files:
        with open(file, "w") as f:
            size = files_sizes[file]
            f.write("X" * size)

    return dirtree


def renderTreeStr(root: CatalogueItem) -> str:
    treestr = ""
    for pre, _, node in RenderTree(root):
        treestr += f"{pre}{node.name}   {node.size}  {node.getFullPath()}\n"
    return treestr

