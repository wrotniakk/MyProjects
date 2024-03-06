# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 21:37:50 2021

@author: kwwro

BlackJack
"""
import random

values = {'Two':2,'Three':3,'Four':4,'Five':5,'Six':6,'Seven':7,'Eight':8,'Nine':9,'Ten':10,'Jack':10,'Queen':10,'King':10,'Ace':11}
suits = ['Spades','Hearts','Diamonds','Clubs']
ranks = ['Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Jack','Queen','King','Ace']


class Bank:
    
    def __init__(self, cash):
        self.cash = cash
        
    def fund(self, amount):
        self.cash += 2 * amount
        
    def pay(self, amount):
        self.cash -= amount
        
    def __str__(self):
        return f"${self.cash} in the Bank"
    
    def __lt__(self,value):
        return self.cash < value
        
    def __gt__(self, value):
        return self.cash > value
    
class Card:
    
    def __init__(self,suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]
    
    def __str__(self):
        return self.rank + " of " + self.suit + f"(value: {self.value})"
    
    def __lt__(self,Card):
        return self.value < Card.value
    
    def __eq__(self,Card):
        return self.value == Card.value
    
    def __gt__(self,Card):
        return self.value > Card.value
    
    def __eq__(self,name):
        return self.rank == name 
    
class Hand:
    
    def __init__(self,cards):

        if type(cards) == type([]):
            self.cards = cards
            self.value = 0
            for card in cards:
                self.value += values[card]
        else:
            self.cards = [cards]
            self.value = values[cards]
        
    def add_card(self,card):
        if type(card) == type([]):
            self.cards.extend(card)
            for c in card:
                self.value += values[c.rank]
        else:
            self.cards.append(card)
            self.value += values[card.rank]


class Player:
    
    def __init__(self,name, Bank):
        self.name = name
        
        self.bank = Bank
        self.hand = Hand([])

    def fund(self,amount):
        self.bank.fund(amount)
        
    def pay(self, amount):
        self.bank.pay(amount)

    def __str__(self):
        return self.name
    
    def add_to_hand(self,card):
        self.hand.add_card(card)
            
    def clear_hand(self):
        self.hand = Hand([])

class Deck:
    '''
    Kept as a list. Top cart is the last one in the list, bottom card is the first one
    '''
    
    def __init__(self):
        
        self.cards = []
        
        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(suit,rank))
                
    def shuffle_deck(self):
        random.shuffle(self.cards)
        
    def draw(self):
        return self.cards.pop()
    
    def __iter__(self):
        for i in range(len(self.cards)):
            yield self.cards[i]
            
    def __getitem__(self,i):
        if i < 0: i = len(self.cards) + i
        if not 0 <= i < len(self.cards): raise IndexError()
        return self.cards[i]
    
def game(name,deck,cash,player,dealer):
        
    '''
    The actual game:
    '''
    # Preparation

    print(f"\nAlright, {name}! You have ${player.bank.cash} in your bank. Lets roll!")

    deck.shuffle_deck()

    bid = int(input("How much do you want to bid?: "))

    while bid > player.bank:
        print("Sorry, but you dont have that much money:")
        bid = int(input("How much do you want to bid?: "))

    # Start

    print(f"\n{player.name} draws 2 cards...\n")
        
    card1 = deck.draw()
    print(card1)
    card2 = deck.draw()
    print(card2)
    
    player.add_to_hand([card1,card2])
    print(f"Thats {player.hand.value} points.\n")
    
    if player.hand.value == 21:
        print('BLACKJACK! You win:')
        player.fund(bid)
        return "Game ends"
        
    if player.hand.value > 21 and "Ace" in [card1,card2]:
        # Value of the Ace is set for 1 (instead of 11)
        player.hand.value -= 10  
    if player.hand.value > 21:
        print("Thats more than 21... you loose.")
        player.pay(bid)
        return "Game ends"
    
    print("Dealer draws 2 cards...\n")
    
    card1 = deck.draw()
    print(card1)
    card2 = deck.draw()
    print("Second card remains unknown...")
    
    dealer.add_to_hand([card1,card2])
    
    # Drawing till success/tie/failure

    game_on = True
    while game_on: # a workaround for when it's a tie (see: at the end)
        
        count = 0
        option = input("Do you draw? Y or N: ")
        
        while option == 'Y' and count <= 4:
            count += 1
            print(f"\n{player.name} draws 1 card...")
            card = deck.draw()
            print(card)
        
            player.add_to_hand(card)
            print(f"Thats {player.hand.value} points.")
            
            if player.hand.value > 21 and "Ace" == card:
                player.hand.value -= 10  # Value of the Ace is set for 1 (instead of 11)
            if player.hand.value > 21:
                print("Thats more than 21... you loose.")
                player.pay(bid)
                return "Game ends"
            if count < 5:
                option = input("Do you draw? Y or N: ")
            else: break
        
        print("Dealer's turn\n")
        print(f"Previous card: {card2}")
        if dealer.hand.value > 21 and "Ace" in [card1,card2]:
            dealer.hand.value -= 10  # Value of the Ace is set for 1 (instead of 11)
        if dealer.hand.value > 21:
            print("Thats more than 21... you win!.")
            player.fund(bid)
            return "Game ends"
            
        while dealer.hand.value <= 17:
            print("Dealer draws 1 card...\n")
            
            card = deck.draw()
            print(card)
            
            dealer.add_to_hand(card)
            
            print(f"Thats {dealer.hand.value} points.\n")
    
            
            if dealer.hand.value > 21 and "Ace" == card:
                dealer.hand.value -= 10  # Value of the Ace is set for 1 (instead of 11)
            if dealer.hand.value > 21:
                print("Thats more than 21... you win!.")
                player.fund(bid)
                return "Game ends"
    
        if player.hand.value > dealer.hand.value:
            print("You got more than the Dealer! You win!")
            player.fund(bid)
        elif player.hand.value < dealer.hand.value:
            print("Dealer got more... you loose.")
            player.pay(bid)
        else:
            print("Thats a tie!")
        
        game_on = False

def main():
    
    deck = Deck()
    dealer = Player('Dealer', Bank(0))
    print("Welcome to our epic non-addictive game of BlackJack! Lets begin:\n")
    name = input("State your player name: ")
    cash = int(input("How much money $$$ you wanna deposit: "))
    
    player = Player(name,Bank(cash))
    
    tryNum = 1
    
    while player.bank > 0:
        
        '''
        The tryNum check is for eventual replaying. Gets ignored if played the first time (tryNum = 1)
        '''

        if tryNum > 1:
            play_on = input("Fancy another round? [Y/N]: ")

            while play_on not in ['Y','N']:
                print('\nInvalid answer...')
                play_again = input("Fancy another round? Y or N: ")
            
            if play_on == 'N':
                return f"Sure, champ. You leave with {player.bank.cash} in your bank. Come back anytime!"
            
        game(name,deck,cash,player,dealer)

        player.clear_hand()
        dealer.clear_hand()

        tryNum += 1
    
    return "I'm sorry, you're out of money. Try to get some and come back when ready!"

main()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
