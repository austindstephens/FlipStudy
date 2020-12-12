#

import json

def main():
    """ """

    prompt = ("\n0: exit\n"
              "1: create deck\n"
              "2: add card to deck\n"
              "3: read existing deck\n"
              "4: load deck from file\n")

    # Dictionary mapping deck names to Deck instances
    decks = dict()
    
    try:

        # Print the prompt
        print(prompt)
        sel = input("Selection: ")
        sel = int(sel)

        while sel:

            # Create a new deck
            if sel == 1:

                name = input("Deck name: ")
                decks[name] = Deck(name) 

            # Add card to an existing deck
            elif sel == 2:

                name = input("Deck name: ")

                if name in decks:

                    decks[name].add_card()
                    print("Card added to \"" + name + "\" deck.")

                else:

                    print("Deck does not exist.")

            elif sel == 3:

                name = input("Deck name: ")

                if name in decks:

                    decks[name].read_deck()

                else:

                    print("Deck does not exist.")

            # Print the prompt
            print(prompt)
            sel = input("Selection: ")
            sel = int(sel)
    
    except ValueError:
        
        print("Invalid input.")


class Node:
    """Node class which Represents a single card in a deck"""

    def __init__(self, front="", back=""):
        """ """

        # Card has a front (question) and back (answer); don't
        # have to be private
        self.front = front
        self.back  = back

        self.next = None

class Deck:
    """ """

    def __init__(self, name="Unamed"):
        """ """

        self._name = name
        self._head = None

    def add_card(self):
        """Appends a card to the end of the linked list"""

        # Obtain the content of the Card/Node from the user
        front = input("Front : ")
        back  = input("Back  : ")
        
        # Check if this is first card (None is a falsy)
        if not self._head:

            self._head = Node(front, back)

        # Otherwise we append it to the end of linked list
        else:
            
            node = self._head

            while node.next is not None:
                node = node.next
 
            node.next = Node(front, back)

    def read_deck(self):
        """ """

        if self._head is None:
            print("Deck is empty.")
            return

        node = self._head
        num  = 1

        while node is not None:

            print("\n" + str(num) + ": " + node.front) 
            input("Tap any key to see back... ")
            print(str(num) + ": " + node.back)

            num += 1

            node = node.next

if __name__ == "__main__":
    main()
