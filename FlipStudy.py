# FIXME fix and condense stuff

import json
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from deck import Deck

class Window:
    """ """

    def __init__(self, root):
        """Takes root window"""


        # Dictionary mapping deck names to Deck instances; Deck operations
        # use a linked list data structure
        self._decks = dict()

        # Root window
        self._root = root
        self._root.geometry("600x400") # Sets window size
        self._root.title("Flip Study")

        # Frames
        self._frame1 = tk.Frame(master=self._root,
                borderwidth=2, relief="raised")

        self._frame2 = tk.Frame(master=self._root,
                borderwidth=2)

        # Menu; don't have to handle geometry
        self._men = tk.Menu(self._root)
        self._root.config(menu=self._men)

        self._fileMenu = tk.Menu(master=self._men, tearoff=0)
        self._men.add_cascade(label="File", menu=self._fileMenu)

        self._fileMenu.add_command(label="Open...") # will add file menu for jsons
        self._fileMenu.add_command(label="Save as...")

        self._fileMenu.add_separator()
        self._fileMenu.add_command(label="Exit", command=root.quit) # exit

        # Buttons
        self._btn1 = tk.Button(text="Create New Deck",
                master=self._frame1, command=self.create_deck)

        self._btn2 = tk.Button(text="Modify Deck", master=self._frame1,
                command=self.modify_deck)
        self._btn3 = tk.Button(text="Study Deck", master=self._frame1)

        self._btn4 = tk.Button(text="Load Decks From Json",
                master=self._frame1, command=self.load_decks_from_json)
        self._btn5 = tk.Button(text="Write Decks to Json",
                master=self._frame1, command=self.write_decks_to_json)

        # Scrollable listbox
        self._lbx  = tk.Listbox(master=self._frame2, height=20, width=40)
        self._sbr  = tk.Scrollbar(master=self._frame2)

        self._lbx.config(yscrollcommand = self._sbr.set)
        self._sbr.config(command = self._lbx.yview)
        
        # Labels
        self._lbl = tk.Label(master=self._frame2, text="Decks")

        # Pack

        self._frame1.grid(column=0, row=0, padx=10) 
        self._frame2.grid(column=1, row=0)

        self._btn1.pack(pady=10)
        self._btn2.pack(pady=10)
        self._btn3.pack(pady=10)
        self._btn4.pack(pady=10)
        self._btn5.pack(pady=10)

        self._lbl.pack(side=tk.TOP)
        self._lbx.pack(side=tk.LEFT, fill=tk.BOTH)
        self._sbr.pack(side=tk.RIGHT, fill=tk.BOTH)

    def create_deck(self):
        """Create deck dialog window; takes and returns nothing"""

        def add_deck():
            """Creates the new deck and adds it to the combobox
            on the root window; takes and returns nothing"""
            name = ent.get()
            self._decks[name] = Deck(name)
            self._lbx.insert(tk.END, name)
            wnd.destroy()

        wnd = tk.Toplevel(self._root)
        wnd.title("Deck Creation Dialog")

        lbl = tk.Label(master=wnd, text="Enter deck name: ")
        ent = tk.Entry(master=wnd)
        btn = tk.Button(master=wnd, text="Create",
                command = add_deck)

        lbl.pack()
        ent.pack()
        btn.pack()

    def load_decks_from_json(self):
        """Loads the json data into program using Deck instances and
        linked list data structure; takes decks instance and returns
        nothing"""

        # will add file selector later
        with open("decks.json", "r") as infile:
            json_decks = json.load(infile)

        for deck in json_decks:
            # Create a new Deck instance from the deck name in the
            # json decks file, then load the front/back data into
            # the program by adding Nodes/Cards to the deck
            self._decks[deck] = Deck(deck)
            self._decks[deck].to_linked_list(json_decks[deck])

            # Add the deck to the listbox on the root window
            self._lbx.insert(tk.END, deck)

        messagebox.showinfo("Decks Loaded",
                "Decks successfully loaded from json file.") 


    def write_decks_to_json(self):
        """Writes all the decks in the decks dictionary to a json
        file; takes decks dictionary and returns nothing"""

        json_decks = dict()

        for deck in self._decks:
            # Map the deck name to a dictionary of the linked list
            front_back = self._decks[deck].to_dict()
            json_decks[deck] = front_back

        # will add file selector later
        with open("decks.json", "w") as outfile:
            json.dump(json_decks, outfile, indent=2, sort_keys=True)

        messagebox.showinfo("Decks Written",
                "Decks successfully written to json file.")

    def modify_deck(self):
        """Allows the user to modify a deck; takes and returns nothing"""


        # Get current selection from the listbox on root window
        deck = self._lbx.get(tk.ANCHOR)

        # Show error if no deck selected on root window
        if(not deck):
            messagebox.showerror("No Deck Selected",
                    "You must select a deck to modify.")
            return

        # Window
        wnd = tk.Toplevel(self._root)
        wnd.title("Modify Deck")

        wnd.geometry("800x600")

        # Frames
        frame1 = tk.Frame(master=wnd, relief="sunken") # buttons
        frame2 = tk.Frame(master=wnd, height=200, width=300) # front text box
        frame3 = tk.Frame(master=wnd, height=200, width=300) # back text box
        frame4 = tk.Frame(master=wnd, relief="sunken", borderwidth=2) # Listbox

        # Buttons
        btn1 = tk.Button(master=frame1, text="Add Card")
        btn2 = tk.Button(master=frame1, text="Update")
        btn3 = tk.Button(master=frame1, text="Delete")

        # Text
        txt1 = tk.Text(master=frame2, width=40, height=10) # front
        txt2 = tk.Text(master=frame3, width=40, height=10) # back

        # Scrollable listbox
        lbx  = tk.Listbox(master=frame4)
        sbr  = tk.Scrollbar(master=frame4)

        lbx.config(yscrollcommand = sbr.set)
        sbr.config(command = lbx.yview)
        
        # Packing
        frame1.grid(column=1, row=2, padx=20, pady=20) # buttons
        frame2.grid(column=1, row=0, padx=20) # front text box
        frame3.grid(column=1, row=1) # back text box
        frame4.grid(column=0, row=0, padx=20, pady=20) # listbox


        btn1.pack(side=tk.LEFT, padx=10)
        btn2.pack(side=tk.LEFT, padx=10)
        btn3.pack(side=tk.LEFT, padx=10)

        txt1.pack()
        txt2.pack()

        lbx.pack(side=tk.LEFT, fill=tk.BOTH)
        sbr.pack(side=tk.RIGHT, fill=tk.BOTH)

        # Seems event we need to have a param here, "event";
        # don't have to use it
        def update_text(event):
            """ """

            card_sel = lbx.curselection()[0] # get index of current selection
            content = self._decks[deck].get_card(card_sel) # tuple front/back

            txt1.delete("1.0", tk.END)
            txt2.delete("1.0", tk.END)

            txt1.insert(tk.END, content[0])
            txt2.insert(tk.END, content[1])


        # Bind selection event with the listbox to a function
        # that updates the text widgets with that card's content
        lbx.bind("<<ListboxSelect>>", update_text)

        # List the card numbers in listbox
        num = self._decks[deck].get_length()

        for i in range(0, num):
            lbx.insert(tk.END, "card " + str(i))


def main():
    """ """

    root   = tk.Tk()
    window = Window(root) # Do all window stuff in this class
    root.mainloop()

if __name__ == "__main__":
    main()
