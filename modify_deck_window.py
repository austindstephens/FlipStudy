import tkinter as tk
from center_window import center_window

class ModifyDeckWindow(tk.Toplevel):
    """ """

    def __init__(self, lbx, deck):
        """ """

        tk.Toplevel.__init__(self)

        self._lbx   = lbx # root window listbox; deck names
        self._deck  = deck

        self.title("Modify Deck")
        center_window(self, 700, 500)

        self._txt      = DeckTextFrame(self)
        self._card_lbx = DeckListboxFrame(self,
                self._txt.get_front_text(), self._txt.get_back_text(),
                self._deck)
  
        self._btn = DeckButtonFrame(self,
                self._card_lbx.get_lbx(), self._txt.get_front_text(),
                self._txt.get_back_text(), self._deck)
        
        # Packing
        self._btn.grid(column=1, row=1, sticky="") # buttons
        self._txt.grid(column=1, row=0, sticky="") # text widgets
        self._card_lbx.grid(column=0, row=0, sticky="") # listbox
        
        # make expandable
        self.grid_columnconfigure([0, 1], weight=1)
        self.grid_rowconfigure([0, 1], weight=1)


class DeckButtonFrame(tk.Frame):
    """ """

    def __init__(self, parent, lbx, front, back, deck):
        """ """

        tk.Frame.__init__(self, parent)

        self._lbx  = lbx
        self._deck = deck
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
        self._deck["front"].append("")
        self._deck["back"].append("")

        # update the card listbox
        length = len(self._deck["front"])
        length = length if length == 0 else length - 1
        
        self._lbx.insert(tk.END, "card " + str(length))

    def delete_card(self):
        """ """

        # Check if nothing is selected in listbox; empty tuple is a falsy
        if not self._lbx.curselection():
            return
        
        pos = self._lbx.curselection()[0] # get index of current selection
        self._deck["front"].pop(pos) # delete card in deck
        self._deck["back"].pop(pos) # delete card in deck
        
        self._lbx.delete(pos, tk.END) # delete the card in the listbox

        # update card numbers in listbox to one less; have to delete
        # and re-insert lines in listboxes; will stop at one less
        # than length, which is the last index position in linked
        # list
        length = len(self._deck["front"])
        
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

        self._deck["front"][pos] = new[0]
        self._deck["back"][pos]  = new[1]

class DeckTextFrame(tk.Frame):
    """ """

    def __init__(self, parent):
        """ """
        tk.Frame.__init__(self, master=parent)

        self["borderwidth"] = 4
        self["relief"]      = "raised"

        self._front = tk.Text(master=self, width=45, height=10)
        self._back  = tk.Text(master=self, width=45, height=10)
        
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

    def __init__(self, parent, front, back, deck):
        """ """

        tk.Frame.__init__(self, parent)

        self["relief"]      = "raised"
        self["borderwidth"] = 4
        
        self._deck          = deck
        self._front_text, self._back_text = front, back

        self._lbx = tk.Listbox(master=self, exportselection=False, height="15")
        self._sbr = tk.Scrollbar(master=self)

        self._lbx.config(yscrollcommand=self._sbr.set)
        self._sbr.config(command=self._lbx.yview)
        
        self._lbx.bind("<<ListboxSelect>>", self.display_content) # bind event to show text

        tk.Label(master=self, text="Cards").pack(side=tk.TOP, fill=tk.BOTH)
        self._lbx.pack(side=tk.LEFT, fill=tk.BOTH)
        self._sbr.pack(side=tk.RIGHT, fill=tk.BOTH)

        length = len(self._deck["front"]) # list card # in listbox
        
        for i in range(0, length):
            self._lbx.insert(tk.END, "card " + str(i))
    
    # Seems we need to have a param here, "event"; don't have to use it
    def display_content(self, event):
        """ """

        # Check if nothing is in listbox; empty tuple is a falsy
        if not self._lbx.curselection():
            return

        pos     = self._lbx.curselection()[0] # get index of current selection
        content = (self._deck["front"][pos], self._deck["back"][pos])

        self._front_text.delete("1.0", tk.END)
        self._back_text.delete("1.0", tk.END)
        
        self._front_text.insert(tk.END, content[0])
        self._back_text.insert(tk.END, content[1])

    def get_lbx(self):
        """ """
        return self._lbx
