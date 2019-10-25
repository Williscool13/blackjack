from random import shuffle
from time import sleep

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
        return self.hand_value() > 21

    def is_blackjack(self):
        return self.hand_value() == 21 and len(self.hand) == 2

class Player(Hand):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def add(self, cards, surpress = False):
        for card in cards:
            self.hand.append(card)
            if not surpress:
                print('You drew ' + card.to_string())

    def reduce(self):
        for card in self.hand:
            if card.is_buffed_ace():
                print(card.to_string() + ' has automatically been reduced in value to 1')
                card.value = 1
                return True
        return False

    def hand_split(self):
        return self.hand[0], self.hand[1]

    def is_splitable(self):
        return len(self.hand) == 2 and self.hand[0].value == self.hand[1].value

class Dealer(Hand):
    def add(self, cards):
        for card in cards:
            self.hand.append(card)
            print('The dealer drew ' + card.to_string())

    def reduce(self):
        for card in self.hand:
            if card.is_buffed_ace():
                print(card.to_string() + ' has automatically been reduced in value to 1')
                card.value = 1
                return True
        return False

class Deck(object):
    '''The Deck class
    Representation of the deck object as a class.
    '''
    def __init__(self, multiplier):
        '''Initializes deck.

           Arguments:
               multiplier: A float, determines how many decks are used.
        '''
        print('Deck Created!')
        self.deck = []
        self.refill_deck(multiplier)

    def draw(self, qty):
        cards_drawn = []
        if not self.deck:
            self.refill_deck()
            self.shuffle()
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

    def shuffle(self):
        shuffle(self.deck)
        print('Deck shuffled!')

class Blackjack(object):
    def __init__(self, deck = None, player = Player('player 0'), dealer = Dealer()):
        self.deck = deck
        self.player = player
        self.dealer = dealer

    def get_dealer(self):
        return self.dealer

    def create_deck(self, multiplier):
        self.deck = Deck(multiplier)
        self.deck.shuffle()

    def initial_draw(self):
        print('-' * 50)
        print('You draw 2 cards')
        self.player.add(self.deck.draw(2))
        print('-' * 50)
        print('The dealer draws 2 cards')
        self.dealer.add(self.deck.draw(2))

    def player_split(self):
        player1 = Player('player 1')
        player2 = Player('player 2')
        card1, card2 = player.hand_split()
        player1.add([card1], surpress = True)
        player2.add([card2], surpress = True)

        return player1, player2


    def player_turn(self):
        while True:
            print('Your hand currently contains: ' + self.player.to_string())
            print('And has a value of: ' + str(self.player.hand_value()))
            if self.player.is_blackjack():
                print('Blackjack! You got a perfect 21')
                print('You Win!')
                sleep(3)
                return 'end_w'
            decision = None
            while decision != 'H' and decision != 'S':
                decision = input('Would you like to (H)it or (S)tand? ').upper()
            if decision == 'H':
                self.player.add(self.deck.draw(1))
            else:
                return 'play'

            if self.player.is_invalid():
                if not self.player.reduce():
                    print('-' * 50)
                    print('Your hand currently contains: ' + self.player.to_string())
                    print('And has a value of: ' + str(self.player.hand_value()))
                    print('Bust! You Lose!')
                    return 'end_l'

    def dealer_turn(self):
        while True:
            print("The dealer's hand currently contains: " + self.dealer.to_string())
            print('And has a value of: ' + str(self.dealer.hand_value()))
            sleep(2)
            if self.dealer.is_blackjack():
                print('-' * 50)
                print("Dealer Blackjack! The dealer got a perfect 21")
                print('You Lose!')
                return 'end_l'

            if self.dealer.is_invalid():
                if not self.dealer.reduce():
                    print('-' * 50)
                    print('Dealer Bust!')
                    print('You Win!')
                    return 'end_w'

            if self.dealer.hand_value() < 17:
                print('Dealer hits')
                self.dealer.add(self.deck.draw(1))
            else:
                return 'play'

    def comparison(self, dealer):
        if self.player.hand_value() == dealer.hand_value():
            print('-' * 50)
            print('Push!\nYour hands are equal!')
            print('Hand value: ' + str(self.player.hand_value()))
            print("Dealer's hand: " + dealer.to_string())
            print("Your hand: " + self.player.to_string())
            return 'end_d'
        elif self.player.hand_value() > dealer.hand_value():
            print('-' * 50)
            print('You win! Your hand is more valuable than the dealer!')
            print("Your hand: " + self.player.to_string())
            print('Your hand value: ' + str(self.player.hand_value()))
            print("Dealer's hand: " + dealer.to_string())
            print("Dealer's hand value: " + str(dealer.hand_value()))
            return 'end_w'
        else:
            print('-' * 50)
            print("You lose! The dealer's hand is more valuable than yours!")
            print("Dealer's hand: " + dealer.to_string())
            print("Dealer's hand value: " + str(dealer.hand_value()))
            print("Your hand: " + self.player.to_string())
            print('Your hand value: ' + str(self.player.hand_value()))
            return 'end_l'


def main():
#    play = None
#    while play != 'y' and play != 'n':
#        play = input('Would you like to play a game? (y/n)').lower()

    game = Blackjack()
    print('Welcome to Blackjack!')

    game.create_deck(1)
    game.initial_draw()
    games = [game]
    if games[0].player.is_splitable():
        split_ask = None
        while split_ask != 'y' and split_ask != 'n':
            split_ask = input('Would you like to split your hand? (y/n)')
        if split_ask == 'y':
            player1, player2 = game.player.player_split()
            player1.add(game.deck.draw(1))
            player2.add(game.deck.draw(1))
            games = [Blackjack(game.deck, player1),  Blackjack(game.deck, player2)]
            games[0].dealer = game.dealer

    dealer_play = []
    for game in games:
        game_outcome = 'play'
        if game_outcome == 'play':
            print('-' * 50)
            print("PLAYER's TURN")
            dealer_play.append(game.player_turn())

    if 'play' in dealer_play:
        print('-' * 50)
        print("DEALER's TURN")
        game_outcome = games[0].dealer_turn()

        if game_outcome == 'play':
            for index, game in enumerate(games):
                if dealer_play[index] == 'play':
                    print('-' * 50)
                    print("COMPARISON TURN")
                    game_outcome = game.comparison(games[0].dealer)
                    sleep(2)


if __name__ == '__main__':
    main()
