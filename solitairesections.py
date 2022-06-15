import cv2
from cv2 import boxPoints
import imutils
import numpy as np

from carddetection import Query_card


def is_point_in_rect(point, rect):

    px, py = point
    r0x, r0y = rect[0] # top left corner of the rectangle
    r1x, r1y = rect[1] # bottom right corner of the rectangle
    return px >= r0x and px <= r1x and py >= r0y and py <= r1y

def distribute_to_board_sections(detected_cards, section_rects):
    # rects for the different board sections where cards can be placed
    deck_rect, waste_rect, foundation_rects, col_rects = section_rects

    # Distribute cards to a number of lists corresponding to the different columns, foundations, etc. of the game
    main_columns = [[], [], [], [], [], [], []]
    foundations = [[], [], [], []]
    deck = []
    waste = []

    for card in detected_cards:
        if is_point_in_rect(card.center, deck_rect):
            deck.append(card)
        if is_point_in_rect(card.center, waste_rect):
            waste.append(card)
            continue

        found = False # just used to end the loop a bit earlier
        for idx, f in enumerate(foundation_rects):
            if is_point_in_rect(card.center, f):
                foundations[idx].append(card)
                found = True
                break
        if found:
            continue
        for idx, col_rect in enumerate(col_rects):
            if is_point_in_rect(card.center, col_rect):
                main_columns[idx].append(card)
                break
    return [deck, waste, foundations, main_columns]

def draw_detected_contours(image, cards):
    #Draw the contours
    for rect in cards:
        box = np.int0(cv2.boxPoints(rect))
        cv2.drawContours(image, [box], -1, (0, 255, 0), 1)
    return image

def draw_board_section_rects(img, section_rects):
    deck_rect, waste_rect, foundation_rects, col_rects = section_rects
    cv2.rectangle(img, deck_rect[0], deck_rect[1], (0,0,255), 2)
    cv2.rectangle(img,waste_rect[0], waste_rect[1], (0,0,255), 2)
    cv2.rectangle(img,foundation_rects[0][0], foundation_rects[0][1], (0,0,255), 2)
    cv2.rectangle(img,foundation_rects[1][0], foundation_rects[1][1], (0,0,255), 2)
    cv2.rectangle(img,foundation_rects[2][0], foundation_rects[2][1], (0,0,255), 2)
    cv2.rectangle(img,foundation_rects[3][0], foundation_rects[3][1], (0,0,255), 2)
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    k = 1
    for c in col_rects:
        cv2.rectangle(img,c[0], c[1], (0,0,255), 2)
        text_center = (np.int64((c[0][0] + c[1][0])/2),np.int64((c[0][1] + c[1][1])/2))
        cv2.putText(img,"c" + str(k),text_center,font,1,(0,0,0),3,cv2.LINE_AA)
        k += 1
    return img

def get_sections(image):
    height, width, _ = image.shape
    y_div = np.int0(height * 0.3)

    deck_rect = [(0, 0), (np.int0(width*0.2), y_div)]
    waste_rect = [(np.int0(width*0.2), 0), (np.int0(width*0.4), y_div)]
    foundation_rects = [ [(np.int0(width*0.4), 0), (np.int0(width*0.55), y_div)], 
                        [(np.int0(width*0.55), 0), (np.int0(width*0.70), y_div)],
                        [(np.int0(width*0.70), 0), (np.int0(width*0.85), y_div)],
                        [(np.int0(width*0.85), 0), (np.int0(width*1.00), y_div)]]
    col_rects = []
    for i in range(7):
        c_rect = [(np.int0(width/7 * i), y_div), (np.int0(width/7 * (i + 1)), height)]
        col_rects.append(c_rect)
    board_section_rects = [deck_rect, waste_rect, foundation_rects, col_rects]
    return board_section_rects

def draw_sections_on_image(image):
    sections = get_sections(image)
    image = draw_board_section_rects(image, sections)
    return image

def print_cards_in_sections(solitaire_board):
    deck, waste, foundations, cols = solitaire_board
    print("Deck:")
    for card in deck:
        print(card.best_card_name + " ", end='')
    print("Waste:")
    for card in waste:
        print(card.best_card_name + " ", end='')
    i = 1
    for f in foundations:
        print("F" + str(i) + ":")
        for card in f:
           print(card.best_card_name + " ", end='')
        print()
        i += 1
    i = 1
    for c in cols:
        print("C" + str(i) + ":")
        for card in c:
           print(card.best_card_name + " ", end='')
        print()
        i += 1

  

def place_cards(image, cards):
    sections = get_sections(image)
    current_board = distribute_to_board_sections(cards, sections)
    return current_board



# - - - - - - 
# - - - - - - 

