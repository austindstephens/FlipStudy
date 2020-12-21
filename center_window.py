import tkinter as tk

def center_window(wnd, width, height):
    """Centers whatever window instances passed to it; takes
    a tk.Toplevel and returns nothing"""

    screen_x = (wnd.winfo_screenwidth() / 2) - (width / 2)
    screen_y = (wnd.winfo_screenheight() / 2) - (height / 2)

    wnd.geometry("%dx%d+%d+%d" %(width, height, screen_x, screen_y))
