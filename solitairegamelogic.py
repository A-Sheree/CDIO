from asyncio.windows_events import NULL
from queue import PriorityQueue
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

    def testprintcard(self):
        if self.rank == 1:
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

    def __str__(self) -> str:
        if self.move_type == MoveType.SETUP:
            return "INIT"
        elif self.move_type == MoveType.DECK:
            return "DRAW FROM DECK"
        elif self.move_type == MoveType.TALONTOCOL:
            if self.destination:
                return "MOVE " + str(self.origin[-self.n_cards]) + " TO " + str(self.destination[-1])
            else:
                return "MOVE " + str(self.origin[-self.n_cards]) + " TO OPEN COLUMN"
        elif self.move_type == MoveType.TOFOUNDATION:
            return "MOVE " + str(self.origin[-self.n_cards]) + " TO FOUNDATION"
        elif self.move_type == MoveType.COLTOCOL:
            if self.destination:
                return "MOVE " + str(self.origin[-self.n_cards]) + " TO " + str(self.destination[-1])
            else:
                return "MOVE " + str(self.origin[-self.n_cards]) + " TO OPEN COLUMN"
        elif self.move_type == MoveType.FOUNDATIONTOCOL:
            return "MOVE " + str(self.origin[-self.n_cards]) + " TO " + str(self.destination[-1])
        elif self.move_type == MoveType.NOMOVE:
            return "NO MOVE"


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
            #print("VENDER BUNKEN...")
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
    def execute_move(self):
        return


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
        if len(self.deck) == 0:
            print("D:\t##")
        else:
            print("D" + ":\t", end='')
            for card in self.deck:
                print(card.testprintcard() + " ", end='')
            print()
        if len(self.waste) == 0:
            print("W:\t##")
        else:
            print("W" + ":\t", end='')
            for card in self.waste:
                print(card.testprintcard() + " ", end='')
            print()
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

    def new_suggest():
        # Check for Ace og 2'er.
        for f in SolitaireBoard.foundations:
            if len(f) == 0:
                res = SolitaireBoard.look_for_ace()
                if len(res) > 0:
                    SolitaireBoard.current_move = ToFoundationMove(res, f)
                    return
            elif len(f) == 1:
                temp_card = Card(rank=2, suit=f[-1].suit)
                res = SolitaireBoard.look_for_deuce(temp_card)
                if len(res) > 0:
                    SolitaireBoard.current_move = ToFoundationMove(res, f)
                    return

                    # check med Tobias om dette er rigtigt kaldt eller om vi misser noget?

        # Gør altid træk der tillader at vende et kort.
        
        for col in SolitaireBoard.columns:
            if col and col[0].hidden: # indeholder et skjult kort
                # Find det øverste synlige kort i kolonnen
                index = -1
                while col[index - 1].hidden == False:
                    index -= 1

                # lav en midlertidig kopi af kortet
                temp_card = Card(rank=col[index].rank, suit=col[index].suit)

                # Frigør ved at flytte et kort til foundation
                if index == -1: 
                    res = SolitaireBoard.look_for_foundation_destination(temp_card)
                    if res:
                        SolitaireBoard.current_move = ToFoundationMove(col, res)
                        return

                # Frigør ved at flytte en konge til en tom kolonne
                if temp_card.rank == 13: 
                    temp_move = SolitaireBoard.make_way_for_the_king(col, index)
                    if temp_move.move_type != MoveType.NOMOVE:
                        SolitaireBoard.current_move = temp_move
                        return
                # Frigør ved at flytte kort fra en kolonne til en anden kolonne
                else:
                    res = SolitaireBoard.look_for_column_destinatination(temp_card)
                    if res:
                        SolitaireBoard.current_move = ColToColMove(col, res, abs(index))
                        return
                    else:
                        # Tjek om et kort fra talon kan hjælpe med at frigøre
                        res = SolitaireBoard.look_for_talon_destination(temp_card)
                        if res:
                            talon_card = SolitaireBoard.waste[-1]
                            if talon_card.rank == 13: #look for empty column
                                temp_move = SolitaireBoard.make_way_for_the_king(SolitaireBoard.waste, -1)
                                if temp_move.move_type != MoveType.NOMOVE:
                                    SolitaireBoard.current_move = temp_move
                                    return
                            else:    
                                res = SolitaireBoard.look_for_column_destinatination(talon_card)
                                if res:
                                    SolitaireBoard.current_move = TalonToColMove(res)
                                    return

    # Altid lav det træk der åbner for den største bunke med kort at vende.

    # Flyt kun fra kolonne til kolonne hvis det tillader at få vendt et kort eller at lave kolonnerne smooth.

    # Ryd ikke et spot med mindre der en konge der klar til at tage spottet.

    # Kun spil en konge hvis kolonnerne med den største bunke af kort der kan vendes
    # eller at spille en anden konge tillader at rykke at rykke fra en kolonne derpå ig vende et kort.

    # Kun byg videre på foundation fra 3+ hvis det ikke påvirke det næste kort beskyttelse
    # eller at det et træk der tillader at lave et spil eller ryk frigør at vende et kort
    # ellers så skal det åbne muligheden for at overføre en bunke af samme farve mønster så der kan vendes et kort
    # eller så frigøre et spot til en konge der venter.

    # Flyt eller ryk kun en 5'er-8'er hvis det tillader at vende et kort med det samme
    # det er smooth med det næste kort I kolonnen
    # der er ikke blevet rykket andre kort til den kolonnen
    # hvis der bare ikke er andre muligheder.

    # alle dine nødvendige kort ser ud til at være i bunkerne som skal vendes
    # flyt straks alle kort som kan op I foundation for måske at kunne åbne
    # for muligheden at lave et træk med et andet kort der allerede findes men er blokeret.


    #...

        # Tjek om et et kort fra talon kan flyttes fra talon ud på en kolonne
        if SolitaireBoard.waste:
            temp_card = Card(rank=SolitaireBoard.waste[-1].rank, suit=SolitaireBoard.waste[-1].suit)
            if temp_card.rank < 5 or (temp_card.rank > 8 and temp_card.rank < 13):
                
                for col in SolitaireBoard.columns:
                    res = SolitaireBoard.look_for_column_destinatination(temp_card)
                    if res:
                        SolitaireBoard.current_move = TalonToColMove(res)
                        return


    #...
        if SolitaireMove.move_number > 80: #start moving cards to foundation
            for col in SolitaireBoard.columns:
                if col:
                    res = SolitaireBoard.look_for_foundation_destination(col[-1])
                    if res:
                        SolitaireBoard.current_move = ToFoundationMove(col, res)
                        return
            if SolitaireBoard.waste:
                res = SolitaireBoard.look_for_foundation_destination(SolitaireBoard.waste[-1])
                if res:
                    SolitaireBoard.current_move = ToFoundationMove(SolitaireBoard.waste, res)
                    return

        if SolitaireMove.move_number > 100: #start moving all ranks from talon to columns
            if SolitaireBoard.waste:
                temp_card = Card(rank=SolitaireBoard.waste[-1].rank, suit=SolitaireBoard.waste[-1].suit)     
                if temp_card.rank == 13: # look for empty column
                    temp_move = SolitaireBoard.make_way_for_the_king(SolitaireBoard.waste, -1)
                    if temp_move.move_type != MoveType.NOMOVE:
                        SolitaireBoard.current_move = temp_move
                        return
                else:
                    for col in SolitaireBoard.columns:
                        res = SolitaireBoard.look_for_column_destinatination(temp_card)
                        if res:
                            SolitaireBoard.current_move = TalonToColMove(res)
                            return

        if SolitaireMove.move_number > 110: #start moving directly from waste to foundation
            if SolitaireBoard.waste:
                temp_card = Card(rank=SolitaireBoard.waste[-1].rank, suit=SolitaireBoard.waste[-1].suit)     
                res = SolitaireBoard.look_for_foundation_destination(temp_card)
                if res:
                    SolitaireBoard.current_move = ToFoundationMove(col, res)
                    return
        # ellers, vend et kort fra bunken
        if len(SolitaireBoard.deck) + len(SolitaireBoard.waste) > 0:
            SolitaireBoard.current_move = DeckMove()
            return
        else:
            SolitaireBoard.current_move = NoMoveMove()
            return

    def look_for_ace():
        # check waste
        if len(SolitaireBoard.waste) > 0 and SolitaireBoard.waste[-1].rank == 1:
                return SolitaireBoard.waste
        for col in SolitaireBoard.columns:
            if len(col) > 0 and col[-1].rank == 1:
                return col
        return []
    def look_for_deuce(card):
        # check waste
        if len(SolitaireBoard.waste) > 0 and SolitaireBoard.waste[-1].rank == 2 and SolitaireBoard.waste[-1].suit == card.suit:
                return SolitaireBoard.waste
        # check columns
        for col in SolitaireBoard.columns:
            if len(col) > 0 and col[-1].rank == 2 and col[-1].suit == card.suit:
                return col
        return []

    def look_for_card_in_columns(card):
        for col in SolitaireBoard.columns:
            if len(col) > 0 and col[-1].rank == card.rank and col[-1].suit == card.suit:
                return col
        return []

    def look_for_talon_destination(original_card):
        if SolitaireBoard.waste and SolitaireBoard.waste[-1].rank == original_card.rank + 1:
            if original_card.suit == "H" or original_card.suit == "D":
                if SolitaireBoard.waste[-1].suit == "C" or SolitaireBoard.waste[-1].suit == "S":
                    return SolitaireBoard.waste
                else:
                    return []
            elif original_card.suit == "C" or original_card.suit == "S":
                if SolitaireBoard.waste[-1].suit == "H" or SolitaireBoard.waste[-1].suit == "D":
                    return SolitaireBoard.waste
                else:
                    return []
        else:
            return []    

    def look_for_foundation_destination(original_card):
        card_to_find = Card(rank=original_card.rank-1, suit=original_card.suit)
        for f in SolitaireBoard.foundations:
            if f:
                if f[-1].rank == card_to_find.rank and f[-1].suit == card_to_find.suit:
                    return f
        return []

    def look_for_column_destinatination(original_card):
        card_to_find = Card(rank=original_card.rank+1)
        if original_card.suit == "H" or original_card.suit == "D":
            card_to_find.suit = "C"
            res = SolitaireBoard.look_for_card_in_columns(card_to_find)
            if res:
                return res
            card_to_find.suit = "S"
            res = SolitaireBoard.look_for_card_in_columns(card_to_find)
            if res:
                return res
        elif original_card.suit == "C" or original_card.suit == "S":
            card_to_find.suit = "H"
            res = SolitaireBoard.look_for_card_in_columns(card_to_find)
            if res:
                return res
            card_to_find.suit = "D"
            res = SolitaireBoard.look_for_card_in_columns(card_to_find)
            if res:
                return res
        return []


    def look_for_card(card):
        if len(SolitaireBoard.waste) > 0 and SolitaireBoard.waste[-1].rank == card.rank and SolitaireBoard.waste[-1].suit == card.suit:
                return SolitaireBoard.waste
        for col in SolitaireBoard.columns:
            if len(col) > 0 and col[-1].rank == card.rank and col[-1].suit == card.suit:
                return col
        return []

    def make_way_for_the_king(king_col, negative_index):
        # led efter en tom plads til kongen
        for res in SolitaireBoard.columns:
            if len(res) == 0:
                return ColToColMove(king_col, res, abs(negative_index))
        # forsøg at rydde en plads til kongen
        for temp_col in SolitaireBoard.columns:
            if temp_col[0].hidden == False:
                res = SolitaireBoard.look_for_column_destinatination(temp_col[0])
                if res:
                    return ColToColMove(temp_col, res, len(temp_col))
        return NoMoveMove()



# -----------------




def debugprintstate(board):
    print("**************************")
    print("Actual move number: " + str(actualmoves))
    print("**************************")

    board.print_board()

def simulate_games(n_games, move_limit):
    sum = 0

    for i in range(n_games):
        SolitaireBoard.new_game()
        moves = 0
        while moves < move_limit:

            SolitaireBoard.new_suggest()
            SolitaireBoard.current_move.execute_move()
            SolitaireBoard.reveal_card()
            moves += 1

            temp = True
            for f in SolitaireBoard.foundations:
                temp = temp and len(f) == 13
            if temp:
                sum += 1
                break
    return sum

if __name__ == "__main__":
    NGAMES = 100
    MOVELIMIT = 500
    print("Simulating " + str(NGAMES) + " solitaires")
    result = simulate_games(NGAMES, MOVELIMIT)
    print(str(result) + " of " + str(NGAMES) + " where solved.")


if __name__ != "__main__":
    board = SolitaireBoard()
    SolitaireBoard.create_deck()
    SolitaireBoard.shuffle_deck()
    SolitaireBoard.new_game()
    print("Game is in auto solve mode..")
    print("Enter any input to continue")
    user_input = input()

    actualmoves = 0

    k = 0
    while True:

        SolitaireBoard.new_suggest()
        print(SolitaireBoard.current_move)
        SolitaireBoard.current_move.execute_move()
        actualmoves += 1
        SolitaireBoard.reveal_card()
        debugprintstate(board)                

        k += 1
        MOVESPERINPUT = 70
        if k > MOVESPERINPUT: #kør flere træk ad gangen så man ikke skal taste så meget
            k = 0
            print("Continue..")
            user_input = input()
            if len(user_input) > 10:
                break
            elif len(user_input) > 3:
                k = MOVESPERINPUT

        # check om kabalen er løst
        temp = True
        for f in SolitaireBoard.foundations:
            temp = temp and len(f) == 13
        if temp:
            print("***************************")
            print("***************************")
            print("SPILLET ER SLUT")
            print("***************************")
            print("***************************")

            board.print_board()

            print("***************************")
            print("***************************")
            break                

        if actualmoves > 500:
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@")
            print("Q_Q Q_Q Q_Q Q_Q Q_Q Q_Q")
            print("KUNNE IKKE FINDE EN LØSNING")
            print("Q_Q Q_Q Q_Q Q_Q Q_Q Q_Q")
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@")
            break

if __name__ != "__main__":
    board = SolitaireBoard()
    SolitaireBoard.create_deck()
    SolitaireBoard.shuffle_deck()
    SolitaireBoard.new_game()

    print("************")
    print(len(board.deck))
    print(len(SolitaireBoard.deck))
