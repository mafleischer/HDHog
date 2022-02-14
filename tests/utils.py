import os

files = [
    ("a/file1.txt", "a", 1000000),
    ("a/file2.txt", "a", 800000),
    ("b/file1.pdf", "b", 700000),
    ("b/file2.mp3", "b", 6000000),
]


def createDirTree(parent=os.getcwd()) -> str:

    dirtree = f"{parent}/dirtree/"

    os.mkdir(f"{dirtree}")

    for d in set([tup[1] for tup in files]):
        os.mkdir(f"{dirtree}/{d}")

    for tup in files:
        with open(f"{dirtree}/{tup[0]}", "w") as f:
            f.write("X" * tup[2])

    return dirtree
