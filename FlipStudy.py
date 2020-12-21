#!/usr/bin/python


# pass arguments to the frame/toplevel classes; use *args, **kwarg;
# that was the purpose of them...

import tkinter as tk
from main_window import MainWindow
#from tkinter import ttk

if __name__ == "__main__":
    """ """

    root = tk.Tk()
    MainWindow(root)
    root.mainloop()
