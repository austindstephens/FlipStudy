from card import Card
import itertools

class Deck:
    """Linked list class composed of Node/Card intances;
    represents a deck of cards"""

    def __init__(self, name):
        """Constructor for deck class; takes the name of the deck
        being instantiated"""

        self._name   = name
        self._head   = None
        self._tail   = None
        self._length = 0

    def append_card(self):
        """Appends a card to the end of the linked list; takes and
        returns nothing"""

        # Create a head node if this is an empty deck; tail node allows
        # us to append without traversing to end of linked list first
        if self._head is None:
            self._head    = Card()
            self._tail    = self._head
            self._length += 1
            return

        self._tail.next = Card()
        self._tail      = self._tail.next
        self._length   += 1

    def set_card(self, content, pos):
        """Takes a tuple containing front and back content and pos
        specifycing which node to set; takes and returns nothing"""

        # Head node should never be None
        card = self._head

        # Get to card in linked list
        for _ in itertools.repeat(None, pos):
            card = card.next

        # Set the new front and back content
        card.front = content[0]
        card.back  = content[1]

    def delete_card(self, pos):
        """Delete card in linked list given index position (starting at 0);
        takes position and returns nothing"""

        if pos == 0:
            # If head points to None then we'll have just
            # an empty linked list and no cards/nodes in listbox
            self._head    = self._head.next
            self._length -= 1
            return

        card = self._head

        # Get to the node/card behind the target node so that deleting
        # target node can be done by simply setting the node pointing
        # to the target node to point to what the target node points to          
        for _ in itertools.repeat(None, pos - 1):
            card = card.next

        # Update tail node if we are deleting the current tail node
        if (self._length - 1) == pos:
            self._tail = card

        card.next = card.next.next
        self._length -= 1

    def get_card(self, pos):
        """Returns tuple of front and back of card given an integer
        position in linked list; takes position and returns tuple"""

        card = self._head

        # Get to the desired card/node; head should never be None
        # since a head node has to exist for it to be in the listbox
        for _ in itertools.repeat(None, pos):
            card = card.next

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
        front, back = json_deck["front"][0], json_deck["back"][0]
        self._head = Card(front, back)
        card = self._head

        i = 1

        # Load the other data; there is a one-to-one correspondence
        # between the Front and Back lists; so we can use the
        # length of either list
        while i < len(json_deck["front"]):
            front, back = json_deck["front"][i], json_deck["back"][i]
            card.next = Card(front, back)
            card = card.next

            i += 1

        # Set the tail to reference last node/card in deck
        self._tail = card

        # Number of cards/nodes corresponds to length of front/back
        self._length = len(json_deck["front"])
