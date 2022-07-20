import random
import time

# Two variables for creating Cards.
SUITE = 'H D S C'.split()
RANKS = '2 3 4 5 6 7 8 9 10 J Q K A'.split()


class Deck:
    """
    This is the Deck Class. This object will create a deck of cards to initiate
    play.
    """
    power_of_rank = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12,
                     'K': 13, 'A': 14}

    def __init__(self, colors, ranking):
        self.colors = colors
        self.ranks = ranking
        self.deck = self.create_deck()

    def create_deck(self):
        created_deck = []
        for rank in self.ranks:
            for color in self.colors:
                card = rank + color
                created_deck.append(card)
        return created_deck

    def shuffle_deck(self):
        random.shuffle(self.deck)

    def split_deck(self):
        first_half = [(self.deck[card]) for card in range(0, len(self.deck), 2)]
        second_half = [(self.deck[card]) for card in range(1, len(self.deck), 2)]
        return {'First half': first_half, 'Second half': second_half}

    def __str__(self):
        return f'Deck configuration: {self.deck}'


class Hand:
    """
    This is the Hand class. Each player has a Hand, and can add or remove
    cards from that hand.
    """

    def __init__(self, cards):
        self.cards = cards

    def remove_card(self):
        return self.cards.pop()

    def add_card(self, new_cards):
        self.cards = new_cards + self.cards

    def show_deck(self):
        return self.cards

    def show_deck_len(self):
        return len(self.cards)


class Player:
    """
    This is the Player class. The Player can play cards and check if they still have cards.
    """
    def __init__(self, name, hand):
        self.name = name
        self.hand = hand

    def play_card(self):
        return self.hand.remove_card()

    def gain_card(self, new_cards):
        self.hand.add_card(new_cards)

    def check_deck(self):
        return self.hand.show_deck_len()

    def show_deck(self):
        print(f'{self.name} hand is: {self.hand.show_deck()}')


class Round:
    """
    This is a Round class. Each round of war game is processed by this class
    """

    def __init__(self, ):
        self.cards_on_table = []

    def add_card_to_table(self, card):
        self.cards_on_table.append(card)

    def get_war_cards(self):
        return {'Player One': self.cards_on_table[-2], 'Player Two': self.cards_on_table[-1]}

    def play_a_round(self, player_one, player_two):
        war_card_player_one = self.get_war_cards()['Player One']
        war_card_player_two = self.get_war_cards()['Player Two']
        print(f'{player_one.name} drops:', war_card_player_one)
        print(f'{player_two.name} drops:', war_card_player_two)
        if Deck.power_of_rank[war_card_player_one[:-1]] > Deck.power_of_rank[war_card_player_two[:-1]]:
            player_one.gain_card(self.cards_on_table)
            return 'break'
        elif Deck.power_of_rank[war_card_player_one[:-1]] < Deck.power_of_rank[war_card_player_two[:-1]]:
            player_two.gain_card(self.cards_on_table)
            return 'break'
        else:
            return 'Add cards to table'

    @staticmethod
    def check_possibility_of_next_round(player_one, player_two):
        if player_one.check_deck() < 3 or player_two.check_deck() < 3:
            return 'break'


######################
#### GAME PLAY #######
######################
print("Welcome to War, let's begin...")


'''DECK CREATION'''
deck = Deck(SUITE, RANKS)


'''SHUFFLE DECK'''
deck.shuffle_deck()
deck.shuffle_deck()
print(deck)


'''DECK SPLIT'''
splitted_deck = deck.split_deck()
first_hand = Hand(splitted_deck['First half'])
second_hand = Hand(splitted_deck['Second half'])
print(f'\n\nFirst Hand cards: \n {first_hand.show_deck()} \nSecond Hand cards: \n{second_hand.show_deck()}\n')


'''PLAYERS CREATION'''
print('First Player Name:')
player_one = Player(f'{input()}', first_hand)
print('Second Player Name:')
player_two = Player(f'{input()}', second_hand)


'''GAME CORE'''
round_number = 1
while True:
    print(f'\nRound number: {round_number} START!')
    round = Round()
    while True:
        for i in range(3):
            round.add_card_to_table(player_one.play_card())
            round.add_card_to_table(player_two.play_card())
        round_result = round.play_a_round(player_one, player_two)
        next_round_possibility = round.check_possibility_of_next_round(player_one, player_two)
        if round_result == 'break' or next_round_possibility == 'break':
            break
        else:
            print('Round draw. Playing more cards..')
    player_one.show_deck()
    player_two.show_deck()
    round_number += 1
    time.sleep(2)
    if next_round_possibility == 'break':
        break

'''CONGRATS FOR WINNER'''
if player_one.check_deck() < 3:
    print(f'\nCongrats {player_two.name} YOU HAVE WON!\n')
else:
    print(f'\nCongrats {player_two.name} YOU HAVE WON!\n')
print(f'Game took {round_number} rounds')
