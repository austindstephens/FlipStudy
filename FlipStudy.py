import json
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from deck import Deck

class Window:
    """ """

    def __init__(self, root):
        """Takes root window"""

        # Root window
        self._root = root

        # Dictionary mapping deck names to Deck instances; Deck operations
        # use a linked list data structure
        self._decks = dict()

       # Create window instance
        self._root.geometry("800x600") # Sets window size
        self._root.title("Flip Study")

        # Frames
        self._frame1 = tk.Frame(master=self._root,
                borderwidth=2, relief="sunken")

        self._frame2 = tk.Frame(master=self._root,
                borderwidth=2, relief="ridge")

        self._frame3 = tk.Frame(master=self._root,
                borderwidth=2, relief="ridge")

        # Buttons
        self._btn1 = tk.Button(text="Create New Deck",
                master=self._frame1, command=self.create_deck)

        self._btn2 = tk.Button(text="Modify Deck", master=self._frame1,
                command=self.modify_deck)
        self._btn3 = tk.Button(text="View Deck", master=self._frame1)

        self._btn4 = tk.Button(text="Load Decks From Json",
                master=self._frame1, command=self.load_decks_from_json)
        self._btn5 = tk.Button(text="Write Decks to Json",
                master=self._frame1, command=self.write_decks_to_json)

        # Scrollable listbox
        self._lbx  = tk.Listbox(master=self._frame2)
        self._sbr  = tk.Scrollbar(master=self._frame2)

        self._lbx.config(yscrollcommand = self._sbr.set)
        self._sbr.config(command = self._lbx.yview)
        
        # Labels

        self._lbl = tk.Label(master=self._frame3, text="Decks")

        # Pack
        self._frame1.pack(side=tk.TOP) 
        self._frame2.pack(side=tk.BOTTOM)
        self._frame3.pack(side=tk.BOTTOM)

        self._btn1.pack()
        self._btn2.pack()
        self._btn3.pack()
        self._btn4.pack()
        self._btn5.pack()

        self._lbl.pack(side=tk.LEFT)
        self._lbx.pack(side=tk.LEFT, fill=tk.BOTH)
        self._sbr.pack(side=tk.RIGHT, fill=tk.BOTH)

    def create_deck(self):
        """Create deck dialog window; takes and returns nothing"""

        def add_deck():
            """Creates the new deck and adds it to the combobox
            on the root window; takes and returns nothing"""
            name = ent.get()
            self._decks[name] = Deck(name)
            self._cmb["values"] += (name,) # cancat as tuple
            self._cmb.current(0)
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

        # prompt the user for the file to load

        # FIXME; add error checking for whether the file exists
        with open("decks.json", "r") as infile:
            json_decks = json.load(infile)

        for deck in json_decks:
            # Create a new Deck instance from the deck name in the
            # json decks file, then load the front/back data into
            # the program by adding Nodes/Cards to the deck
            self._decks[deck] = Deck(deck)
            self._decks[deck].to_linked_list(json_decks[deck])

            # Add the deck to the combobox list on the root window
            self._lbx.insert(tk.END, deck)

        tk.messagebox.showinfo("Decks Loaded",
                "Decks successfully loaded from json file.") 


    def write_decks_to_json(self):
        """Writes all the decks in the decks dictionary to a json
        file; takes decks dictionary and returns nothing"""

        json_decks = dict()

        for deck in self._decks:
            # Map the deck name to a dictionary of the linked list
            front_back = self._decks[deck].to_dict()
            json_decks[deck] = front_back

        # Add error checking for whether file already exists; don't
        # want to overwrite data that already exists; FIXME
        with open("decks.json", "w") as outfile:
            json.dump(json_decks, outfile, indent=2, sort_keys=True)

        tk.messagebox.showinfo("Decks Written",
                "Decks successfully written to json file.")

    def modify_deck(self):
        """Allows the user to modify a deck; takes and returns nothing"""

        wnd = tk.Toplevel(self._root)
        wnd.title("Modify Deck")

        wnd.geometry("800x600")


def main():
    """ """

    root   = tk.Tk()
    window = Window(root) # Do all window stuff in this class
    root.mainloop()


def add_card_to_deck(decks):
    """Adds a card to an existing Deck's linked list; takes the decks
    dictionary and returns nothing"""

    name = input("Deck name: ")

    if name in decks:
        decks[name].add_card()
        print("Card added to \"" + name + "\" deck.")
    else:
        print("Deck does not exist.")

def read_deck(decks):
    """Reads the front and back of a Deck linked list; takes decks
    dictionary and returns nothing"""

    name = input("Deck name: ")

    if name in decks:
        decks[name].read_deck()
    else:
        print("Deck does not exist.")



if __name__ == "__main__":
    main()
