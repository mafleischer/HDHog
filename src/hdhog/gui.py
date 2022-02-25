from tkinter import Tk, Frame, Button, Listbox, Entry, Label, ttk
from tkinter import RIGHT, LEFT, TOP, BOTTOM, END
from tkinter import W
from tkinter import MULTIPLE
from tkinter import filedialog, messagebox
from math import log

from models import Catalogue


class GUI:
    def __init__(self):

        """ ### Data structures ### """
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
            command=self.chooseFolder,
        )
        self.button_choose_folder.pack(side=TOP, pady=10)

        self.button_choose_folder = Button(
            self.frame_right, text="List", width=50, command=self.listInfo,
        )
        self.button_choose_folder.pack(side=TOP)

        self.button_delete_selected = Button(
            self.frame_right,
            text="Delete Selected",
            width=50,
            command=self.deleteSelected,
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

        # self.lb_files = Listbox(tab_files, selectmode=MULTIPLE, height=350, width=200)
        # self.lb_files.pack(expand=1, fill="both")
        # self.lb_files.bind("<Double-Button-1>", self.dummy)

        self.tv_files = ttk.Treeview(tab_files)
        self.tv_files.pack(expand=1, fill="both")

        """ create directory view """

        # self.lb_dirs = Listbox(tab_dirs, selectmode=MULTIPLE, height=350, width=200)
        # self.lb_dirs.pack(expand=1, fill="both")
        # self.lb_dirs.bind("<Double-Button-1>", self.dummy)

        self.tv_dirs = ttk.Treeview(tab_dirs)
        self.tv_dirs.pack(expand=1, fill="both")

        """ create tree view """

        self.tv_tree = ttk.Treeview(tab_tree)
        self.tv_tree.pack(expand=1, fill="both")

        # adding data
        self.treeview.insert("", END, text="Administration", iid=0, open=False)
        self.treeview.insert("", END, text="Logistics", iid=1, open=False)
        self.treeview.insert("", END, text="Sales", iid=2, open=False)
        self.treeview.insert("", END, text="Finance", iid=3, open=False)
        self.treeview.insert("", END, text="IT", iid=4, open=False)

        # adding children of first node
        self.treeview.insert("", END, text="John Doe", iid=5, open=False)
        self.treeview.insert("", END, text="Jane Doe", iid=6, open=False)
        self.treeview.move(5, 0, 0)
        self.treeview.move(6, 0, 1)

    def __del__(self):
        self.root.destroy()

    def run(self):
        self.root.mainloop()

    def chooseFolder(self):
        name = filedialog.askdirectory(parent=self.frame_right, mustexist=True)
        self.startdir_entry.delete(0)
        self.startdir_entry.insert(0, name)

    def listInfo(self):
        startdir = self.startdir_entry.get()
        if not startdir:
            messagebox.showinfo(
                title="Folder field empty", message="Choose a folder to list."
            )
        else:
            self.catalogue.createCatalogue(start=startdir)

    def deleteSelected(self):
        self.treeview.pack_forget()
        self.listbox.pack(side=BOTTOM)

    def dummy(self):
        self.treeview.pack_forget()

    def humanReadableSize(self, size: int):
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

        loga = int(log(size, 1000))
        if loga == 0:
            return f"{size}"
        elif loga == 1:
            return f"{size // 1000}{size_suffixes[0]}"
        else:
            size_unit = size / (1000 ** loga)
            return f"{size_unit:.1f}{size_suffixes[loga - 1]}"

