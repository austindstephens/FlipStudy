import tkinter as tk

from center_window import center_window

class StudyDeckWindow(tk.Toplevel):
    """ """

    def __init__(self, deck):

        tk.Toplevel.__init__(self)

        center_window(self, 600, 420)
        self.title("Study Deck")

        self._deck   = deck
        self._length = len(deck["front"])

        self._txt_frame = TextFrame(self, self._length, self._deck)
        self._btn_frame = ButtonFrame(self, self._txt_frame.get_label(),
                self._deck, self._length, self._txt_frame.get_txt())
        
        self._txt_frame.grid(column=0, row=0,
                padx=10, pady=10, sticky="")
        self._btn_frame.grid(column=0, row=1, sticky="")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure([0, 1], weight=1)
        

class TextFrame(tk.Frame):
    """ """

    def __init__(self, parent, length, deck):
        """ """

        tk.Frame.__init__(self, parent)

        self["borderwidth"] = 4
        self["relief"]      = "raised"

        self._deck = deck

        # MAKE READ ONLY
        self._txt = tk.Text(master=self,
                width=60, height=15)
        self._lbl = tk.Label(master=self, text=F"1 / {length}")

        self._lbl.pack(side=tk.TOP, fill=tk.BOTH)
        self._txt.pack(fill=tk.BOTH)

        # A card should exist if we're launching this window
        self._txt.insert(tk.END, self._deck["front"][0])

    def get_label(self):
        """ """
        return self._lbl

    def get_txt(self):
        """ """
        return self._txt

class ButtonFrame(tk.Frame):
    """ """

    def __init__(self, parent, label, deck, length, txt):
        """ """

        tk.Frame.__init__(self, parent)

        self._label       = label
        self._length      = length
        self._txt         = txt
        self._deck        = deck
        self._cur         = 1
        
        self._is_front = True

        self["relief"]      = "raised"
        self["borderwidth"] = 4

        btn_cmd = [self.back, self.flip, self.next]
        btn_str = ["Back", "Flip", "Next"]

        for i in range(3):
            tk.Button(master=self, text=btn_str[i],
                    command=btn_cmd[i]).pack(side=tk.LEFT, padx=5)


    def back(self):
        """ """

        self._is_front = True

        # Update the label
        if self._cur > 1:
            self._cur -= 1
            self._label["text"] = F"{self._cur} / {self._length}"

        # Update text widget
        self._txt.delete("0.0", tk.END)
        self._txt.insert(tk.END, self._deck["front"][self._cur - 1])
    
    def flip(self):
        """Shows back of card"""

        self._txt.delete("0.0", tk.END)
        
        # Update text depending on whether front or back is currently
        # displayed
        if self._is_front:
            self._txt.insert(tk.END, self._deck["back"][self._cur - 1])
            self._is_front = False
        else:
            self._txt.insert(tk.END, self._deck["front"][self._cur - 1])
            self._is_front = True
    
    def next(self):
        """ """

        self._is_front = True

        # Update the label
        if self._cur < self._length:
            self._cur += 1
            self._label["text"] = F"{self._cur} / {self._length}"

        # Update text widget
        self._txt.delete("0.0", tk.END)
        self._txt.insert(tk.END, self._deck["front"][self._cur - 1])
