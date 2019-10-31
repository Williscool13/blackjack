from random import shuffle
from time import sleep


class Wallet(object):
    def __init__(self, starting = 200):
        self.balance = starting

    def current_balance(self):
        return str(self.balance)

    def increase(self, qty):
        self.balance += qty
        print('New Balance', self.balance)

    def decrease(self, qty):
        self.balance -= qty
        print('New Balance', self.balance)

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
    def __init__(self, name, auto = False, starting = 200):
        super().__init__()
        self.name = name
        self.auto = auto

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

    def is_auto(self):
        return self.auto


    def auto_play(self, upcard):
        pass
    def auto_split(self, upcard):
        pass


'''
    def balance(self):
        return self.wallet.total()

    def player_win(self, value):
        self.wallet.increase(value)

    def player_lose(self, value):
        self.wallet.decrease(value)
'''



class Dealer(Hand):
    def add(self, cards, surpress = False):
        for card in cards:
            self.hand.append(card)
            if not surpress:
                print('The dealer drew ' + card.to_string())

    def reduce(self):
        for card in self.hand:
            if card.is_buffed_ace():
                print(card.to_string() + ' has automatically been reduced in value to 1')
                card.value = 1
                return True
        return False

    def dealer_up(self):
        return self.deck[0]
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
        self.double = False

    def get_dealer(self):
        return self.dealer

    def create_deck(self, multiplier):
        self.deck = Deck(multiplier)
        self.deck.shuffle()

    def initial_draw(self):
        print('=' * 50)
        print('You draw 2 cards')
        print('-' * 25)
        self.player.add(self.deck.draw(2))
        print('=' * 50)
        print('The dealer draws 2 cards')
        print('-' * 25)
        self.dealer.add(self.deck.draw(1))
        self.dealer.add(self.deck.draw(1), surpress = True)

    def player_split(self):
        player1 = Player('player 1', auto = self.player.is_auto())
        player2 = Player('player 2', auto = self.player.is_auto())
        card1, card2 = self.player.hand_split()
        player1.add([card1], surpress = True)
        player2.add([card2], surpress = True)
        print('Hand 1:')
        player1.add(self.deck.draw(1))
        print('Hand 2:')
        player2.add(self.deck.draw(1))
        return player1, player2


    def player_turn(self):
        turn = True
        while True:
            if self.player.is_auto():
                decision = self.player.auto_play(self.dealer.up_card())
            else:
                print('Your hand currently contains: ' + self.player.to_string())
                print('And has a value of: ' + str(self.player.hand_value()))
                if self.player.is_blackjack():
                    print('Blackjack!')
                    sleep(2)
                    return 'pl_w'
                decision = None
                if turn:
                    while decision != 'H' and decision != 'S' and decision != 'D':
                        decision = input('Would you like to (D)ouble, (H)it, or (S)tand').upper()
                    turn = False
                else:
                    while decision != 'H' and decision != 'S':
                        decision = input('Would you like to (H)it or (S)tand? ').upper()
            if decision == 'H':
                self.player.add(self.deck.draw(1))
            elif decision == 'D':
                self.player.add(self.deck.draw(1))
                self.double = True
            else:
                return 'play'

            if self.player.is_invalid():
                if not self.player.reduce():
                    print('-' * 50)
                    print('Your hand currently contains: ' + self.player.to_string())
                    print('And has a value of: ' + str(self.player.hand_value()))
                    print('Bust!')
                    return 'pl_l'

            if decision == 'D':
                self.double = True
                print('Your hand currently contains: ' + self.player.to_string())
                print('And has a value of: ' + str(self.player.hand_value()))
                return 'play'

    def dealer_turn(self):
        while True:
            print("The dealer's hand currently contains: " + self.dealer.to_string())
            print('And has a value of: ' + str(self.dealer.hand_value()))
            if self.dealer.is_invalid():
                if not self.dealer.reduce():
                    print('-' * 50)
                    print('Dealer Bust!')
                    sleep(2)
                    return 'de_w'

            sleep(2)

            if self.dealer.is_blackjack():
                print('-' * 50)
                print("Dealer Blackjack! The dealer got a perfect 21")
                return 'de_l'


            if self.dealer.hand_value() < 17:
                print('Dealer hits')
                self.dealer.add(self.deck.draw(1))
            else:
                print('Dealer stands')
                return 'play'

    def comparison(self):
        if self.player.hand_value() == self.dealer.hand_value():
            print('-' * 50)
            print('Your hands are equal.')
            print('Push!')
            return 'co_d'
        elif self.player.hand_value() > self.dealer.hand_value():
            print('-' * 50)
            print('Your hand is more valuable than the dealer.')
            print("Your hand: " + self.player.to_string())
            print("Dealer's hand: " + self.dealer.to_string())
            print('You Win!')
            if self.double:
                print('Double Winnings!')
            return 'co_w'
        else:
            print('-' * 50)
            print("You lose! The dealer's hand is more valuable than yours!")
            print("Dealer's hand: " + self.dealer.to_string())
            print("Dealer's hand value: " + str(self.dealer.hand_value()))
            print("Your hand: " + self.player.to_string())
            print('Your hand value: ' + str(self.player.hand_value()))
            if self.double:
                print('Double Losses!')
            return 'co_l'
    def raw_comparison(self, version):
        if version == 'pl_w':
            print('You got a Blackjack! Perfect 21!')
            print('You Win!')
            sleep(3)
        if version == 'pl_l':
            print('You Busted! You went above 21!')
            if self.double:
                print('Double Losses!')
            print('You Lose!')
        if version == 'de_l':
            print('Dealer Blackjack! Perfect 21!')
            if self.double:
                print('Double Losses!')
            print('You Lose!')
        if version == 'de_w':
            print('Dealer Busted! Dealer went above 21!')
            if self.double:
                print('Double Winnings!')
            print('You Win!')

    def game_instance(self):
        print('Game Start!')
        self.deck.deck[-1] = Card(0,10)
        self.deck.deck[-2] = Card(0,11)
        self.initial_draw()
        print('=' * 50)
        games = [self]
        if self.player.is_splitable():
            if self.player.is_auto():
                split_ask = player.auto_split(self.dealer.up_card())
            else:
                split_ask = None
                while split_ask != 'y' and split_ask != 'n':
                    split_ask = input('Would you like to split your hand? (y/n)')
            if split_ask == 'y':
                print('-' * 50)
                player1, player2 = self.player_split()
                games = [Blackjack(self.deck, player1, self.dealer),  Blackjack(self.deck, player2, self.dealer)]

        player_outcome = []
        doubles = []
        for index, instance in enumerate(games):
            print('=' * 50)
            print("PLAYER's TURN", index + 1)
            player_outcome.append(instance.player_turn())
            doubles.append(instance.double)

        dealer_outcome = None
        if 'play' in player_outcome:
            print('=' * 50)
            print("DEALER's TURN ")
            dealer_outcome = self.dealer_turn()

        game_outcome = []
        for index, game in enumerate(games):
            print('=' * 50)
            print("COMPARISON TURN " + str(index + 1))
            #if both player and dealer dont bust
            if player_outcome[index] == 'play' and dealer_outcome == 'play':
                game_outcome.append(game.comparison())
            else:
                #if player busts or 21
                if player_outcome[index] != 'play':
                    self.raw_comparison(player_outcome[index])
                    game_outcome.append(player_outcome[index])
                #if dealer bust or 21
                else:
                    self.raw_comparison(dealer_outcome)
                    game_outcome.append(dealer_outcome)
            sleep(3)



        print(game_outcome)
        print(doubles)
        return game_outcome, doubles

def main():
#    play = None
#    while play != 'y' and play != 'n':
#        play = input('Would you like to play a game? (y/n)').lower()
    wallet = Wallet(200)
    main_deck = Deck(1)
    main_deck.shuffle()

    auto_player = Player('bot', auto = True)
    bet = input('How much money would you like to bet? (Wallet: ' + wallet.current_balance() + ')\n')
    game = Blackjack(main_deck)
    outcomes, doubles = game.game_instance()
    for index, outcome in enumerate(outcomes):
        if outcome[-1] == 'w':
            if doubles[index]:
                wallet.increase(bet * 2)
            else:
                wallet.increase(bet)
        if outcome[-1] == 'l':
            if doubles[index]:
                wallet.decrease(bet * 2)
            else:
                wallet.decrease(bet)
    print(wallet.current_balance())

if __name__ == '__main__':
    main()

