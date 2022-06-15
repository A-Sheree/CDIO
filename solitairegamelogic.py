from asyncio.windows_events import NULL
from queue import Queue
import random
import string
from enum import Enum

from cv2 import sort
from urllib3 import Retry

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
        return self.dansk_str()

    def gammel_str(self):
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

    def dansk_suit(self):
        if self.suit == "H":
            return "H"
        elif self.suit == "D":
            return "R"
        elif self.suit == "C":
            return "K"
        elif self.suit == "S":
            return "S"            

    def dansk_str(self):
        if self.hidden:
            return "##"
        else:
            return self.dansk_suit() + str(self.rank)

    def card_from_string(string_card):
        if len(string_card) == 2:
            rank = Card.rank_str_to_int(string_card[0])
            suit = string_card[1]
            return Card(rank=rank, suit=suit)
        else:
            raise ValueError

    def testprintcard(self):
        
        if self.hidden:
            self.hidden = False
            temp = self.__str__()
            self.hidden = True
            return temp
        else:
            return self.__str__()

class MoveType(Enum):
    SETUP = 1
    DECK = 2
    TALONTOCOL = 3
    TOFOUNDATION = 4
    COLTOCOL = 5
    FOUNDATIONTOCOL = 6
    NOMOVE = 7
    TALONTOFOUNDATION = 8
    #COLTOFOUNDATION = 
    

class SolitaireMove():
    def __init__(self, move_type: MoveType, origin: list, destination: list, n_cards: int):
        self.move_type = move_type
        self.origin = origin
        self.destination = destination
        self.n_cards = n_cards
        self.text_description = self.describe_move()

    def old_describe_move(self) -> str:
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
        elif self.move_type == MoveType.TALONTOFOUNDATION:
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

    def describe_move(self) -> str:
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
        elif self.move_type == MoveType.TALONTOFOUNDATION:
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


    def __str__(self) -> str:
        return self.text_description


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
        super().__init__(MoveType.DECK, SolitaireBoard.deck, SolitaireBoard.waste, 3)
    def execute_move(self):
        #if len(self.origin) + len(self.destination) < 3:
        #    raise ValueError
        
        if len(self.origin) - self.n_cards < 0:
            #print("VENDER BUNKEN...")
            temp_list = []
            while self.origin: #tøm stock
                temp_list.append(self.origin.pop())
            while self.destination: #vend bunken
                self.origin.append(self.destination.pop())      
            while temp_list:
                self.origin.append(temp_list.pop())

        for i in range(self.n_cards):
            self.destination.append(self.origin.pop())   

class TalonToColMove(SolitaireMove):
    def __init__(self, destination):
        super().__init__(MoveType.TALONTOCOL, SolitaireBoard.waste, destination, 1)

class TalonToFoundationMove(SolitaireMove):
    def __init__(self, destination):
        super().__init__(MoveType.TALONTOFOUNDATION, SolitaireBoard.waste, destination, 1)

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
    move_count = 0
    move_history = []
    state_history = []


    def create_deck_unidentified():
        SolitaireBoard.deck = []
        for x in range(52):
            SolitaireBoard.deck.append(Card())


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

    def new_game_from_string(cards):
        SolitaireBoard.deck = []
        SolitaireBoard.waste = []
        SolitaireBoard.foundations = [[], [], [], []]
        SolitaireBoard.columns = [[], [], [], [], [], [], []]
        SolitaireBoard.current_move = NoMoveMove()
        SolitaireBoard.move_count = 0
        SolitaireBoard.move_history = []
        SolitaireBoard.state_history = []

        # split the string and create each card and add it to the deck
        list_of_cards = cards.split()
        for c in list_of_cards:
            SolitaireBoard.deck.append(Card.card_from_string(c))


        for i in range(7):
            for j in range(i, 7):
                e = SolitaireBoard.deck.pop()
                SolitaireBoard.columns[j].append(e)
        SolitaireBoard.reveal_card()

        # for i in range(7):
        #     for j in range(i+1):
        #         e = SolitaireBoard.deck.pop()
        #         SolitaireBoard.columns[i].append(e)
        #     SolitaireBoard.columns[i][-1].hidden = False

    def new_game_unidentified():
        SolitaireBoard.deck = []
        SolitaireBoard.waste = []
        SolitaireBoard.foundations = [[], [], [], []]
        SolitaireBoard.columns = [[], [], [], [], [], [], []]
        SolitaireBoard.current_move = NoMoveMove()
        SolitaireBoard.move_count = 0
        SolitaireBoard.move_history = []
        SolitaireBoard.state_history = []

        SolitaireBoard.create_deck_unidentified()

        for i in range(7):
            for j in range(i, 7):
                e = SolitaireBoard.deck.pop()
                SolitaireBoard.columns[j].append(e)

    def new_game():
        SolitaireBoard.deck = []
        SolitaireBoard.waste = []
        SolitaireBoard.foundations = [[], [], [], []]
        SolitaireBoard.columns = [[], [], [], [], [], [], []]
        SolitaireBoard.current_move = NoMoveMove()
        SolitaireBoard.move_count = 0
        SolitaireBoard.move_history = []
        SolitaireBoard.state_history = []

        SolitaireBoard.create_deck()
        SolitaireBoard.shuffle_deck()

        # for c in SolitaireBoard.deck:
        #     print(c.testprintcard() + " ", end='')
        # print()

        for i in range(7):
            for j in range(i, 7):
                e = SolitaireBoard.deck.pop()
                SolitaireBoard.columns[j].append(e)
        SolitaireBoard.reveal_card()


        #count hidden cards in each column and return a number of hidden cards for each column
    def count_hiddencards():
        hiddencolumn = []
        # count hidden cards in each column and return a number of hidden cards for each column
        for col in SolitaireBoard.columns:
            hidden_cards = 0
            for card in col:
                if card.hidden:
                    hidden_cards += 1
                else:
                    break
            hiddencolumn.append(hidden_cards)
        return hiddencolumn
    # sort columns from most hidden cards to least hidden cards
    def sorted_hiddencolumn():
        temp_list = SolitaireBoard.count_hiddencards()
        index_list = []
        for i in range(7):
            index_list.append(i)
        return [x for _,x in sorted(zip(temp_list, index_list), reverse=True)]


    def identify_cards(cards):
        identified_deck, identified_waste, identified_foundations, identified_columns = cards
        if SolitaireBoard.waste and SolitaireBoard.waste[-1].hidden:
            SolitaireBoard.waste[-1].hidden = False
            if identified_waste[-1]: # <- supposed to be true
                SolitaireBoard.waste[-1].rank = identified_waste[-1].rank
                SolitaireBoard.waste[-1].suit = identified_waste[-1].suit
        col_index = 0
        for col in SolitaireBoard.columns:
            if col and col[-1].hidden:
                col[-1].hidden = False
                if identified_columns[col_index]: # <- supposed to be true
                    col[-1].rank = identified_columns[col_index][-1].rank
                    col[-1].suit = identified_columns[col_index][-1].suit
            col_index += 1

    def get_current_state():
        state_string = ""
        for c in SolitaireBoard.columns:
            if c:
                state_string += str(c[-1]) + " "
        for f in SolitaireBoard.foundations:
            if f:
                state_string += str(f[-1]) + " "
        if SolitaireBoard.waste:
            state_string += str(SolitaireBoard.waste[-1]) + " "
        state_string += str(SolitaireBoard.current_move)
        return state_string

    def execute_current_without_revealing():
        SolitaireBoard.state_history.append(SolitaireBoard.get_current_state())
        SolitaireBoard.current_move.execute_move()
        SolitaireBoard.move_history.append(SolitaireBoard.current_move)
        SolitaireBoard.move_count += 1

    def execute_current_move():
        SolitaireBoard.state_history.append(SolitaireBoard.get_current_state())
        SolitaireBoard.current_move.execute_move()
        SolitaireBoard.move_history.append(SolitaireBoard.current_move)
        SolitaireBoard.move_count += 1
        SolitaireBoard.reveal_card()

    def reveal_card():
        if SolitaireBoard.waste:
            SolitaireBoard.waste[-1].hidden = False
        for col in SolitaireBoard.columns:
            if col:
                col[-1].hidden = False

    def cards_need_identification():
        if SolitaireBoard.waste:
            if SolitaireBoard.waste[-1].hidden:
                return True
        for col in SolitaireBoard.columns:
            if col and col[-1].hidden:
                return True
        return False

    def is_game_over():
        return (len(SolitaireBoard.foundations[0]) == 13 and 
                len(SolitaireBoard.foundations[1]) == 13 and 
                len(SolitaireBoard.foundations[2]) == 13 and 
                len(SolitaireBoard.foundations[3]) == 13)


    def print_board(self):
        if len(self.deck) == 0:
            print("D:\t##")
        else:
            print("D:\t[]")
            # print("D" + ":\t", end='')
            # for card in self.deck:
            #     print(card.testprintcard() + " ", end='')
            # print()
        if len(self.waste) == 0:
            print("W:\t##")
        else:
            print("W" + ":\t", end='')
            for card in self.waste:
                print(card.testprintcard() + " ", end='')
            print()
        i = 0
        for f in self.foundations:
            print("F" + str(i+1) + ":\t[]") if len(f) == 0 else print("F" + str(i) + ":\t" + str(f[-1])) 
            i += 1
        i = 0
        for col in self.columns:
            if len(col) == 0:
                print("C" + str(i+1) + ":\t[]") 
            else:
                print("C" + str(i+1) + ":\t", end='')
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
        # Altid lav det træk der åbner for den største bunke med kort at vende.
        sorted_columns = SolitaireBoard.sorted_hiddencolumn()
        for i in sorted_columns:
            col = SolitaireBoard.columns[i]
            if col and col[0].hidden: # indeholder et skjult kort
                # Find det øverste synlige kort i kolonnen
                index = -1
                while col[index - 1].hidden == False:
                    index -= 1

                temp_card = col[index] #Card(rank=col[index].rank, suit=col[index].suit)

                # -> stod her før           

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
                            if talon_card.rank == 13: # find tom kolonne
                                temp_move = SolitaireBoard.make_way_for_the_king(SolitaireBoard.waste, -1)
                                if temp_move.move_type != MoveType.NOMOVE:
                                    SolitaireBoard.current_move = temp_move
                                    return
                            else:    
                                res = SolitaireBoard.look_for_column_destinatination(talon_card)
                                if res:
                                    SolitaireBoard.current_move = TalonToColMove(res)
                                    return
                        # Tjek om et kort fra foundation kan hjælpe med at frigøre
                        foundation = SolitaireBoard.look_for_foundation_destination2(temp_card)
                        if foundation:
                            foundation_card = foundation[-1]
                            if foundation_card.rank == 13:
                                temp_move = SolitaireBoard.make_way_for_the_king(SolitaireBoard.waste, -1)
                                if temp_move.move_type != MoveType.NOMOVE:
                                    SolitaireBoard.current_move = temp_move
                                    return
                            else:
                                res = SolitaireBoard.look_for_column_destinatination(foundation_card)
                                if res:
                                    SolitaireBoard.current_move = FoundationToColMove(foundation, res)
                                    return

                # Frigør ved at flytte et kort til foundation
                if index == -1: 
                    res = SolitaireBoard.look_for_foundation_destination(temp_card)
                    if res:
                        SolitaireBoard.current_move = ToFoundationMove(col, res)
                        return



    #[ ] Flyt kun fra kolonne til kolonne hvis det tillader at få vendt et kort eller at lave kolonnerne smooth.

    #[ ] Ryd ikke et spot med mindre der en konge der klar til at tage spottet.

    #[ ] Kun spil en konge hvis kolonnerne med den største bunke af kort der kan vendes
    #[ ] eller at spille en anden konge tillader at rykke at rykke fra en kolonne derpå ig vende et kort.

    #[✔] Kun byg videre på foundation fra 3+ hvis det ikke påvirke det næste kort beskyttelse 
    #[✔] eller at det et træk der tillader at lave et spil eller ryk frigør at vende et kort     
    #[?] ellers så skal det åbne muligheden for at overføre en bunke af samme farve mønster så der kan vendes et kort
    #[?] eller så frigøre et spot til en konge der venter.

    #[✔] Flyt eller ryk kun en 5'er-8'er hvis det tillader at vende et kort med det samme
    #[X] det er smooth med det næste kort I kolonnen
    #[?] der er ikke blevet rykket andre kort til den kolonnen
    # hvis der bare ikke er andre muligheder.

    # alle dine nødvendige kort ser ud til at være i bunkerne som skal vendes
    # flyt straks alle kort som kan op I foundation for måske at kunne åbne
    # for muligheden at lave et træk med et andet kort der allerede findes men er blokeret.

        # queue til træk der ikke vender et nyt kort 
        move_queue = Queue()

        # Flyt kort til foundation hvis de er next-card-protected
        for col in SolitaireBoard.columns:
            if col:
                res = SolitaireBoard.look_for_foundation_destination(col[-1])
                if res:
                    if SolitaireBoard.next_card_protected(col[-1]):
                        move_queue.put(ToFoundationMove(col, res))
        if SolitaireBoard.waste and (len(SolitaireBoard.waste) + len(SolitaireBoard.deck) > 2 or len(SolitaireBoard.deck) == 0):
            res = SolitaireBoard.look_for_foundation_destination(SolitaireBoard.waste[-1])
            if res:
                if SolitaireBoard.next_card_protected(SolitaireBoard.waste[-1]):
                    move_queue.put(ToFoundationMove(SolitaireBoard.waste, res))

        if SolitaireBoard.move_count > 100:
            # Tjek om et et kort fra talon kan flyttes fra talon ud på en kolonne
            if SolitaireBoard.waste and (len(SolitaireBoard.waste) + len(SolitaireBoard.deck) > 2 or len(SolitaireBoard.deck) == 0):
                temp_card = Card(rank=SolitaireBoard.waste[-1].rank, suit=SolitaireBoard.waste[-1].suit)
                if temp_card.rank < 5 or (temp_card.rank > 8 and temp_card.rank < 13):
                    
                    for col in SolitaireBoard.columns:
                        res = SolitaireBoard.look_for_column_destinatination(temp_card)
                        if res:
                            move_queue.put(TalonToColMove(res))

        # # Flyt kort til foundation hvis de er next-card-protected
        # for col in SolitaireBoard.columns:
        #     if col:
        #         res = SolitaireBoard.look_for_foundation_destination(col[-1])
        #         if res:
        #             if SolitaireBoard.next_card_protected(col[-1]):
        #                 SolitaireBoard.current_move = ToFoundationMove(col, res)
        #                 return
        # if SolitaireBoard.waste:
        #     res = SolitaireBoard.look_for_foundation_destination(SolitaireBoard.waste[-1])
        #     if res:
        #         if SolitaireBoard.next_card_protected(SolitaireBoard.waste[-1]):
        #             SolitaireBoard.current_move = ToFoundationMove(SolitaireBoard.waste, res)
        #             return

        # begynd at flytte kort til foundation
        # Flyt kort til foundation hvis selvom de ikke er next-card-protected
        if SolitaireBoard.move_count > 30:
            for col in SolitaireBoard.columns:
                if col:
                    res = SolitaireBoard.look_for_foundation_destination(col[-1])
                    if res:
                        move_queue.put(ToFoundationMove(col, res))
            if SolitaireBoard.waste and (len(SolitaireBoard.waste) + len(SolitaireBoard.deck) > 2 or len(SolitaireBoard.deck) == 0):
                res = SolitaireBoard.look_for_foundation_destination(SolitaireBoard.waste[-1])
                if res:
                    move_queue.put(ToFoundationMove(SolitaireBoard.waste, res))


        #start moving all ranks from talon to columns
        if SolitaireBoard.move_count > 50:
            if SolitaireBoard.waste and (len(SolitaireBoard.waste) + len(SolitaireBoard.deck) > 2 or len(SolitaireBoard.deck) == 0):
                temp_card = Card(rank=SolitaireBoard.waste[-1].rank, suit=SolitaireBoard.waste[-1].suit)     
                if temp_card.rank == 13: # find tom kolonne
                    temp_move = SolitaireBoard.make_way_for_the_king(SolitaireBoard.waste, -1)
                    if temp_move.move_type != MoveType.NOMOVE:
                        move_queue.put(temp_move)
                else:
                    for col in SolitaireBoard.columns:
                        res = SolitaireBoard.look_for_column_destinatination(temp_card)
                        if res:
                            move_queue.put(TalonToColMove(res))

        

        if SolitaireBoard.move_count > 200:
            # begynd at lægge kolonner sammen
            for col in SolitaireBoard.columns:
                if col and col[0].hidden: # indeholder et skjult kort
                    # Find det øverste synlige kort i kolonnen
                    index = -1
                    while col[index - 1].hidden == False:
                        index -= 1
                    if abs(index) == len(col):
                        pass
                    temp_card = col[index]
                    res = SolitaireBoard.look_for_column_destinatination(temp_card)
                    if res:
                        move_queue.put(ColToColMove(col, res, abs(index)))


        # ellers, vend et kort fra bunken
        if len(SolitaireBoard.deck) + len(SolitaireBoard.waste) > 2:
            move_queue.put(DeckMove())
        # 
        move_queue.put(NoMoveMove())


        SolitaireBoard.current_move = move_queue.get()
        # searching = True
        # while searching:
        #     if not SolitaireBoard.get_current_state() in SolitaireBoard.state_history:
        #         searching = False
        #     else:
        #         SolitaireBoard.current_move = move_queue.get()


    def next_card_protected(card: Card):
        if card.suit == "H":
            if SolitaireBoard.look_for_card_in_columns(Card(rank=card.rank, suit="D")):
                return True
            is_protected = True
            temp1 = False
            temp2 = False
            for f in SolitaireBoard.foundations:
                if f:
                    if f[-1].suit == "C":
                        temp1 = True
                        is_on_the_board = len(SolitaireBoard.look_for_card_in_columns(Card(rank=card.rank - 1, suit="C"))) > 0
                        is_protected = is_protected and ( f[-1].rank >= card.rank - 1 ) or is_on_the_board
                    if f[-1].suit == "S":
                        temp2 = True
                        is_on_the_board = len(SolitaireBoard.look_for_card_in_columns(Card(rank=card.rank - 1, suit="S"))) > 0
                        is_protected = is_protected and ( f[-1].rank >= card.rank - 1 ) or is_on_the_board
            return is_protected and temp1 and temp2
        elif card.suit == "D":
            if SolitaireBoard.look_for_card_in_columns(Card(rank=card.rank, suit="H")):
                return True
            is_protected = True
            temp1 = False
            temp2 = False
            for f in SolitaireBoard.foundations:
                if f:
                    if f[-1].suit == "C":
                        temp1 = True
                        is_on_the_board = len(SolitaireBoard.look_for_card_in_columns(Card(rank=card.rank - 1, suit="C"))) > 0
                        is_protected = is_protected and ( f[-1].rank >= card.rank - 1 ) or is_on_the_board
                    if f[-1].suit == "S":
                        temp2 = True
                        is_on_the_board = len(SolitaireBoard.look_for_card_in_columns(Card(rank=card.rank - 1, suit="S"))) > 0
                        is_protected = is_protected and ( f[-1].rank >= card.rank - 1 ) or is_on_the_board
            return is_protected and temp1 and temp2
        elif card.suit == "C":
            if SolitaireBoard.look_for_card_in_columns(Card(rank=card.rank, suit="S")):
                return True
            is_protected = True
            temp1 = False
            temp2 = False
            for f in SolitaireBoard.foundations:
                if f:
                    if f[-1].suit == "H":
                        temp1 = True
                        is_on_the_board = len(SolitaireBoard.look_for_card_in_columns(Card(rank=card.rank - 1, suit="H"))) > 0
                        is_protected = is_protected and ( f[-1].rank >= card.rank - 1 ) or is_on_the_board
                    if f[-1].suit == "D":
                        temp2 = True
                        is_on_the_board = len(SolitaireBoard.look_for_card_in_columns(Card(rank=card.rank - 1, suit="D"))) > 0
                        is_protected = is_protected and ( f[-1].rank >= card.rank - 1 ) or is_on_the_board
            return is_protected and temp1 and temp2
        elif card.suit == "S":
            if SolitaireBoard.look_for_card_in_columns(Card(rank=card.rank, suit="C")):
                return True
            is_protected = True 
            temp1 = False
            temp2 = False
            for f in SolitaireBoard.foundations:
                if f:
                    if f[-1].suit == "H":
                        temp1 = True
                        is_on_the_board = len(SolitaireBoard.look_for_card_in_columns(Card(rank=card.rank - 1, suit="H"))) > 0
                        is_protected = is_protected and ( f[-1].rank >= card.rank - 1 ) or is_on_the_board
                    if f[-1].suit == "D":
                        temp2 = True
                        is_on_the_board = len(SolitaireBoard.look_for_card_in_columns(Card(rank=card.rank - 1, suit="D"))) > 0
                        is_protected = is_protected and ( f[-1].rank >= card.rank - 1 ) or is_on_the_board
            return is_protected and temp1 and temp2



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

    def look_for_foundation_destination(card_to_move):
        for f in SolitaireBoard.foundations:
            if f:
                if f[-1].rank == card_to_move.rank - 1 and card_to_move.suit == f[-1].suit:
                    return f
        return []

    def look_for_foundation_destination2(card_to_move: Card):
        for f in SolitaireBoard.foundations:
            if f:
                if card_to_move.suit == "H" or card_to_move.suit == "D":
                    if f[-1].rank == card_to_move.rank + 1 and (f[-1].suit == "S" or f[-1].suit == "C"):
                        return f
                elif card_to_move.suit == "S" or card_to_move.suit == "C":
                    if f[-1].rank == card_to_move.rank + 1 and (f[-1].suit == "H" or f[-1].suit == "D"):
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

def simulate_games(n_games, move_limit):
    sum = 0
    for i in range(n_games):
        SolitaireBoard.new_game()

        while SolitaireBoard.move_count < move_limit:
            SolitaireBoard.new_suggest()
            SolitaireBoard.execute_current_move()
            if SolitaireBoard.current_move.move_type == MoveType.NOMOVE:
                break

            if SolitaireBoard.is_game_over():
                print("LØSNING FUNDET!")
                for m in SolitaireBoard.move_history:
                    print(str(m))
                sum += 1
                break
    return sum

if __name__ == "__main__":
    # GAMEMODE:
    # 1: simuler mange spil
    # 2: step-by-step gennem et spil
    # 3: step-by-step gennem en bestemt sortering
    GAMEMODE = 1 
    
    if GAMEMODE == 1:
        NGAMES = 100
        MOVELIMIT = 500
        print("Simulating " + str(NGAMES) + " solitaires")
        result = simulate_games(NGAMES, MOVELIMIT)
        print(str(result) + " of " + str(NGAMES) + " were solved.")
    elif GAMEMODE == 2:
        board = SolitaireBoard()
        SolitaireBoard.create_deck()
        SolitaireBoard.shuffle_deck()
        SolitaireBoard.new_game()
        print("Game is in auto solve mode..")
        print("Enter any input to continue")
        user_input = input()

        k = 0
        while True:
            SolitaireBoard.new_suggest()
            print(SolitaireBoard.current_move)
            SolitaireBoard.execute_current_move()
            print("Move number: " + str(SolitaireBoard.move_count))
            board.print_board()

            k += 1
            MOVESPERINPUT = 10
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

                print("Printing move_history ...")

                for m in SolitaireBoard.move_history:
                    print(str(m))
                break                

            if SolitaireBoard.move_count > 500 or SolitaireBoard.current_move.move_type == MoveType.NOMOVE:
                print("@@@@@@@@@@@@@@@@@@@@@@@@@@")
                print("Q_Q Q_Q Q_Q Q_Q Q_Q Q_Q")
                print("KUNNE IKKE FINDE EN LØSNING")
                print("Q_Q Q_Q Q_Q Q_Q Q_Q Q_Q")
                print("@@@@@@@@@@@@@@@@@@@@@@@@@@")
                break
    elif GAMEMODE == 3:
        board = SolitaireBoard()
        SolitaireBoard.new_game_from_string("3C 2C 8C KH AD QH QC 6C 3S 3H 9S KS QS AS 6H TS 5S AC 8S 9C 5C JD QD 4C 4H 2S 8D 9D KC 7C 8H 4D AH TH JC JH 3D 7D 9H 7S 6D KD 4S JS TC 5D 2H 6S 7H TD 2D 5H")
        print("Game is in auto solve mode..")
        print("Enter any input to continue")
        user_input = input()

        k = 0
        while True:
            SolitaireBoard.new_suggest()
            print(SolitaireBoard.current_move)
            SolitaireBoard.execute_current_move()
            print("Move number: " + str(SolitaireBoard.move_count))
            board.print_board()

            k += 1
            MOVESPERINPUT = 20
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

                print("Printing move_history ...")

                for m in SolitaireBoard.move_history:
                    print(str(m))
                break                

            if SolitaireBoard.move_count > 500 or SolitaireBoard.current_move.move_type == MoveType.NOMOVE:
                print("@@@@@@@@@@@@@@@@@@@@@@@@@@")
                print("Q_Q Q_Q Q_Q Q_Q Q_Q Q_Q")
                print("KUNNE IKKE FINDE EN LØSNING")
                print("Q_Q Q_Q Q_Q Q_Q Q_Q Q_Q")
                print("@@@@@@@@@@@@@@@@@@@@@@@@@@")