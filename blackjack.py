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
        return self.hand_value == 21 and len(self.hand) == 2

class Player(Hand):
    def add(self, cards):
        for card in cards:
            self.hand.append(card)
            print('You drew ' + card.to_string())

    def reduce(self):
        for card in self.hand:
            if card.is_buffed_ace():
                print(card.to_string() + ' has automatically been reduced in value to 1')
                card.value = 1
                return True
        return False

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
        self.deck = []
        self.refill_deck(multiplier)

    def draw(self, qty):
        cards_drawn = []
        if not deck:
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


def blackjack():
    print('Welcome to Blackjack')
    deck = Deck(1)
    deck.shuffle()
    gamestate = 'unresolved'
    deck.deck[-1] = deck.deck[0]
    #player's turn
    turn = 'player'
    player = Player()
    dealer = Dealer()
    print('-' * 50)
    print('You draw 2 cards')
    player.add(deck.draw(2))
    print('-' * 50)
    print('The dealer draws 2 cards')
    dealer.add(deck.draw(2))
    print('-' * 50)
    while turn == 'player':
        print('Your hand currently contains: ' + player.to_string())
        print('And has a value of: ' + str(player.hand_value()))
        if player.is_blackjack():
            print('Blackjack! You got a perfect 21')
            turn = 'dealer'
            break
        decision = None
        while decision != 'H' and decision != 'S':
            decision = input('Would you like to (H)it or (S)tand? ').upper()
        if decision == 'H':
            player.add(deck.draw(1))
        else:
            turn = 'dealer'

        if player.is_invalid():
            if player.reduce():
                continue
            else:
                turn = 'player_end'
    print('-' * 50)

    while turn == 'dealer':
        print("The dealer's hand currently contains: " + dealer.to_string())
        print('And has a value of: ' + str(dealer.hand_value()))
        sleep(1)
        if dealer.is_invalid():
            if dealer.reduce():
                continue
            else:
                turn = 'dealer_end'
                break

        if dealer.hand_value() < 17:
            print('Dealer hits')
            dealer.add(deck.draw(1))
        else:
            print("Dealer's hand exceeds 16, turn is over")
            turn = 'compare'

    print('-' * 50)


    if turn == 'compare':
        if player.hand_value() == dealer.hand_value():
            if player.is_blackjack() and dealer.is_blackjack():
                print('Push! You both have Blackjacks!')
                print("Dealer's hand: " + dealer.to_string())
                print("Your hand: " + player.to_string())
            elif player.is_blackjack():
                print('You win, you have a Blackjack!')
                print("Dealer's hand: " + dealer.to_string())
                print("Your hand: " + player.to_string())
            elif dealer.is_blackjack():
                print("You lose, dealer has a Blackjack!")
                print("Dealer's hand: " + dealer.to_string())
                print("Your hand: " + player.to_string())
            else:
                print('Push! Your hands are equal!')
                print('Hand value: ' + str(player.hand_value()))
                print("Dealer's hand: " + dealer.to_string())
                print("Your hand: " + player.to_string())
        elif player.hand_value() > dealer.hand_value():
            print('You win! Your hand is more valuable than the dealer!')
            print("Your hand: " + player.to_string())
            print('Your hand value: ' + str(player.hand_value()))
            print("Dealer's hand: " + dealer.to_string())
            print("Dealer's hand value: " + str(dealer.hand_value()))
        else:
            print("You lose! The dealer's hand is more valuable than yours!")
            print("Dealer's hand: " + dealer.to_string())
            print("Dealer's hand value: " + str(dealer.hand_value()))
            print("Your hand: " + player.to_string())
            print('Your hand value: ' + str(player.hand_value()))
    elif turn == 'player_end':
        print('Bust, you Lose! Your hand exceeds 21!')
        print('Your hand value totals up to: ' + str(player.hand_value()))
    elif turn == 'dealer_end':
        print("Dealer bust, you Win! The dealer's hand exceeds 21")
        print("The dealer's hand value totals up to: " + str(dealer.hand_value()))





def main():
    blackjack()





if __name__ == '__main__':
    main()
