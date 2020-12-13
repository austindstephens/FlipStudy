from card import Card

class Deck:
    """Linked list class composed of Node/Card intances;
    represents a deck of cards"""

    def __init__(self, name):
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
            self._head = Card(front, back)
        # Otherwise we append it to the end of linked list
        else: 
            card = self._head

            while card.next is not None:
                card = card.next
 
            card.next = Card(front, back)

    def read_deck(self):
        """ """
        if self._head is None:
            print("Deck is empty.")
            return

        card = self._head
        num  = 1

        while card is not None:
            print("\n" + str(num) + ": " + card.front) 
            input("Tap any key to see back... ")
            print(str(num) + ": " + card.back)

            num += 1

            card = card.next

    def to_dict(self):
        """Creates a dictionary out of front and back content of all
        cards; takes nothing and returns a list of the front content"""

        #FIXME maybe come up with a new format than two separate lists
        # for front and back content?

        if self._head is None:
            return {}

        front_back = dict()  
        front_back = {"front": [], "back": []}

        card = self._head

        while card is not None:

            front_back["front"].append(card.front)
            front_back["back"].append(card.back)

            card = card.next

        return front_back

    def to_linked_list(self, json_deck):
        """Loads the decks from a json file into the program as
        linked list; takes a json decks dictionary and returns
        nothin"""

        # Check if there is data to load
        if "front" not in json_deck:
            print(self._name + " has no data from json file.")
            return

        # The head node should be None since this is a deck loaded
        # from a json file
        front = json_deck["front"][0]
        back  = json_deck["back"][0]

        self._head = Card(front, back)
        card = self._head

        i = 1

        # Load the other data; there is a one-to-one correspondence
        # between the Front and Back lists; so we can use the
        # length of either list
        while i < len(json_deck["front"]):
            front     = json_deck["front"][i]
            back      = json_deck["back"][i]
            card.next = Card(front, back)

            card = card.next

            i += 1


