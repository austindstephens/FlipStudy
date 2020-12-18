class Card:
    """Node class which represents a single Card in a Deck"""

    def __init__(self, front="", back=""):
        """Constructor for card node class; optionally takes
        content of front and back"""

        # Every card has a front and back
        self.front = front
        self.back  = back

        self.next = None
