import pytest
from hdhog.item import Item, FileItem, DirItem, setFileSizeFromFS, addChildToDir
from hdhog.inventory import Inventory


class TestItems:

    def testFixtureCreateItems(self, createItems):
        """Test item creation."""
        fi0, di0 = createItems
        assert fi0.iid == "F0"
        assert fi0.dirpath == "/test/path/"
        assert fi0.item_name == "fname0"
        assert fi0.item_size == 1

        assert di0.iid == "D0"
        assert di0.dirpath == "/test/path/"
        assert di0.item_name == "dname0/"
        assert di0.item_size == 0
        assert isinstance(di0.inventory, Inventory)

    def testRepr(self, createItems):
        fi0, di0 = createItems
        assert repr(fi0) == "F0"

    def setName(self, createItems): 
        fi0, di0 = createItems
        fi0.item_name = "a"
        assert fi0.item_name == "a"

    def testAbstractMethodsError(self, createItems):
        fi0, di0 = createItems
        i0 = Item(
            iid="D0",
            _dirpath="/test/path",
            _item_name="dname0",
            item_size=0
        )
        with pytest.raises(NotImplementedError):
            _ = i0.item_name

    def testFullPath(self, createItems):
        fi0, di0 = createItems
        assert fi0.getFullPath() == "/test/path/fname0"
        assert di0.getFullPath() == "/test/path/dname0/"

class TestItemFunctions:
    def testSetSizeFromFile(self, createItems, tmp_path):
        fi0, di0 = createItems
        fi0.dirpath = str(tmp_path)
        size = 10
        with open(fi0.getFullPath(), "w") as f:
            f.write("X" * size)
        setFileSizeFromFS(fi0)
        assert fi0.item_size == 10

    def testAddChildToDir(self, createItems):
        fi0, di0 = createItems
        addChildToDir(di0, fi0)
        assert fi0 in di0.inventory.per_type_lists[FileItem]
        assert fi0 in di0.inventory.dirs_files
    #
    # def testCreateParentChildItems(self, createSmallItemTree):
    #     """Test whether in the fixture all basic things
    #     are in order."""
    #
    #     di0, di1, fi0 = createSmallItemTree
    #     assert fi0.size == 1
    #     assert di0.size == 0
    #     assert di1.size == 1
    #     assert di1.children == (fi0, di0)
    #     assert fi0 in di1.files and fi0 in di1.dirs_files
    #     assert di0 in di1.dirs and di0 in di1.dirs_files
    #
    # def testGetFullPath(self, createSmallItemTree):
    #     """Test path method of dir and file item."""
    #     di0, di1, fi0 = createSmallItemTree
    #     assert fi0.getFullPath() == "/test/path/fname0"
    #     assert di0.getFullPath() == "/test/path/dname0/"
    #
    # def testSetFileTypeFromFname(self):
    #     """Test setting a files type from file name"""
    #     fi0 = FileItem(
    #         iid="F0", dirpath="/test/path/", item_name="fname0.pdf", item_size=1
    #     )
    #     fi0.setFileType()
    #     assert fi0.type == "pdf"
    #
    # def testAddItemToDiritem(self, createSmallItemTree):
    #     """Add child to parent in fixture and test if size changes and
    #     child appears in containers."""
    #     di0, di1, fi0 = createSmallItemTree
    #     fi1 = FileItem(iid="F1", dirpath="/test/path/", item_name="fname1", item_size=2)
    #     di1.addItem(fi1)
    #     assert di1.size == 3
    #     assert fi1 in di1.files
    #     assert fi1 in di1.dirs_files
    #
    # def testRemoveItemFromDiritem(self, createSmallItemTree):
    #     """Add child to parent in fixture and test if size changes and
    #     child appears in containers."""
    #     di0, di1, fi0 = createSmallItemTree
    #     di1.removeItem(fi0)
    #     assert di1.size == 0
    #
    # def testUpdateItemSelf(self):
    #     """Test wether updating an item's attrs works."""
    #     fi0 = FileItem(iid="F0", dirpath="/test/path/", item_name="fname0", item_size=1)
    #     fi0._updateSelf(size=123)
    #     assert fi0.item_size == 123
    #
    # def testUpdateItemInContainers(self, createSmallItemTree):
    #     """Test updating an item in containers of the caller item."""
    #     di0, di1, fi0 = createSmallItemTree
    #     di1.updateItem(di0, size=123)
    #     assert di0.size == 123
    #     assert di0 in di1.dirs and di0 in di1.dirs_files

    # def testUpdateItemInParent(self, createSmallItemTree):
    #     """Test wether updating an item's attrs leaves it referenceable":
    #         parents containers."""
    #     di0, di1, fi0 = createSmallItemTree
    #     fi0.updateInParentContainers(size=123)
    #     assert fi0.size == 123
    #     assert fi0 in di1.files
    #     assert fi0 in di1.dirs_files
