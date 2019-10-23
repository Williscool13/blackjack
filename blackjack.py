class Card(object):
    def __init__(self, suit, value):
        suit_dict = {0: 'Spades', 1: 'Hearts', 2: 'Clubs', 3: 'Diamonds'}
        title_dict = {0: 'Ace', 1: '2', 2: '3', 3: '4', 4: '5', 5: '6', 6: '7', 7: '8', 8: '9', 9: '10', 10: 'Jack', 11: 'Queen', 12: 'King'}
        self.suit = suit_dict[suit]
        self.title = title_dict[value]
        self.value = None
        if value == 0:
            self.value = 11
        else:
            self.value = value + 1


    def to_string(self):
        return 'The ' + self.title + ' of ' + self.suit

    def is_buffed_ace(self):
        if self.value == 11 and self.title == 'Ace':
            return True
        else:
            return False

class Hand(object):
    def __init__(self):
        self.hand = []

    def draw(self, card):
        self.hand.append(card)

    def to_string(self):
        print(', '.join([card.to_string() for card in self.hand]))


class Deck(object):
    '''The Deck class
    Representation of the deck object as a class
    '''
    def __init__(self, multiplier):
        self.deck = []
        self.refill_deck(multiplier)

    def draw(self):
        card_drawn = self.deck.pop()
        print(card_drawn.to_string() + ' was drawn')
        return card_drawn

    def is_empty(self):
        return not self.deck

    def refill_deck(self, multiplier):
        for i in range(52 * multiplier):
            self.deck.append(Card(i // 13, i % 13))

    def to_string(self):
        print(', '.join([card.to_string() for card in self.deck]))






def main():
    player = Hand()
    #instantiate a deck of 52 cards
    deck = Deck(1)






if __name__ == '__main__':
    main()
