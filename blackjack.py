class Card(object):
    def __init__(self, suit, value):
        suit_dict = {0: 'Spades', 1: 'Hearts', 2: 'Clubs', 3: 'Diamonds'}
        title_dict = {0: 'Ace', 1: '2', 2: '3', 3: '4', 4: '5', 5: '6', 6: '7', 7: '8', 8: '9', 9: '10', 10: 'Jack', 11: 'Queen', 12: 'King'}
        self.suit = suit_dict[suit]
        self.title = title_dict[value]
        self.value = None
        if value == 0:
            self.value = 11
        elif value > 9:
            self.value = 10
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

    def add(self, cards):
        for card in cards:
            self.hand.append(card)

    def to_string(self):
        return(', '.join([card.to_string() for card in self.hand]))

    def hand_value(self):
        return(sum([card.value for card in self.hand]))


    def is_invalid(self):
        pass

class Player(Hand):
    def add(self, cards):
        for card in cards:
            self.hand.append(card)
            print('You drew ' + card.to_string())

class Dealer(Hand):
    def add(self, cards):
        for card in cards:
            self.hand.append(card)
            print('The dealer drew ' + card.to_string())

class Deck(object):
    '''The Deck class
    Representation of the deck object as a class.
    '''
    def __init__(self, multiplier):
        '''Initializes deck.

           Arguments:
               multiplier: A float, determines how many decks are used.
        '''
        self.deck = []
        self.refill_deck(multiplier)

    def draw(self, qty):
        cards_drawn = []
        for i in range(qty):
            cards_drawn.append(self.deck.pop())
        return cards_drawn

    def is_empty(self):
        return not self.deck

    def refill_deck(self, multiplier):
        for i in range(52 * multiplier):
            self.deck.append(Card(i // 13, i % 13))

    def to_string(self):
        return(', '.join([card.to_string() for card in self.deck]))



def blackjack():
    print('Welcome to Blackjack')
    deck = Deck(1)
    gamestate = 'unresolved'


    #player's turn
    turn = 'player'
    player = Player()
    dealer = Dealer()
    print('You draw 2 cards')
    player.add(deck.draw(2))
    print('The dealer draws 2 cards')
    dealer.add(deck.draw(2))
    while turn == 'player':
        print('Your hand currently contains: ' + player.to_string())
        print('And has a value of: ' + str(player.hand_value()))
        decision = None
        while decision != 'H' and decision != 'S':
            decision = input('Would you like to (H)it or (S)tand? ').upper()
        if decision == 'H':
            player.add(deck.draw(1))
        else:
            turn = 'dealer'

        if player.is_invalid():
            print('Bust! Your hand exceeded 21!')
            print('Your hand value totals up to: ' + str(player.hand_value()))
            turn = 'end'




        break




def main():
    blackjack()





if __name__ == '__main__':
    main()
