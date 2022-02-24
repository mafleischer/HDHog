from tkinter import Tk, Frame, Button, Listbox, Entry, Label, ttk
from tkinter import RIGHT, LEFT, TOP, BOTTOM, END
from tkinter import W
from tkinter import MULTIPLE
from tkinter import filedialog, messagebox

from models import Catalogue


class GUI:
    def __init__(self):
        self.root = Tk()
        # self.root.tk.call("encoding", "system", "unicode")
        self.root.title("Big File Finder - Find biggest files and delete or move them.")

        """ initial position and size """
        w = 500
        h = 400
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
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

        self.lb_files = Listbox(tab_files, selectmode=MULTIPLE, height=350, width=200)
        self.lb_files.pack(expand=1, fill="both")
        self.lb_files.bind("<Double-Button-1>", self.dummy)

        """ create directory view """

        self.lb_dirs = Listbox(tab_dirs, selectmode=MULTIPLE, height=350, width=200)
        self.lb_dirs.pack(expand=1, fill="both")
        self.lb_dirs.bind("<Double-Button-1>", self.dummy)

        """ create tree view """

        self.treeview = ttk.Treeview(tab_tree)
        self.treeview.pack(expand=1, fill="both")

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

    def deleteSelected(self):
        self.treeview.pack_forget()
        self.listbox.pack(side=BOTTOM)

    def dummy(self):
        self.treeview.pack_forget()
