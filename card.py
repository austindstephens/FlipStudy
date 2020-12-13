class Card:
    """Node class which Represents a single Card in a Deck"""

    def __init__(self, front="", back=""):
        """ """

        # Card has a front (question) and back (answer); don't
        # have to be private
        self.front = front
        self.back  = back

        self.next = None
