from hdhog.itemcontainer import DirItem, FileItem, ItemContainer

file_container = ItemContainer()
dir_container = ItemContainer()

fitem = FileItem("F0", "/bla/", "fname", 2000)
fitem2 = FileItem("F1", "/bla/", "fname2", 300)
ditem = DirItem("D0", "/bla/", "dname", [fitem])

file_container.addItem(fitem)
file_container.addItem(fitem2)
dir_container.addItem(ditem)

# fitem.rmNodeFromParent()

for item in ditem.children:
    print("ditem children:", item)

for item in file_container:
    print("file container:", item)

fitem.size = 1000
fitem2.size = 50

for item in file_container:
    print("file size in container:", item._getSize())

fitem.rmNodeFromParent()
