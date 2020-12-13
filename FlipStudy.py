#

import json
from deck import Deck

def main():
    """ """
    # Dictionary mapping deck names to Deck instances; Deck operations
    # use a linked list data structure
    decks = dict()
    
    try:
        sel = prompt()

        while sel:
            # Create a new deck
            if sel == 1:
                create_deck(decks)
            # Add card to an existing deck
            elif sel == 2:
                add_card_to_deck(decks)
            # Reads front and back of cards in a deck
            elif sel == 3:
                read_deck(decks)
            # Reads whatever decks from a json file
            elif sel == 4:
                load_decks_from_json(decks)
            # List all the decks
            elif sel == 5:
                list_decks(decks)
            # Writes all the decks to json
            elif sel == 6:
                write_decks_to_json(decks)
            # Writes all the decks to json and exits
            elif sel == 10:
                write_decks_to_json(decks)
                break

            sel = prompt()

    except ValueError: 
        print("Invalid input.")

def prompt():
    """Prints the prompt and takes user's selection;
    returns the user's selection as integer"""

    prompt = ("\n0: exit\n"
              "1: create deck\n"
              "2: add card to deck\n"
              "3: read existing deck\n"
              "4: load decks from json file\n"
              "5: list decks\n"
              "6: write decks to json file\n"
              "7: insert card to deck\n"
              "8: delete card from deck\n"
              "9: shuffle cards in deck\n"
              "10: write decks and exit")

    # Print the prompt
    print(prompt)
    sel = input("Selection: ")
    
    return int(sel)

def create_deck(decks):
    """Creates a Deck instance and adds it to the dictionary;
    takes the decks dictionary and returns nothing"""

    name = input("Deck name: ")
    decks[name] = Deck(name) 

def add_card_to_deck(decks):
    """Adds a card to an existing Deck's linked list; takes the decks
    dictionary and returns nothing"""

    name = input("Deck name: ")

    if name in decks:
        decks[name].add_card()
        print("Card added to \"" + name + "\" deck.")
    else:
        print("Deck does not exist.")

def read_deck(decks):
    """Reads the front and back of a Deck linked list; takes decks
    dictionary and returns nothing"""

    name = input("Deck name: ")

    if name in decks:
        decks[name].read_deck()
    else:
        print("Deck does not exist.")

def list_decks(decks):
    """Prints out all the Deck names/instances; takes decks dictionary
    and returns nothing"""

    print("\nDecks: ")
    for deck in decks:
        print(deck)

def write_decks_to_json(decks):
    """Writes all the decks in the decks dictionary to a json
    file; takes decks dictionary and returns nothing"""

    json_decks = dict()

    for deck in decks:
        # Map the deck name to a dictionary of the linked list
        front_back = decks[deck].to_dict()
        json_decks[deck] = front_back

    # Add error checking for whether file already exists; don't
    # want to overwrite data that already exists; FIXME
    with open("decks.json", "w") as outfile:
        json.dump(json_decks, outfile, indent=2, sort_keys=True)

def load_decks_from_json(decks):
    """Loads the json data into program using Deck instances and
    linked list data structure; takes decks instance and returns
    nothing"""

    # prompt the user for the while to load


    # FIXME; add error checking for whether the file exists
    with open("decks.json", "r") as infile:
        json_decks = json.load(infile)

    for deck in json_decks:
        # Create a new Deck instance from the deck name in the
        # json decks file, then load the front/back data into
        # the program by adding Nodes/Cards to the deck
        decks[deck] = Deck(deck)
        decks[deck].to_linked_list(json_decks[deck])


if __name__ == "__main__":
    main()
