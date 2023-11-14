import os
import pytest
from anytree.search import find_by_attr
from typing import Generator

from utils import (
    renderTreeStr,
    render_init,
    render_del_file,
    render_del_dir,
)

from hdhog.catalogue import Catalogue
from hdhog.itemcontainer import DirItem, FileItem
from hdhog.logger import logger


def testCreateCatalogue(create_tree_on_fs: Generator) -> None:
    dirtree, dirs_and_sizes, files_and_sizes = create_tree_on_fs

    catalogue = Catalogue(hash_files=False)
    catalogue.createCatalogue(start=dirtree)

    # all files and dirs in catalogue?
    assert len(catalogue.all_files) == len(files_and_sizes)
    assert len(catalogue.all_dirs) == len(dirs_and_sizes)

    # quick IDs check
    file_ids = sorted([item.iid for item in catalogue.all_files])
    dir_ids = sorted([item.iid for item in catalogue.all_dirs])

    file_ids_expected = sorted([f"F{iid}" for iid in list(range(0, len(file_ids)))])
    assert file_ids == file_ids_expected

    dir_ids_expected = sorted([f"D{iid}" for iid in list(range(0, len(dir_ids)))])
    assert dir_ids == dir_ids_expected

    # sorting by size works?
    files_sorted = sorted(files_and_sizes.items(), key=lambda tup: tup[1], reverse=True)

    for ix, item in enumerate(catalogue.all_files):
        assert catalogue.all_files[ix].getFullPath() == files_sorted[ix][0]

    dirs_sorted = sorted(dirs_and_sizes.items(), key=lambda tup: tup[1], reverse=True)

    for ix, item in enumerate(catalogue.all_dirs):
        assert catalogue.all_dirs[ix].getFullPath() == dirs_sorted[ix][0]

    # correct file / dir count / total space?
    assert catalogue.num_files == len(files_and_sizes)
    assert catalogue.num_dirs == len(dirs_and_sizes) - 1
    assert catalogue.total_space == sum(files_and_sizes.values())

    # # is the tree correct ?
    result_render = renderTreeStr(catalogue.tree.root_node)
    assert result_render == render_init


def testDeleteFile(create_tree_on_fs: Generator) -> None:
    dirtree, dirs_and_sizes, files_and_sizes = create_tree_on_fs

    catalogue = Catalogue(hash_files=False)
    catalogue.createCatalogue(start=dirtree)

    del_iid = "F0"

    del_item = find_by_attr(catalogue.tree.root_node, del_iid, name="iid")

    logger.info(f"Deleting file {del_item.getFullPath()}")

    catalogue.deleteByIDs((del_iid,))

    path = del_item.getFullPath()
    dirs_and_sizes[f"{os.path.dirname(path)}{os.path.sep}"] -= del_item.size

    assert os.path.isfile(path) is False

    assert find_by_attr(catalogue.tree.root_node, del_iid, name="iid") is None

    with pytest.raises(ValueError):
        catalogue.all_files.itemcontainer.index(del_item)

    # correct file count / total space ?
    assert catalogue.num_files == len(files_and_sizes) - 1

    del_files_sizes = {f: size for f, size in files_and_sizes.items() if f != path}
    assert catalogue.total_space == sum(del_files_sizes.values())

    # is the tree correct
    result_render = renderTreeStr(catalogue.tree.root_node)

    assert result_render == render_del_file


def testDeleteDir(create_tree_on_fs: Generator) -> None:
    dirtree, dirs_and_sizes, files_and_sizes = create_tree_on_fs

    catalogue = Catalogue(hash_files=False)
    catalogue.createCatalogue(start=dirtree)

    del_iid = "D0"

    del_item = find_by_attr(catalogue.tree.root_node, del_iid, name="iid")
    old_space = catalogue.total_space

    logger.info(f"Deleting dir {del_item.getFullPath()}")

    catalogue.deleteByIDs((del_iid,))

    path = del_item.getFullPath()
    assert os.path.isdir(path) is False

    assert find_by_attr(catalogue.tree.root_node, del_iid, name="iid") is None

    with pytest.raises(ValueError):
        catalogue.all_dirs.itemcontainer.index(del_item)

    # correct dir count / total space?
    assert catalogue.num_dirs == len(dirs_and_sizes) - 2
    assert catalogue.total_space == old_space - dirs_and_sizes[path]

    # children removed? ; need to expand recursively
    for child in del_item.children:
        if isinstance(child, DirItem):
            with pytest.raises(ValueError):
                catalogue.all_dirs.itemcontainer.index(child)
        if isinstance(child, FileItem):
            with pytest.raises(ValueError):
                catalogue.all_files.itemcontainer.index(child)

    # is the tree correct
    result_render = renderTreeStr(catalogue.tree.root_node)

    assert result_render == render_del_dir
