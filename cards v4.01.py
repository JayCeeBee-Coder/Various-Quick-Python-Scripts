'''
********************************************************************************************************
Fun Friday ACI project 
JC Boissy
V3.5 Aug 5 24:------------------------------------------------------------------------------------------
    -   Added cards ranking
V4.0 Aug 2024:------------------------------------------------------------------------------------------
    - Added cards points value (renamed a few class variables to properly use 'face')
    - Added ability to draw card face down
    - Added game of 21/Blackjack ...
V4.0 Aug 9 24:------------------------------------------------------------------------------------------
    - Fixed bug in play21(): Needed to ensure that the dealer gets a change to hit at every cycle
********************************************************************************************************
'''

import os
from time import sleep
from random import shuffle #This function is useful for shuffling my deck

# Clear Screen function
def cls():
    os.system('cls' if os.name=='nt' else 'clear')

# ------------------------------------------------------------------------------------------------------
# CardsInfo class: This will store all the info on each possible card in the deck
# ------------------------------------------------------------------------------------------------------
class CardsInfo:
    def __init__(self, points_val: list[int] = []) -> None: # When CardsInfo is initialized, points valuecan be added as an ordered list of integers matching faces
        self.suits = ['♠', '\033[91m♦\33[0m', '\033[91m♥\33[0m', '♣']
        self.faces = [' 2',' 3',' 4',' 5',' 6',' 7',' 8',' 9','10',' J',' Q', ' K', ' A']
        self.udfaces = [' S',' \u0190',' \u03DE',' \u03DB',' 9',' \u1228',' 8',' 6','0\u0196',' \u017F',' \u00D2', ' \u029E', ' \u2200'] # Upside down for display
        self.ranks = [2,3,4,5,6,7,8,9,10,11,12,13,14]
        self.data = [] # Create a list of dictionaries aggregating the different cards' info
        pval = 0
        for i in range(len(self.faces)):
            if len(points_val) >= i+1:
                pval = points_val[i]
            self.data.append(dict(face = self.faces[i], udface = self.udfaces[i], rank = self.ranks[i], value = pval))


# ------------------------------------------------------------------------------------------------------
# Card class
# ------------------------------------------------------------------------------------------------------
class Card:
    def __init__(self, suit: str, face: str, udface: str, rank: int, value:int = 0):
        self.suit = suit
        self.face = face
        self.udface = udface
        self.rank = rank
        self.points_val = value
        
        fc = self.face
        if fc[0] == ' ':
            fc = fc[::-1] # fc is only used to place the face properly on the top of the card by moving the space to the end if one exists
        self.printL = [] # Line by line ASCII art drawing of the card
        self.printL.append('┌───────┐')
        self.printL.append('│{}     │'.format(fc))
        self.printL.append('│{}      │'.format(self.suit))
        self.printL.append('│   {}   │'.format(self.suit))
        self.printL.append('│      {}│'.format(self.suit))
        self.printL.append('│     {}│'.format(self.udface))
        self.printL.append('└───────┘')
        
        self.printLD = [] # Line by line ASCII art drawing of the card face down
        self.printLD.append('┌───────┐')
        self.printLD.append('│✭✫✭✫✭✫✭│')
        self.printLD.append('│✫✭✫✭✫✭✫│')
        self.printLD.append('│✭✫✭✫✭✫✭│')
        self.printLD.append('│✫✭✫✭✫✭✫│')
        self.printLD.append('│✭✫✭✫✭✫✭│')
        self.printLD.append('└───────┘')


    def __str__(self):
        return(f'[{self.face}{self.suit}]')
        
    # This function draws a picture of the card. A number of blank characters can be added for padding to the left
    def drawPic(self, space:int = 0, up:bool = True):
        if up:
            for l in self.printL:
                print(' ' * space, l)
        else:
            for l in self.printLD:
                print(' ' * space, l)

# ------------------------------------------------------------------------------------------------------       
# Deck class
# ------------------------------------------------------------------------------------------------------
class Deck:
    def __init__(self):
        self.cards = []
        self.index = 0
        self.total = 0

    def __str__(self):
        rStr = ""
        for card in self.cards:
            rStr += f"{card.__str__()}, "
        return rStr[:-2] # removing the last comma and space from the returned string
        
    def addCard(self, card):
        self.cards.append(card)
        self.total += card.points_val
        
    def reset(self):
        self.cards.clear()
        self.index = 0
        
    def dealnext(self): # This function moves through the shuffled deck and returns the next card.
        if self.index == len(self.cards):
            return None # If last card has already been dealt, return None
        else:
            self.index += 1 # The index s used to keep the current position in the deck. We could have popped the top card from teh deck but I prefer leaving it intact for now.
            return self.cards[self.index - 1]

    def getCard(self, indx): # Returns the card at specified zero-based index in the hand 
        return self.cards[indx]
        
    def drawPic(self, up = [True]):
        pic = ''
        if len(self.cards) > 11: # More than 11 cards just takes too much screen real-estate
            pic = self.__str__()
        else:
            if len(self.cards) > 0:
                n_up = len(up)
                for l in range(len(self.cards[0].printL)): # We need to concatenate the cards representation line by line
                    ct = 0
                    for c in self.cards:
                        if (n_up == 1 and up[0]) or (n_up < ct+1 and up[0]) or up[ct-1]:
                            pic += c.printL[l]
                        else:
                            pic += c.printLD[l]
                        ct += 1
                    pic+= '\n'
        print(pic, end='')

# ------------------------------------------------------------------------------------------------------
# Full deck class.This one containes 50 cards.
# ------------------------------------------------------------------------------------------------------
class FullDeck(Deck):
    def __init__(self, point_vals: list[int] = []):
        super().__init__()
        # Build the deck...
        self.cards_data = CardsInfo(point_vals)
        for suit in self.cards_data.suits:
            for c in self.cards_data.data:
                self.addCard(Card(suit, c.get('face'), c.get('udface'), c.get('rank'), c.get('value')))
        self.shuffle()

    def shuffle(self):
        shuffle(self.cards)

#-------------------------------------------------------------------------------------------------------
# Function to draw a list of hands/piles... We will call this often to create the illusion of animation
#-------------------------------------------------------------------------------------------------------
def paint_hands(hands: list[Deck], names: list[str], up: list[bool] = [True], clear: bool = False, scores: list[int] = []):
    if clear:
        cls() # clear the screen first

    nP = 1
    for hand in hands:
        print(f"\033[91m{names[nP-1]:}:\33[0m")
        hand.drawPic(up)
        nP +=1
        if scores:
            print('Score(s):', scores)
            if 21 in scores:
                print('\033[92m[WINNER 21!]\33[0m')
                game_over = True
            elif scores[0] > 21:
                print('\033[91m[BUST!]\33[0m')
                game_over = True
    print()


# ------------------------------------------------------------------------------------------------------
# Magic Trick
# ------------------------------------------------------------------------------------------------------
def abracadabra():
    cls()
    print(".・。.・゜✭・.・✫・゜・。.WELCOME TO JC'S GREATEST CARD TRICK!.・。.・゜✭・.・✫・゜・。.\n")
    
    # Initialize a deck and 3 player hands and a magicPile that will contain the 21 cards involved in teh trick
    theDeck = FullDeck()
    pile1 = Deck()
    pile2 = Deck()
    pile3 = Deck()
    magicPile = Deck()
    
    # Placing the hands in a list...
    piles = []
    piles.append(pile1)
    piles.append(pile2)
    piles.append(pile3)
    
    # Deal 21 cards to the magicPile. This is our working deck
    for c in range(21):
            magicPile.addCard(theDeck.dealnext())
    
    # Show the magic pile and ask for a pick
    input(f"Pick a card from the below, make sure to remember it, and hit Enter when ready...\n{magicPile.__str__()} ")
    print("\nI'll bet you anything that I can guess your card with just 3 vague clues...")
    
    for p in range(3):
        print (f"\nPASS {p+1} OF 3 --------------------------------------------")
        # Split the cards between the 3 hands
        i = 0
        for i in range(7):
            for h in range(3):
                cls()
                piles[h].addCard(magicPile.dealnext()) # Deal a card
                print(f"Look a the following piles...")
                paint_hands(hands = piles, names = ['Pile #1', 'Pile #2', 'Pile #3']) # Draw the hands. We repeatthat to create the animation
                sleep(0.15)

        # Ask player to ID the hand containing the picked card
        pick = "x"
        while not pick.isdigit() or int(pick) > 3:
            pick = input("\033[31mWhich pile is your card in: 1, 2, or 3?\033[0m ")
        
        # Re-pile the hands, making sure that the selected one is in th middle...
        iPick = int(pick)-1
        piles[1], piles[iPick] = piles[iPick], piles[1] # This just swaps the midle pile with the selection
        magicPile.reset()
        for pile in piles:
            nextcard = pile.dealnext()
            while not (nextcard is None):
                    magicPile.addCard(nextcard)
                    nextcard = pile.dealnext()
        
        # Reset hands for next iteration...
        pile1.reset()
        pile2.reset()    
        pile3.reset()
    
        cls() # Clear the screen
    
    print("\n\33[91m☆.｡.:*\033[32m...I GOT IT!!! YOUR CARD IS...\033[0m\33[91m.｡.:*☆\033[0m")
    sleep(0.5)
    magicPile.getCard(10).drawPic(15)
    
    print("\n 👏👏👏 AND THE CROWD GOES WILD! 👏👏👏\n")


# ------------------------------------------------------------------------------------------------------
# 21/Blackjack Game based on the rules here: https://www.instructables.com/How-to-Play-21Blanckjack/
# ------------------------------------------------------------------------------------------------------

def play21() -> str:
    game_over = False
    points = [2,3,4,5,6,7,8,9,10,10,10,10,11]
    theDeck = FullDeck(points)
    player1 = Deck()
    dealer = Deck()
    p1_points = []
    dl_points = []
    deal = 1

    def calc_Score(hand: Deck, dealer_hand = False) -> list[int]:
        scores = [hand.total]
        # Find the number of aces in the hand
        faces = [c.face for c in hand.cards]
        num_aces = faces.count(' A')
        if not dealer_hand:
            for a in range(num_aces):
                scores.append(scores[0] - ((a+1)*10)) # Aces can be 1 instead of 11 so there are alternate scores
        else:
            if scores[0] < 17:
                scores[0] -= (num_aces*10) # Dealer's aces count for 1 if the total is less than 17, and 11 otherwise

        scores.sort()
        return scores

    def dealer_hit():
        nonlocal dl_points
        dealer.addCard(theDeck.dealnext())
        cls()
        dl_points = calc_Score(hand = dealer, dealer_hand = True)
        paint_hands(hands = [dealer], names = ['Dealer'], up = dealer_cards_up, scores = dl_points)
        paint_hands(hands = [player1], names = ['You'], scores = p1_points)
        print()

    dealer_cards_up = [True, False] # Dealer's first card will be shown, second card will be face down
    # Deal 2 cards to each
    for i in range(2):
        cls()
        player1.addCard(theDeck.dealnext())
        dealer.addCard(theDeck.dealnext())
        dl_points = calc_Score(hand = dealer, dealer_hand = True)
        paint_hands(hands = [dealer], names = ['Dealer'], up = dealer_cards_up)
        sleep(0.25)
        print()
        p1_points = calc_Score(player1)
        paint_hands(hands = [player1], names = ['You'], scores = p1_points)
        sleep(0.25)

    while not game_over:
        move = ''
        deal += 1
        while move.lower() != 'h' and move.lower() != 's' and not game_over:
            if deal == 2:
                    dealer_cards_up = [True, True] # This will flip the dealer's cards

            move = input('\033[34mYour move! Do you want to Hit(H) or Stay(S)? \33[0m')

        # Player's move
        if move.lower() == 'h':
            cls()
            dl_points = calc_Score(hand = dealer, dealer_hand = True)
            paint_hands(hands = [dealer], names = ['Dealer'], up = dealer_cards_up, scores = dl_points)
            print()
            player1.addCard(theDeck.dealnext())
            p1_points = calc_Score(player1)
            paint_hands(hands = [player1], names = ['You'], scores = p1_points)
            sleep(0.25)

            if p1_points[0] >= 21:
                game_over = True
        else:
            game_over = True

        # Dealer move
        if dl_points[0] < 17:
            dealer_hit()


    # re-paint the hands
    cls()
    paint_hands(hands = [dealer], names = ['Dealer'], scores = dl_points)
    paint_hands(hands = [player1], names = ['You'], scores = p1_points)
    
    # Dealer is required to hit until they get to 17 or beyond
    while dl_points[0] < 17:
        dealer_hit()
    
    # Declare a winner
    p = 0
    d = 0
    i = 1
    p = p1_points[-i]
    while p > 21 and i < len(p1_points):
        i += 1
        p = p1_points[-i]
    if p >21:
        p = 0
    if dl_points[0] <= 21:
        d = (dl_points[0])

    retstr = ''
    if  p == d:
        print("\033[34mIT'S A DRAW!\33[0m")
        retstr = 'D'
    elif p > d:
        print("\033[92mYOU WON!\33[0m")
        retstr = 'W'
    else:
        print("\033[91mYOU LOST!\33[0m")
        retstr = 'L'

    print()
    return retstr


# ------------------------------------------------------------------------------------------------------
# Execution script
# -----------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    cls()
    print(".・。.・゜✭・.・✫・゜・。.WELCOME TO JC'S FUN FRIDAY!.・。.・゜✭・.・✫・゜・。.\n")
    print('\033[91mMAKE SURE TO ENLARGE YOUR CONSOLE WINDOW!\33[0m\n')
    pick = input ("Would you like to see a \033[91mMagic Trick (type 'M')\33[0m, or play \033[91m21/Blackjack (type 'B')\33[0m?")
    play_again = 'Y'

    if pick.lower() == 'm':
        while play_again.lower() == 'y':
            abracadabra()
            play_again = input('\033[91mDo you want to see the trick again?\33[0m ')
    elif pick.lower() == 'b':
        wins = 0
        losses = 0
        draws = 0
        while play_again.lower() == 'y':
            result = play21()
            if result == 'W':
                wins += 1
            elif result == 'L':
                losses += 1
            elif result == 'D':
                draws += 1
            print(f'\033[34mYou have {wins} win(s), {losses} loss(es), and {draws} draw(s)\33[0m\n')
            play_again = input('\033[91mDo you want to play again? (Y/N)\33[0m ')
    else:
        print("\nIt's a shame to be missing out on so much fun!")
    print('\nThanks for playing!\n')

