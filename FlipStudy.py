#

import json

def main():
    """ """

    prompt = ("0: exit\n"
              "1: create deck\n"
              "2: add card to deck\n"
              "3: read deck")

    print(prompt)


    try:
        sel = input("Selection: ")
        sel = int(sel)

        while sel:
            # do stuff

            print(prompt)

            sel = input("Selection: ")
            sel = int(sel)
    
    except ValueError:
        
        print("Invalid input.")


class Node:
    """Node class which Represents a single card in a deck"""

    def __init__(self, front="", back=""):
        """ """

        self._front = front
        self._back  = back

        next     = None

class Deck:
    """ """

    def __init__(self):
        """ """

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

            while node is not None:
                node = node.next
 
            node = Node(front, back)

    def read_deck(self):
        """ """
        pass



if __name__ == "__main__":
    main()
