import random
import string
from enum import Enum

class Card():
    suit = "?"
    rank = 0
    hidden = True
    def rank_str_to_int(rank: string):
        if rank == "A":
            return 1
        elif rank == "2":
            return 2
        elif rank == "3":
            return 3
        elif rank == "4":
            return 4
        elif rank == "5":
            return 5
        elif rank == "6":
            return 6
        elif rank == "7":
            return 7
        elif rank == "8":
            return 8
        elif rank == "9":
            return 9
        elif rank == "T":
            return 10
        elif rank == "J":
            return 11
        elif rank == "Q":
            return 12
        elif rank == "K":
            return 13
        else:
            return -1
    
    def __init__(self, rank=0, suit="?"):
        self.rank = rank
        self.suit = suit
    def __str__(self):
        if self.hidden:
            return "##"
        elif self.rank == 1:
            return "A" + self.suit
        elif self.rank == 2:
            return "2" + self.suit
        elif self.rank == 3:
            return "3" + self.suit
        elif self.rank == 4:
            return "4" + self.suit
        elif self.rank == 5:
            return "5" + self.suit
        elif self.rank == 6:
            return "6" + self.suit
        elif self.rank == 7:
            return "7" + self.suit
        elif self.rank == 8:
            return "8" + self.suit
        elif self.rank == 9:
            return "9" + self.suit
        elif self.rank == 10:
            return "T" + self.suit
        elif self.rank == 11:
            return "J" + self.suit
        elif self.rank == 12:
            return "Q" + self.suit
        elif self.rank == 13:
            return "K" + self.suit
        else:
            return "X" + self.suit


class MoveType(Enum):
    SETUP = 1
    DECK = 2
    TALONTOCOL = 3
    TOFOUNDATION = 4
    COLTOCOL = 5
    FOUNDATIONTOCOL = 6
    NOMOVE = 7
    #TALONTOFOUNDATION = 
    #COLTOFOUNDATION = 
    

class SolitaireMove():
    move_number = 0
    def __init__(self, move_type: MoveType, origin: list, destination: list, n_cards: int):
        self.move_type = move_type
        self.origin = origin
        self.destination = destination
        self.n_cards = n_cards

        self.move_number = SolitaireMove.move_number
        SolitaireMove.move_number += 1

    def execute_move(self):
        temp_list = []
        for i in range(self.n_cards):
            temp_card = self.origin.pop()
            temp_list.append(temp_card)
        for i in range(self.n_cards):
            temp_card = temp_list.pop()
            self.destination.append(temp_card)

    def reverse_move(self):
        temp = []
        for i in range(self.n_cards):
            temp.append(self.destination.pop())
        for i in range(self.n_cards):
            self.origin.append(temp.pop())


class DeckMove(SolitaireMove):
    def __init__(self):
        super().__init__(MoveType.DECK, SolitaireBoard.deck, SolitaireBoard.waste, 1) # change to 3
    def execute_move(self):
        #if len(self.origin) + len(self.destination) < 3:
        #    raise ValueError
        
        if len(self.origin) - self.n_cards < 0:
            print("VENDER BUNKEN...")
            while self.origin:
                self.destination.append(self.origin.pop())
            while self.destination:
                self.origin.append(self.destination.pop())                
            self.origin.reverse()
        return super().execute_move()

class TalonToColMove(SolitaireMove):
    def __init__(self, destination):
        super().__init__(MoveType.TALONTOCOL, SolitaireBoard.waste, destination, 1)

#class TalonToFoundationMove(SolitaireMove):
#    def __init__(self, destination):
#        super().__init__(MoveType.TALONTOFOUNDATION, SolitaireBoard.waste, destination, 1)

#class ColToFoundationMove(SolitaireMove):
#    def __init__(self, origin, destination):
#        super().__init__(MoveType.COLTOFOUNDATION, origin, destination, 1)

class ToFoundationMove(SolitaireMove):
    def __init__(self, origin, destination):
        super().__init__(MoveType.TOFOUNDATION, origin, destination, 1)

class ColToColMove(SolitaireMove):
    def __init__(self, origin, destination, count):
        super().__init__(MoveType.COLTOCOL, origin, destination, count)

class FoundationToColMove(SolitaireMove):
    def __init__(self, origin, destination):
        super().__init__(MoveType.FOUNDATIONTOCOL, origin, destination, 1)

class NoMoveMove(SolitaireMove):
    def __init__(self):
        super().__init__(MoveType.NOMOVE, [], [], 0)


class SolitaireBoard():
    deck = []
    waste = []
    foundations = [[], [], [], []]
    columns = [[], [], [], [], [], [], []]
    current_move = NoMoveMove()

    #### NONE OF THESE SHOULD ACTUALLY BE USED
    #### ALL CARDS SHOULD BE GENERATED AS PLACEHOLDER CARDS AT THE START
    #### AND THEN UPDATED WITH CORRECT SUIT AND RANK AS THEY ARE REVEALED
    def append_to_deck(self, cards):
        for c in cards:
            self.deck.append(c)
    def append_to_waste(self, cards):
        for c in cards:
            self.waste.append(c)
    def append_to_foundations(self, cards):
        if len(cards) == len(self.foundations):
            x = 0
            for f in cards:
                for c in f:
                    self.foundations[x].append(c)
                x += 1
    def append_to_columns(self, cards):
        if len(cards) == len(self.columns):
            x = 0
            for col in cards:
                for c in col:
                    self.columns[x].append(c)
                x += 1
    ####-----------------------------------------
    ####-----------------------------------------
    
    # THIS NEEDS UPDATING TOO
    def load_with_cards(self, cards):
        if len(cards) == 4:
            self.append_to_deck(cards[0])
            self.append_to_waste(cards[1])
            self.append_to_foundations(cards[2])
            self.append_to_columns(cards[3])


    def create_deck():
        SolitaireBoard.deck = []
        for x in range(1, 14, 1):
            SolitaireBoard.deck.append(Card(x, 'D'))
            SolitaireBoard.deck.append(Card(x, 'C'))
            SolitaireBoard.deck.append(Card(x, 'H'))
            SolitaireBoard.deck.append(Card(x, 'S'))

    def shuffle_deck():
        random.shuffle(SolitaireBoard.deck)
        return

    def new_game():
        SolitaireBoard.deck = []
        SolitaireBoard.columns = [[], [], [], [], [], [], []]
        SolitaireBoard.foundations = [[], [], [], []]
        SolitaireBoard.waste = []
        SolitaireBoard.create_deck()
        SolitaireBoard.shuffle_deck()
        for i in range(7):
            for j in range(i+1):
                e = SolitaireBoard.deck.pop()
                SolitaireBoard.columns[i].append(e)
            SolitaireBoard.columns[i][-1].hidden = False

        #count hidden cards in each column and return a number of hidden cards for each column
    def count_hiddencards():
        hiddencolumn = []
        # count hidden cards in each column and return a number of hidden cards for each column
        hidden_cards = 0
        for col in SolitaireBoard.columns:
            for card in col:
                if card.hidden:
                    hidden_cards += 1
                else:
                    break
            hiddencolumn.append(hidden_cards)
            print(hiddencolumn[hidden_cards])
            hidden_cards = 0
        return hiddencolumn
    # sort columns from most hidden cards to least hidden cards
    def sorted_hiddencolumn():
        temp_list = SolitaireBoard.count_hiddencards()
        sorted = []
        for i in range(7):
            sorted.append(temp_list.index(max(temp_list)))
            temp_list.pop(max(temp_list))
        return sorted






    def identify_cards(cards):
        identified_deck, identified_waste, identified_foundations, identified_columns = cards
        if SolitaireBoard.waste and SolitaireBoard.waste[-1].hidden:
            SolitaireBoard.waste[-1].hidden = False
            SolitaireBoard.waste[-1].rank = identified_waste[-1].rank
            SolitaireBoard.waste[-1].suit = identified_waste[-1].suit

        col_index = 0
        for col in SolitaireBoard.columns:
            if col and col[-1].hidden:
                col[-1].hidden = False
                col[-1].rank = identified_columns[col_index][-1].rank
                col[-1].suit = identified_columns[col_index][-1].suit
            col_index += 1


    def reveal_card():
        if SolitaireBoard.waste:
            SolitaireBoard.waste[-1].hidden = False
        for col in SolitaireBoard.columns:
            if col:
                col[-1].hidden = False


    #def draw_from_deck(self):
    #    move = DeckMove()
    #    move.execute_move()

    """         
        if len(self.deck) > 0:
            card = self.deck.pop()
            card.hidden = False
            self.waste.append(card)
        elif len(self.deck) == 0 and len(self.waste) > 0:
            self.deck = self.waste[:]
            self.deck.reverse()
            self.waste = []
            for c in self.deck:
                c.hidden = True  """

    def valid_to_col_move(card, dest_column):
        if len(dest_column) == 0:
            return card.rank == 13
        else:
            dest_card = dest_column[-1]
            valid_ranks = card.rank == dest_card.rank - 1
            if card.suit == 'D' or card.suit == 'H':
                valid_suit = dest_card.suit == 'C' or dest_card.suit == 'S'
            elif card.suit == 'C' or card.suit == 'S':
                valid_suit = dest_card.suit == 'D' or dest_card.suit == 'H'
            else:
                valid_suit = False
            return valid_ranks and valid_suit

    def move_to_col(from_column, to_column, number_of_cards):
        if len(from_column) == 0 or number_of_cards < 0 or from_column == to_column or number_of_cards > len(from_column):
            return
        from_card = from_column[-number_of_cards]
        if from_card.hidden:
            return
        if SolitaireBoard.valid_to_col_move(from_card, to_column):
            move = ColToColMove(SolitaireBoard.columns[from_column], SolitaireBoard.columns[to_column], number_of_cards)
            move.execute_move()

            """ if number_of_cards == 0:
                to_column.extend(to_column)
                from_column[:] = []
            else:
                to_column.extend(from_column[-number_of_cards : ])
                from_column[:] = from_column[ : -number_of_cards]
                if len(from_column) > 0:
                    from_column[-1].hidden = False """

    def valid_to_foundation_move(card, dest_foundation):
        if len(dest_foundation) == 0:
            return card.rank == 1
        else:
            dest_card = dest_foundation[-1]
            return card.suit == dest_card.suit and card.rank == dest_card.rank + 1

    def OLDmove_to_foundation(self, column, foundation):
        if len(column) == 0:
            return

        card = column[-1]
        if self.valid_to_foundation_move(card, foundation):
            foundation.append(column.pop())
            if len(column) > 0:
                column[-1].hidden = False

    def print_board(self):
        print("D:\t[]") if len(self.deck) == 0 else print("D:\t##")
        print("W:\t[]") if len(self.waste) == 0 else print("W:\t" + str(self.waste[-1]))
        i = 0
        for f in self.foundations:
            print("F" + str(i) + ":\t[]") if len(f) == 0 else print("F" + str(i) + ":\t" + str(f[-1])) 
            i += 1
        i = 0
        for col in self.columns:
            if len(col) == 0:
                print("C" + str(i) + ":\t[]") 
            else:
                print("C" + str(i) + ":\t", end='')
                for card in col:
                    print(str(card) + " ", end='')
                print()
            i += 1

#       #      # # # # #      
#      # #         #         
#     #   #        # 
#    # # # #       #  
#   #       #      #           
#  #         # # # # # #            
# - Led efter næste kort til en foundation
#   - Hvis det er fri, flyt til foundation
#   - Ellers, rekursivt se om det kan frigøres (max dybde fx 3)
# - Forsøg at vende et kort fra en kolonne (rekursivt på samme måde)
# - Vend et kort fra bunken
    def suggest_move():
        # - Tjek om næste kort til en foundation ligger frit
        for f in SolitaireBoard.foundations:
            if len(f) == 0:
                res = SolitaireBoard.look_for_ace()
                if len(res) > 0:
                    SolitaireBoard.current_move = ToFoundationMove(res, f)
                    return "MOVE " + str(res[-1]) + " TO A FOUNDATION"
            else:
                temp_card = Card(f[-1].rank + 1, f[-1].suit)
                res = SolitaireBoard.look_for_card(temp_card)
                if len(res) > 0:
                    SolitaireBoard.current_move = ToFoundationMove(res, f)
                    return "MOVE " + str(res[-1]) + " TO A FOUNDATION"

        # ellers, tjek om næste kort til en foundation kan frigøres

        # ellers, tjek om et skjult kort kan frigøres
        k = -1
        for col in SolitaireBoard.columns:
            k += 1
            if col:
                height = 1
                while((height+1) < len(col) and not col[-(height+1)].hidden):
                    height += 1
                temp_card = Card(rank=col[-height].rank + 1, suit=col[-height].suit)
                if temp_card.rank == 14: # look for empty column
                    for res in SolitaireBoard.columns:
                        if len(res) == 0:
                            SolitaireBoard.current_move = ColToColMove(col, res, height)
                            return "MOVE KING TO EMPTY COLUMN"
                else:
                    if temp_card.suit == "H" or temp_card.suit == "D":
                        temp_card.suit = "C"
                        res = SolitaireBoard.look_for_card_in_columns(temp_card)
                        if res:
                            SolitaireBoard.current_move = ColToColMove(col, res, height)
                            return "MOVE TO " + str(res[-1])
                        temp_card.suit = "S"
                        res = SolitaireBoard.look_for_card_in_columns(temp_card)
                        if res:
                            SolitaireBoard.current_move = ColToColMove(col, res, height)
                            return "MOVE TO " + str(res[-1])
                    elif temp_card.suit == "C" or temp_card.suit == "S":
                        temp_card.suit = "H"
                        res = SolitaireBoard.look_for_card_in_columns(temp_card)
                        if res:
                            SolitaireBoard.current_move = ColToColMove(col, res, height)
                            return "MOVE TO " + str(res[-1])
                        temp_card.suit = "D"
                        res = SolitaireBoard.look_for_card_in_columns(temp_card)
                        if res:
                            SolitaireBoard.current_move = ColToColMove(col, res, height)
                            return "MOVE TO " + str(res[-1])
                    else:
                        raise ValueError
        
        # Tjek om et et kort fra talon kan flyttes fra talon ud på en kolonne
        if SolitaireBoard.waste:
            temp_card = Card(rank=SolitaireBoard.waste[-1].rank + 1, suit=SolitaireBoard.waste[-1].suit)
            if temp_card.rank == 14: # look for empty column
                for res in SolitaireBoard.columns:
                    if len(res) == 0:
                        SolitaireBoard.current_move = TalonToColMove(res)
                        return "MOVE KING TO EMPTY COLUMN"
            else:
                if temp_card.suit == "H" or temp_card.suit == "D":
                    temp_card.suit = "C"
                    res = SolitaireBoard.look_for_card_in_columns(temp_card)
                    if res:
                        SolitaireBoard.current_move = TalonToColMove(res)
                        return "MOVE TO " + str(res[-1])
                    temp_card.suit = "S"
                    res = SolitaireBoard.look_for_card_in_columns(temp_card)
                    if res:
                        SolitaireBoard.current_move = TalonToColMove(res)
                        return "MOVE TO " + str(res[-1])
                elif temp_card.suit == "C" or temp_card.suit == "S":
                    temp_card.suit = "H"
                    res = SolitaireBoard.look_for_card_in_columns(temp_card)
                    if res:
                        SolitaireBoard.current_move = TalonToColMove(res)
                        return "MOVE TO " + str(res[-1])
                    temp_card.suit = "D"
                    res = SolitaireBoard.look_for_card_in_columns(temp_card)
                    if res:
                        SolitaireBoard.current_move = TalonToColMove(res)
                        return "MOVE TO " + str(res[-1])
                else:
                    raise ValueError



        # ellers, vend et kort fra bunken
        SolitaireBoard.current_move = DeckMove()
        return "TURN A CARD FROM THE DECK"

    def new_suggest():
        for f in SolitaireBoard.foundations:
            if len(f) == 0:
                res = SolitaireBoard.look_for_ace()
                if len(res) > 0:
                    SolitaireBoard.current_move = ToFoundationMove(res, f)
                    return "MOVE " + str(res[-1]) + " TO A FOUNDATION"
                else:
                    if len(f) == 1:
                        res = SolitaireBoard.look_for_deuce()
                        if len(res) > 0 and Card(f[-1].suit):
                            SolitaireBoard.current_move = ToFoundationMove(res, f)
                            return "MOVE " + str(res[-1]) + " TO A FOUNDATION"
    def look_for_ace():
        # check waste
        if len(SolitaireBoard.waste) > 0 and SolitaireBoard.waste[-1].rank == 1:
                return SolitaireBoard.waste
        for col in SolitaireBoard.columns:
            if len(col) > 0 and col[-1].rank == 1:
                return col
        return []
    def look_for_deuce():
        # check waste
        if len(SolitaireBoard.waste) > 0 and SolitaireBoard.waste[-1].rank == 2:
                return SolitaireBoard.waste
        for col in SolitaireBoard.columns:
            if len(col) > 0 and col[-1].rank == 2:
                return col
        return []

    def look_for_card_in_columns(card):
        for col in SolitaireBoard.columns:
            if len(col) > 0 and col[-1].rank == card.rank and col[-1].suit == card.suit:
                return col
        return []

    def look_for_card(card):
        if len(SolitaireBoard.waste) > 0 and SolitaireBoard.waste[-1].rank == card.rank and SolitaireBoard.waste[-1].suit == card.suit:
                return SolitaireBoard.waste
        for col in SolitaireBoard.columns:
            if len(col) > 0 and col[-1].rank == card.rank and col[-1].suit == card.suit:
                return col
        return []

# -----------------

if __name__ != "__main__":
    board = SolitaireBoard()
    SolitaireBoard.create_deck()
    SolitaireBoard.shuffle_deck()
    SolitaireBoard.new_game()

    print("************")
    print(len(board.deck))
    print(len(SolitaireBoard.deck))


if __name__ == "__main__":
    board = SolitaireBoard()
    SolitaireBoard.create_deck()
    SolitaireBoard.shuffle_deck()
    SolitaireBoard.new_game()
    print("Game is in auto solve mode..")
    print("Enter any input to continue")
    user_input = input()

    k = 0
    while True:
        board.print_board()
        print()
        print()
        print(SolitaireBoard.suggest_move())
        SolitaireBoard.execute_current_move()
        SolitaireBoard.reveal_card()

        k += 1
        if k == 10: #kør 10 træk ad gangen så man ikke skal taste så meget
            k = 0
            print("Continue..")
            user_input = input()
            if len(user_input) > 3:
                break
        

    