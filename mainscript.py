import string
import cv2
from solitairegamelogic import SolitaireBoard, Card
import carddetection
import solitairesections
from threading import Thread

def card_adapter(detection_cards):
    deck, waste, foundations, columns = detection_cards
    game_logic_deck = []
    game_logic_waste = []
    game_logic_foundations = []
    game_logic_columns = []

    for c in deck:
        if len(c.best_card_name) == 2:
            temp = Card()
            temp.hidden = False
            temp.rank = Card.rank_str_to_int(c.best_card_name[0])
            temp.suit = c.best_card_name[1]
            game_logic_deck.append(temp)
    
    for c in waste:
        if len(c.best_card_name) == 2:
            temp = Card()
            temp.hidden = False
            temp.rank = Card.rank_str_to_int(c.best_card_name[0])
            temp.suit = c.best_card_name[1]
            game_logic_waste.append(temp)

    for foundation in foundations:
        temp_list = []
        for c in foundation:
            if len(c.best_card_name) == 2:
                temp = Card()
                temp.hidden = False
                temp.rank = Card.rank_str_to_int(c.best_card_name[0])
                temp.suit = c.best_card_name[1]
                temp_list.append(temp)
        game_logic_foundations.append(temp_list)

    for column in columns:
        temp_list = []
        for c in column:
            if len(c.best_card_name) == 2:
                temp = Card()
                temp.hidden = False
                temp.rank = Card.rank_str_to_int(c.best_card_name[0])
                temp.suit = c.best_card_name[1]
                temp_list.append(temp)
        game_logic_columns.append(temp_list)

    logic_cards = [game_logic_deck, game_logic_waste, game_logic_foundations,game_logic_columns]
    return logic_cards

def fix_card(wrong_name, correct_name, cards):
    #find card in list and fix its name
    for c in cards:
        if c.best_card_name == wrong_name:
            c.best_card_name = correct_name
            break


testimg1 = cv2.imread("Cards1.JPG")
testimg2 = cv2.imread("Cards2.JPG")


if __name__ == "__main__":
    vid = cv2.VideoCapture(0)
    cv2.imshow('image', testimg2)

    game_state = SolitaireBoard()
    
    while (True):
        # - -  Get a frame from the video feed - -
        isTrue, img = vid.read()
        img = testimg1.copy()
        original_img = img

        # - - Detect cards in the frame - -
        img, cards = carddetection.processing(img)
        
        # - - Place detected cards into columns - - 
        cards_in_sections = solitairesections.place_cards(img, cards)
        cards_in_sections = card_adapter(cards_in_sections)

        print("If cards are detected correctly: Press Y to get move suggestion. If cards are detected incorrectly: Press N to correct cards")
        cv2.imshow('image', img)

        pressed_key = cv2.waitKey(-1)
        if pressed_key & 0xFF == ord('q'):
            break
        elif pressed_key & 0xFF == ord('n'):
            cv2.destroyWindow('image')

            ### - - - INPUT FOR FIXING CARDS - - -

            print("Enter the number of cards you are fixing: ")
            n_cards = int(input())
            for i in range(n_cards):
                print("Enter name of the incorrect card followed by name of the correct card: eg. KH KD")
                console_input = input()
                entered_correction = console_input.split()

                fix_card(entered_correction[0], entered_correction[1], cards)
            img = original_img
            for c in cards:
                carddetection.draw_results(img, c)

            #img = solitairesections.draw_sections_on_image(img)
            cv2.imshow('image', img)
            print("Press Y for move suggestion")
            pressed_key = cv2.waitKey(-1)

        if pressed_key & 0xFF == ord('y'):
            # - - Send the cards to the game logic - - 
            SolitaireBoard.identify_cards(cards_in_sections)
            #game_state.load_with_cards(cards_in_sections)

            # - - print the current board state - - 
            game_state.print_board()

            #game_state.getsuggestedmove()
            print("Draw a card from the deck")
            print("*************************")
            print()

        
        print("Press any key to take a new picture")
        cv2.waitKey(-1)
        
        
            

print("OUT OF LOOP")

vid.release()




