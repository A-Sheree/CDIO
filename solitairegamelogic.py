import random
import string

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

class SolitaireBoard():
    deck = []
    waste = []
    foundations = [[], [], [], []]
    columns = [[], [], [], [], [], [], []]

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
    def load_with_cards(self, cards):
        if len(cards) == 4:
            self.append_to_deck(cards[0])
            self.append_to_waste(cards[1])
            self.append_to_foundations(cards[2])
            self.append_to_columns(cards[3])


    def create_deck(self):
        self.deck = []
        for x in range(1, 14, 1):
            self.deck.append(Card(x, 'D'))
            self.deck.append(Card(x, 'C'))
            self.deck.append(Card(x, 'H'))
            self.deck.append(Card(x, 'S'))

    def shuffle_deck(self):
        random.shuffle(self.deck)
        return

    def new_game(self):
        self.deck = []
        self.columns = [[], [], [], [], [], [], []]
        self.foundations = [[], [], [], []]
        self.waste = []
        self.create_deck()
        self.shuffle_deck()
        for i in range(7):
            for j in range(i+1):
                e = self.deck.pop()
                self.columns[i].append(e)
            self.columns[i][-1].hidden = False

    def draw_from_deck(self):
        if len(self.deck) > 0:
            card = self.deck.pop()
            card.hidden = False
            self.waste.append(card)
        elif len(self.deck) == 0 and len(self.waste)  > 0:
            self.deck = self.waste[:]
            self.deck.reverse()
            self.waste = []
            for c in self.deck:
                c.hidden = True 

    def valid_to_col_move(self, card, dest_column):
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

    def move_to_col(self, from_column, to_column, number_of_cards):
        if len(from_column) == 0 or number_of_cards < 0 or from_column == to_column or number_of_cards > len(from_column):
            return
        from_card = from_column[-number_of_cards]
        if from_card.hidden:
            return
        if self.valid_to_col_move(from_card, to_column):
            if number_of_cards == 0:
                to_column.extend(to_column)
                from_column[:] = []
            else:
                to_column.extend(from_column[-number_of_cards : ])
                from_column[:] = from_column[ : -number_of_cards]
                if len(from_column) > 0:
                    from_column[-1].hidden = False

    def valid_to_foundation_move(self, card, dest_foundation):
        if len(dest_foundation) == 0:
            return card.rank == 1
        else:
            dest_card = dest_foundation[-1]
            return card.suit == dest_card.suit and card.rank == dest_card.rank + 1

    def move_to_foundation(self, column, foundation):
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


# - Led efter næste kort til en foundation
#   - Hvis det er fri, flyt til foundation
#   - Ellers, rekursivt se om det kan frigøres (max dybde fx 3)
# - Forsøg at vende et kort fra en kolonne (rekursivt på samme måde)
# - Vend et kort fra bunken
    def suggest_move(self):
        # - Tjek om næste kort til en foundation ligger frit
        for f in self.foundations:
            if len(f) == 0:
                res = self.look_for_ace()
                if len(res) > 0:
                    return "MOVE " + str(res[-1]) + " TO A FOUNDATION"
            else:
                temp_card = Card(f[-1].rank + 1, f[-1].suit)
                res = self.look_for_card(temp_card)
                if len(res) > 0:
                    return "MOVE " + str(res[-1]) + " TO A FOUNDATION"

        # ellers, tjek om næste kort til en foundation kan frigøres

        # ellers, tjek om der kan vendes et skjult kort fra en kolonne

        # ellers, tjek om et skjult kort kan frigøres

        # ellers, vend et kort fra bunken
        return "TURN A CARD FROM THE DECK"

    def look_for_ace(self):
        # check waste
        if len(self.waste) > 0 and self.waste[-1].rank == 1:
                return self.waste
        for col in self.columns:
            if len(col) > 0 and col[-1].rank == 1:
                return col
        return []
        
    def look_for_card(self, card):
        if len(self.waste) > 0 and self.waste[-1].rank == card.rank and self.waste[-1].suit == card.suit:
                return self.waste
        for col in self.columns:
            if len(col) > 0 and col[-1].rank == card.rank and col[-1].suit == card.suit:
                return col
        return []

# -----------------