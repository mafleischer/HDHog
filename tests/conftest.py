import pytest
import shutil

from utils import (
    createFSDirTree,
    renderTreeStr,
    render_init,
    render_del_file,
    render_del_dir,
)
from hdhog.tree import FSTree
from hdhog.container import CatalogueContainer, CatalogueItem, DirItem, FileItem


@pytest.fixture
def test_catalogue():
    dirtree, dirs_and_sizes, files_and_sizes = createFSDirTree()
    yield dirtree, dirs_and_sizes, files_and_sizes
    shutil.rmtree(dirtree)
