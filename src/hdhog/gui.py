from tkinter import Tk, Frame, Button, Listbox, Entry, Label, ttk
from tkinter import RIGHT, LEFT, TOP, BOTTOM, END
from tkinter import W
from tkinter import MULTIPLE
from tkinter import filedialog, messagebox
from math import log
from typing import List, Tuple

from catalogue import Catalogue, DirItem
from tree import Tree
from logger import logger

colors = {"file": "#FFF0D9", "dir": "#D7F4F3"}  # Papaya Whip, Water


class GUITree(Tree):
    def __init__(self, treeview: ttk.Treeview):
        self.element = treeview
        self.element.tag_configure("file", background=colors["file"])
        self.element.tag_configure("dir", background=colors["dir"])

    def deleteByIDs(self, iids: Tuple[str]):
        for iid in iids:
            parent = self.element.parent(iid)
            size = self.element.item(iid)["values"][1]
            update = -size
            self.updateAncestorsSize(iid, update)
            self.deleteSubtree(iid)

    def deleteSubtree(self, item_iid: str):
        self.element.delete(iid)

    def moveSubtree(self, item_iid: str):
        pass

    def updateAncestorsSize(self, item_iid: str, update: int):
        parent = self.element.parent(item_iid)
        while parent:
            name = self.element.item(parent)["values"][0]
            size = self.element.item(parent)["values"][1]
            self.element.item(parent, values=(name, size + update))
            parent = self.element.parent(parent)

    def insertItemsAt(self, parent_iid: str, items: List[Tuple[str, str, str]]):
        pass

    def rmNodeFromParent(item_iid: str):
        pass

    def insertDirItem(self, dir_item: DirItem):
        dir_iid = dir_item.iid
        dir_name = dir_item.name
        dir_size = self.humanReadableSize(dir_item.size)

        if not self.element.exists(dir_iid):
            self.element.insert(
                "", 0, iid=dir_iid, values=(dir_name, dir_size), tags=["dir"]
            )

        # insert sorted dirs, then sorted files

        for child in dir_item.dirs:
            c_iid = child.iid
            c_name = child.name
            c_size = self.humanReadableSize(child.size)
            self.element.move(c_iid, dir_iid, "end")

        for child in dir_item.files:
            c_iid = child.iid
            c_name = child.name
            c_size = self.humanReadableSize(child.size)
            # if not self.element.exists(c_iid):
            self.element.insert(
                dir_iid, END, iid=c_iid, values=(c_name, c_size), tags=["file"]
            )

    def humanReadableSize(self, size: int) -> str:
        """Takes a size in bytes and returns a string with size suffix.

        Takes a size in bytes (as returned from the OS FS functions) and
        turns it into a size string in the manner of Unix' ls tool with
        options -lh.

        Args:
            size (int): size in bytes

        Returns:
            str: size string in human readable form
        """
        size_suffixes = ["K", "M", "G", "T"]

        if size == 0:
            return "0"

        loga = int(log(size, 1000))

        if loga == 0:
            return f"{size}"
        else:
            amount_suffix_x = size // (1000 ** loga)

            if len(str(amount_suffix_x)) > 1:
                return f"{amount_suffix_x}{size_suffixes[loga - 1]}"
            else:
                size_point = size / (1000 ** loga)
                return f"{size_point:.1f}{size_suffixes[loga - 1]}"


class GUI:
    def __init__(self):

        """ ### Data models ### """
        self.catalogue = Catalogue()

        """ ### GUI elements ### """

        self.root = Tk()
        self.root.title("Big File Finder - Find biggest files and delete or move them.")

        """ initial position and size """
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        w = int(sw * 0.66)
        h = int(sh * 0.66)
        x = (sw // 2) - (w // 2)
        y = (sh // 2) - (h // 2)

        self.root.geometry(f"{w}x{h}+{x}+{y}")

        """ ### create right side ### """

        self.frame_right = Frame(self.root, borderwidth=10, height=360, width=200)
        self.frame_right.pack(side=RIGHT, expand=1, fill="both")
        self.frame_right.pack_propagate(0)

        self.lbl_choose_info = Label(
            self.frame_right, text="Start folder:", width=50, anchor=W
        )
        self.lbl_choose_info.pack(side=TOP)

        self.startdir_entry = Entry(self.frame_right, width=50, bd=5)
        self.startdir_entry.pack(side=TOP)

        self.button_choose_folder = Button(
            self.frame_right,
            text="Choose folder...",
            width=50,
            command=self.btnChooseFolder,
        )
        self.button_choose_folder.pack(side=TOP, pady=10)

        self.button_list = Button(
            self.frame_right, text="List", width=50, command=self.bntList,
        )
        self.button_list.pack(side=TOP)

        self.button_delete_selected = Button(
            self.frame_right,
            text="Delete Selected",
            width=50,
            command=self.btnDeleteSelected,
        )
        self.button_delete_selected.pack(side=TOP, pady=50)

        self.button_quit = Button(
            self.frame_right, text="Quit", width=50, command=self.__del__
        )
        self.button_quit.pack(side=BOTTOM)

        """ ### create left side ### """

        self.frame_left = Frame(self.root, borderwidth=10, height=360, width=350)
        self.frame_left.pack(side=LEFT, expand=1, fill="both")
        self.frame_left.pack_propagate(0)

        """ create tabs """

        self.tabs = ttk.Notebook(self.frame_left)
        tab_files = ttk.Frame(self.tabs)
        tab_dirs = ttk.Frame(self.tabs)
        tab_tree = ttk.Frame(self.tabs)
        self.tabs.add(tab_files, text="Files")
        self.tabs.add(tab_dirs, text="Directories")
        self.tabs.add(tab_tree, text="Tree View")
        self.tabs.pack(expand=1, fill="both")

        """ create files view """

        columns = ["name", "size", "dir"]
        self.tv_files = ttk.Treeview(
            tab_files, columns=columns, show="headings", selectmode="extended"
        )
        self.tv_files.column("size", width=80, minwidth=80, stretch=False)
        self.tv_files.column("name", width=200, minwidth=200, stretch=False)
        self.tv_files.column("dir", width=400, stretch=True)

        self.tv_files.heading("name", text="File Name")
        self.tv_files.heading("size", text="File Size")
        self.tv_files.heading("dir", text="Parent Folder")

        self.tv_files.tag_configure("file", background=colors["file"])

        self.tv_files.pack(expand=1, fill="both")

        """ create directory view """

        columns = ["name", "size", "dir"]
        self.tv_dirs = ttk.Treeview(
            tab_dirs, columns=columns, show="headings", selectmode="extended"
        )

        self.tv_dirs.column("size", width=80, minwidth=80, stretch=False)
        self.tv_dirs.column("name", width=200, minwidth=200, stretch=False)
        self.tv_dirs.column("dir", width=400, stretch=True)

        self.tv_dirs.heading("name", text="Folder Name")
        self.tv_dirs.heading("size", text="Folder Size")
        self.tv_dirs.heading("dir", text="Parent Folder")

        self.tv_dirs.tag_configure("dir", background=colors["dir"])

        self.tv_dirs.pack(expand=1, fill="both")

        """ create tree view """

        columns = ["name", "size"]
        guitree = GUITree(
            ttk.Treeview(
                tab_tree, columns=columns, show="tree headings", selectmode="extended"
            )
        )
        self.catalogue.tree.registerMirrorTree(guitree)

        self.tv_tree = guitree.element
        self.tv_tree.heading("name", text="Name")
        self.tv_tree.heading("size", text="Size")
        self.tv_tree.pack(expand=1, fill="both")

        # adding data
        # self.tv_tree.insert("", END, text="Administration", iid=0, open=False)
        # self.tv_tree.insert("", END, text="Logistics", iid=1, open=False)
        # self.tv_tree.insert("", END, text="Sales", iid=2, open=False)
        # self.tv_tree.insert("", END, text="Finance", iid=3, open=False)
        # self.tv_tree.insert("", END, text="IT", iid=4, open=False)

        # # adding children of first node
        # self.tv_tree.insert("", END, text="John Doe", iid=5, open=False)
        # self.tv_tree.insert("", END, text="Jane Doe", iid=6, open=False)
        # self.tv_tree.move(5, 0, 0)
        # self.tv_tree.move(6, 0, 1)

    def __del__(self):
        self.root.destroy()

    def run(self):
        self.root.mainloop()

    def btnChooseFolder(self):
        name = filedialog.askdirectory(parent=self.frame_right, mustexist=True)
        self.startdir_entry.delete(0, END)
        self.startdir_entry.insert(0, name)

    def bntList(self):
        startdir = self.startdir_entry.get()
        if not startdir:
            messagebox.showinfo(
                title="Folder field empty", message="Choose a folder to list."
            )
        else:
            self.catalogue.createCatalogue(start=startdir)

            color_file = "#FFF0D9"
            color_dir = "#D7F4F3"

            for item in self.catalogue.files:
                iid = item.iid
                name = item.name
                size = self.humanReadableSize(item.size)
                parent = item.dirpath
                self.tv_files.insert(
                    "", END, iid=iid, values=(name, size, parent), tags=["file"]
                )

            for item in self.catalogue.dirs:
                iid = item.iid
                name = item.name
                size = self.humanReadableSize(item.size)
                parent = item.dirpath
                self.tv_dirs.insert(
                    "", END, iid=iid, values=(name, size, parent), tags=["dir"]
                )

            # root_iid = self.catalogue.tree.root_node.iid
            # root_name = self.catalogue.tree.root_node.name
            # # root_parent = self.catalogue.tree.root_node.parent
            # root_size = self.catalogue.tree.root_node.size
            # root_size = self.humanReadableSize(root_size)
            # self.tv_tree.insert("", END, iid=root_iid, values=(root_name, root_size))
            # # for node in self.catalogue.tree.root_node:
            # for child in self.catalogue.tree.root_node.dirs:
            #     self.tv_tree.insert(
            #         root_iid,
            #         END,
            #         iid=child.iid,
            #         values=(child.name, self.humanReadableSize(child.size)),
            #     )
            # for child in self.catalogue.tree.root_node.files:
            #     self.tv_tree.insert(
            #         root_iid,
            #         END,
            #         iid=child.iid,
            #         values=(child.name, self.humanReadableSize(child.size)),
            #     )

    def btnDeleteSelected(self):
        tab = self.tabs.tab(self.tabs.select(), "text")
        logger.debug(f"Selected tab {tab}")

        if tab == "Files":
            selection = self.tv_files.selection()
            for iid in selection:
                self.tv_files.delete(iid)
        elif tab == "Directories":
            selection = self.tv_dirs.selection()
            for iid in selection:
                self.tv_dirs.delete(iid)
        else:
            selection = self.tv_tree.selection()
            for iid in selection:
                self.tv_tree.delete(iid)

        # del_items = self.catalogue.tree.deleteByIDs(selection)
        # for item in del_items:
        #     self.catalogue.files.removeItemByValue(item)

        self.catalogue.deleteByIDs(selection)

    def dummy(self):
        self.treeview.pack_forget()

    def humanReadableSize(self, size: int) -> str:
        """Takes a size in bytes and returns a string with size suffix.

        Takes a size in bytes (as returned from the OS FS functions) and
        turns it into a size string in the manner of Unix' ls tool with
        options -lh.

        Args:
            size (int): size in bytes

        Returns:
            str: size string in human readable form
        """
        size_suffixes = ["K", "M", "G", "T"]

        if size == 0:
            return "0"

        loga = int(log(size, 1000))

        if loga == 0:
            return f"{size}"
        else:
            amount_suffix_x = size // (1000 ** loga)

            if len(str(amount_suffix_x)) > 1:
                return f"{amount_suffix_x}{size_suffixes[loga - 1]}"
            else:
                size_point = size / (1000 ** loga)
                return f"{size_point:.1f}{size_suffixes[loga - 1]}"
