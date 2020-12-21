import tkinter as tk

class CreateDeckWindow(tk.Toplevel):
    """ """

    def __init__(self, decks, lbx):
        """ """

        tk.Toplevel.__init__(self)

        self._decks = decks
        self._lbx   = lbx

        self.title("Create Deck")

        tk.Label(master=self, text="Enter deck name: ").pack() 
        self._ent = tk.Entry(master=self)
        self._ent.pack() 
        tk.Button(master=self, text="Create", command=self.add_deck).pack()

    def add_deck(self):
        """Creates the new deck and adds it to the combobox
        on the root window; takes and returns nothing"""
        
        name = self._ent.get()
        self._decks[name] = {"front": [""], "back": [""]}
        self._lbx.insert(tk.END, name)  
        self.destroy()
