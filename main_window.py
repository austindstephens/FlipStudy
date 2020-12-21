import tkinter as tk
import json
from tkinter import messagebox
from tkinter import filedialog
from center_window import center_window
from modify_deck_window import ModifyDeckWindow
from create_deck_window import CreateDeckWindow
from study_deck_window import StudyDeckWindow

class MainWindow():
    """ """

    def __init__(self, parent):
        """Takes root window"""

        # Dictionary mapping deck names to dictionaries containing
        # front/back content
        self._decks = dict()

        self._parent = parent

        center_window(self._parent, 600, 420)

        self._parent.title("Flip Study")

        self.init_menu()

        self._lbx_frame = RootListboxFrame(self._parent)
        self._btn_frame = RootButtonFrame(self._parent, self._decks,
                self._lbx_frame.get_lbx())

        self._btn_frame.grid(column=0, row=0, sticky="")
        self._lbx_frame.grid(column=1, row=0, pady=30, sticky="")

        self._parent.grid_columnconfigure([0, 1], weight=1)
        self._parent.grid_rowconfigure([0, 1], weight=1)


    def init_menu(self):
        """ """

        men = tk.Menu(self._parent)
        self._parent.config(menu=men)

        file_menu = tk.Menu(master=men, tearoff=0)
        men.add_cascade(label="File", menu=file_menu)

        file_menu.add_command(label="Open...", command=self.load_from_json)
        file_menu.add_command(label="Save as...", command=self.write_to_json)

        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self._parent.quit) # exit

    def load_from_json(self):
        """Loads the json data into program"""

        # Returns path to file
        file_name = filedialog.askopenfilename(initialdir="./",
                filetypes=[("Json files", ".json")], multiple=False)
        
        # Return if None; happens if dialog is opened and then closed;
        # returns an empty tuple in that case which is a falsy
        if not file_name:
            return
        
        with open(file_name, "r") as infile:
            json_decks = json.load(infile)

        for deck in json_decks:

            # Copy the deck to self._decks; handle duplicates FIXME
            self._decks[deck] = json_decks[deck]

            # Add the deck to the listbox on the root window
            self._lbx_frame.get_lbx().insert(tk.END, deck)

    def write_to_json(self):
        """Writes all the decks in the decks dictionary to a json
        file; takes decks dictionary and returns nothing"""

        # Returns a file object
        fileObj = filedialog.asksaveasfile(
                filetypes=[("Json files", ".json")],
                defaultextension=[("Json files", ".json")])

        if not fileObj:
            return

        json.dump(self._decks, fileObj, indent=2, sort_keys=True)
        fileObj.close()

        messagebox.showinfo("Decks Written",
                "Decks successfully written to json.")


class RootListboxFrame(tk.Frame):
    """ """
    
    def __init__(self, parent):
        """ """

        # Super class' init method; master of frame is parent
        tk.Frame.__init__(self, parent)

        self._parent = parent

        self["borderwidth"] = 4
        self["relief"]      = tk.RAISED

        # Scrollable listbox
        self._lbx  = tk.Listbox(master=self, height=20, width=40,
                exportselection=False)
        self._sbr  = tk.Scrollbar(master=self)

        self._lbx.config(yscrollcommand = self._sbr.set)
        self._sbr.config(command = self._lbx.yview)
        
        # Labels
        tk.Label(master=self, text="Decks").pack(side=tk.TOP)

        self._lbx.pack(side=tk.LEFT, fill=tk.BOTH)
        self._sbr.pack(side=tk.RIGHT, fill=tk.BOTH)

    def get_lbx(self):
        """Returns a reference to the listbox needed in the button
        frame class"""
        return self._lbx


class RootButtonFrame(tk.Frame):
    """ """

    def __init__(self, parent, decks, lbx):
        """ """

        # Super class' init method; master of frame is parent
        tk.Frame.__init__(self, parent)

        self._parent = parent
        self._lbx    = lbx
        self._decks  = decks

        self["borderwidth"] = 4
        self["relief"]      = tk.RAISED


        btn_str = ["Create Deck", "Modify Deck", "Delete Deck", "Study Deck"]

        btn_cmd = [self.create_deck, self.modify_deck, self.delete_deck,
                self.study_deck]

        for i in range(4):
            tk.Button(text=btn_str[i], master=self,
                    command=btn_cmd[i]).pack(pady=5)

    def create_deck(self):
        """Create deck dialog window; takes and returns nothing"""

        # Create a 'create deck window' instance
        CreateDeckWindow(self._decks, self._lbx)

    def modify_deck(self):
        """ """

        # Get current selection from the listbox on root window
        cur_sel = self._lbx.get(tk.ANCHOR)

        # Show error if no deck selected on root window
        if not cur_sel:
            messagebox.showerror("No Deck Selected",
                    "You must select a deck to modify.")
            return

        # Create a 'modify deck window' instance
        ModifyDeckWindow(self._lbx, self._decks[cur_sel])

    def study_deck(self):
        """ """

        cur_sel = self._lbx.get(tk.ANCHOR)
        deck    = self._decks[cur_sel]

        if not cur_sel:
            messagebox.showerror("No Deck Selected",
                    "You must select a non-empty deck to study.")
            return

        # Create a 'study deck window' instance
        StudyDeckWindow(deck)


    def delete_deck(self):
        """ """

        # delete the key-value pair in the dicitonary mapping deck name
        # to Deck object
        deck = self._lbx.get(tk.ANCHOR)
        self._decks.pop(deck)

        # update listbox to reflect deleted deck
        self._lbx.delete(tk.ANCHOR)
