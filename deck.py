from card import Card

class Deck:
    """Linked list class composed of Node/Card intances;
    represents a deck of cards"""

    def __init__(self, name):
        """ """

        self._name   = name
        self._head   = None
        self._length = 0

    def append_card(self):
        """Appends a card to the end of the linked list"""

        if self._head is None:
            self._head = Card()
            self._length += 1
            return

        card = self._head

        while card.next is not None:
            card = card.next
 
        card.next = Card()

        self._length += 1

    def set_node(self, content, pos):
        """Takes a tuple containing front and back
        content and pos specifycing which node to set; takes and
        returns nothing"""

        # head node should never be None
        card = self._head
        i = 0

        # Get to card in linked list
        while i < pos:
            card = card.next
            i += 1

        # Set the new front and back content
        card.front = content[0]
        card.back  = content[1]


    def get_card(self, pos):
        """Returns tuple of front and back of card given an integer
        position in linked list"""

        card = self._head

        i = 0

        # Get to the desired card/node; head should never be None
        # since a head node has to exist for it to be in the listbox
        while i < pos:
            card = card.next
            i += 1

        return (card.front, card.back)


    def get_length(self):
        """Takes nothing and returns number of cards/nodes in
        linked list"""

        return self._length

    def to_dict(self):
        """For creating json file; Creates a dictionary out of front
        and back content of all cards; takes nothing and returns a
        list of the front content"""

        # FIXME; improve this

        front_back = {"front": [], "back": []}

        if self._head is None:
            front_back["front"] = [""]
            front_back["back"]  = [""]
            return front_back

        card = self._head

        while card is not None:
            front_back["front"].append(card.front)
            front_back["back"].append(card.back)

            card = card.next

        return front_back

    def to_linked_list(self, json_deck):
        """For loading jsons; loads the decks from json file into
        the program as linked list; takes a json decks dictionary
        and returns nothing"""

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

        # Number of cards/nodes corresponds to length of front/back
        self._length = len(json_deck["front"])


