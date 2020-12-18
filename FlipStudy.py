#!/usr/bin/python

import json
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

from deck import Deck

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

        btn_cmd = [self.create_deck, self.modify_deck, self.delete_deck, None]

        for i in range(4):
            tk.Button(text=btn_str[i], master=self,
                    command=btn_cmd[i]).pack(pady=5)

    def create_deck(self):
        """Create deck dialog window; takes and returns nothing"""

        # Improve/remove this method
        CreateDeckWindow(self._decks, self._lbx) # window instance

    def modify_deck(self):
        """ """

        # Get current selection from the listbox on root window
        deck = self._lbx.get(tk.ANCHOR)

        # Show error if no deck selected on root window
        if(not deck):
            messagebox.showerror("No Deck Selected",
                    "You must select a deck to modify.")
            return
        
        ModifyDeckWindow(self._decks, self._lbx, deck) # window instance

    def delete_deck(self):
        """ """

        # delete the key-value pair in the dicitonary mapping deck name
        # to Deck object
        deck = self._lbx.get(tk.ANCHOR)
        self._decks.pop(deck)

        # update listbox to reflect deleted deck
        self._lbx.delete(tk.ANCHOR)

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
        self._decks[name] = Deck(name)
        self._lbx.insert(tk.END, name)  
        self.destroy()


class DeckButtonFrame(tk.Frame):
    """ """

    def __init__(self, parent, decks, lbx, front, back, name):
        """ """

        tk.Frame.__init__(self, parent)

        self._decks      = decks
        self._name       = name
        self._lbx        = lbx
        self._front_text, self._back_text = front, back

        self["relief"]      = "raised"
        self["borderwidth"] = 4

        btn_cmd = [self.append_card, self.update_card, self.delete_card]
        btn_str = ["Add Card", "Update", "Delete"]

        # Buttons
        for i in range(3):
            tk.Button(master=self, text=btn_str[i],
                    command=btn_cmd[i]).pack(side=tk.LEFT, padx=5)

    def append_card(self):
        """ a card to the deck"""

        # append the card to end of linked list
        self._decks[self._name].append_card()

        # update the card listbox
        length = self._decks[self._name].get_length()
        length = length if length == 0 else length - 1
        
        self._lbx.insert(tk.END, "card " + str(length))

    def delete_card(self):
        """ """

        # Check if nothing is selected in listbox; empty tuple is a falsy
        if not self._lbx.curselection():
            return
        
        pos = self._lbx.curselection()[0] # get index of current selection
        self._decks[self._name].delete_card(pos) # delete card in deck

        self._lbx.delete(pos, tk.END) # delete the card in the listbox

        # update card numbers in listbox to one less; have to delete
        # and re-insert lines in listboxes; will stop at one less
        # than length, which is the last index position in linked
        # list
        length = self._decks[self._name].get_length()
        
        for i in range(pos, length):
            self._lbx.insert(tk.END, "card " + str(i))

        # Delete the left-over contents in the text widgets
        self._front_text.delete("0.0", tk.END)
        self._back_text.delete("0.0", tk.END)

    def update_card(self):
        """ """

        # Check if nothing is selected in listbox; empty tuple is a falsy
        if not self._lbx.curselection():
            return

        # Get the content excluding the added new line character
        new = (self._front_text.get("0.0", "end-1c"),
                self._back_text.get("0.0", "end-1c"))
        pos = self._lbx.curselection()[0]

        self._decks[self._name].set_card(new, pos)

class DeckTextFrame(tk.Frame):
    """ """

    def __init__(self, parent):
        """ """
        tk.Frame.__init__(self, parent)

        self["height"]      = "200"
        self["width"]       = "300"
        self["borderwidth"] = 4
        self["relief"]      = "raised"

        self._front = tk.Text(master=self, width=40, height=10)
        self._back  = tk.Text(master=self, width=40, height=10)
        
        tk.Label(master=self, text="Front").pack(side=tk.TOP, fill=tk.BOTH)
        self._front.pack() 
        tk.Label(master=self, text="Back").pack(fill=tk.BOTH)
        self._back.pack()
    
    def get_front_text(self):
        """ """
        return self._front

    def get_back_text(self):
        """ """
        return self._back

class DeckListboxFrame(tk.Frame):
    """ """

    def __init__(self, parent, decks, front, back, name):
        """ """

        tk.Frame.__init__(self, parent)

        self["relief"]      = "raised"
        self["borderwidth"] = 4
        
        self._decks      = decks
        self._name       = name
        self._front_text, self._back_text = front, back

        self._lbx = tk.Listbox(master=self, exportselection=False, height="15")
        self._sbr = tk.Scrollbar(master=self)

        self._lbx.config(yscrollcommand=self._sbr.set)
        self._sbr.config(command=self._lbx.yview)
        
        self._lbx.bind("<<ListboxSelect>>", self.display_content) # bind event to show text

        tk.Label(master=self, text="Cards").pack(side=tk.TOP, fill=tk.BOTH)
        self._lbx.pack(side=tk.LEFT, fill=tk.BOTH)
        self._sbr.pack(side=tk.RIGHT, fill=tk.BOTH)

        length = self._decks[self._name].get_length() # list card # in listbox
        
        for i in range(0, length):
            self._lbx.insert(tk.END, "card " + str(i))
    
    # Seems we need to have a param here, "event"; don't have to use it
    def display_content(self, event):
        """ """

        # Check if nothing is in listbox; empty tuple is a falsy
        if not self._lbx.curselection():
            return

        pos     = self._lbx.curselection()[0] # get index of current selection
        content = self._decks[self._name].get_card(pos) # tuple front/back

        self._front_text.delete("1.0", tk.END)
        self._back_text.delete("1.0", tk.END)
        
        self._front_text.insert(tk.END, content[0])
        self._back_text.insert(tk.END, content[1])

    def get_lbx(self):
        """ """
        return self._lbx

class ModifyDeckWindow(tk.Toplevel):
    """ """

    def __init__(self, decks, lbx, name):
        """ """

        tk.Toplevel.__init__(self)

        self._decks = decks
        self._name  = name
        self._lbx   = lbx # root window listbox; deck names

        self.title("Modify Deck")

        wnd_x = self.winfo_screenwidth() / 2 - (600 / 2) 
        wnd_y = self.winfo_screenheight() / 2 - (600 / 2)
        
        self.geometry("700x500+%d+%d" %(wnd_x, wnd_y))

        self._txt      = DeckTextFrame(self)
        self._card_lbx = DeckListboxFrame(self, self._decks,
                self._txt.get_front_text(), self._txt.get_back_text(),
                self._name)
  
        self._btn = DeckButtonFrame(self, self._decks,
                self._card_lbx.get_lbx(), self._txt.get_front_text(),
                self._txt.get_back_text(), self._name)
        
        # Packing
        self._btn.grid(column=1, row=1, sticky="") # buttons
        self._txt.grid(column=1, row=0, sticky="") # text widgets
        self._card_lbx.grid(column=0, row=0, sticky="") # listbox

        # Make a polymorphic function
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

# not a frame
class MainApplication():
    """ """

    def __init__(self, parent):
        """Takes root window"""

        # Dictionary mapping deck names to Deck instances; Deck operations
        # use a linked list data structure
        self._decks = dict()

        # Root window
        self._parent = parent

        screen_x = self._parent.winfo_screenwidth() / 2 - (600 / 2)
        screen_y = self._parent.winfo_screenheight() / 2 - (420 / 2)

        self._parent.geometry("600x420+%d+%d" %(screen_x, screen_y)) # Sets window size
        self._parent.title("Flip Study")

        self.init_menu()

        self._lbx_frame = RootListboxFrame(self._parent)
        self._btn_frame = RootButtonFrame(self._parent, self._decks,
                self._lbx_frame.get_lbx())

        self._btn_frame.grid(column=0, row=0, sticky="")
        self._lbx_frame.grid(column=1, row=0, pady=30, sticky="")

        # Make a polymorphic function
        self._parent.grid_columnconfigure(0, weight=1)
        self._parent.grid_columnconfigure(1, weight=1)
        self._parent.grid_rowconfigure(0, weight=1)
        self._parent.grid_rowconfigure(1, weight=1)


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
        """Loads the json data into program using Deck instances and
        linked list data structure; takes decks instance and returns
        nothing"""

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
            # Create a new Deck instance from the deck name in the
            # json decks file, then load the front/back data into
            # the program by adding Nodes/Cards to the deck
            self._decks[deck] = Deck(deck)
            self._decks[deck].to_linked_list(json_decks[deck])

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

        json_decks = dict()

        for deck in self._decks:
            # Map the deck name to a dictionary of the linked list
            front_back       = self._decks[deck].to_dict()
            json_decks[deck] = front_back

        json.dump(json_decks, fileObj, indent=2, sort_keys=True)
        fileObj.close()

        messagebox.showinfo("Decks Written",
                "Decks successfully written to json.")

if __name__ == "__main__":
    """ """

    root = tk.Tk()
    MainApplication(root)
    root.mainloop()
