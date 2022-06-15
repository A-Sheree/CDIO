from glob import glob
import sys
from turtle import width
from pyparsing import hexnums
import carddetection
import solitairesections
import requests
import cv2
import numpy as np
import imutils
import os
import sys
from tkinter import *
from PIL import Image
from solitairegamelogic import SolitaireBoard, Card
from io import StringIO
import time

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


# - - - Button functions - - - 

def connect_to_camera():
    global video
    global camera_connected
    video = cv2.VideoCapture(ipcam_entry.get())
    
    if video.isOpened():
        ipcam_indicator.itemconfig(ipcam_indicator_oval, fill="green")
        camera_connected = True
    else:
        ipcam_indicator.itemconfig(ipcam_indicator_oval, fill="red")
        camera_connected = False

def view_stream():
    if not camera_connected:
        print("Camera is not connected")
        return
    else:
        while True:
            ret, frame = video.read()
            
            cv2.imshow('Press q to close the window', solitairesections.draw_sections_on_image(frame))
            key = cv2.waitKey(1)
            if key == ord('q'):
                cv2.destroyAllWindows()
                break

def show_current_frame():
    cv2.imshow('press any key to close the window', current_frame)
    cv2.waitKey()
    cv2.destroyAllWindows()

def take_picture():
    if not camera_connected:
        print("Camera is not connected")
        return
    else:
        # read from stream for 2 seconds
        t_end = time.time() + 2
        while time.time() < t_end:
            video.read()

        global current_frame
        global current_frame_clean
        global cards
        current_frame = video.read()[1]
        current_frame_clean = current_frame.copy()
        #cv2.imwrite(filename='testimg.jpg', img=current_frame)

        # - - Detect cards in the frame - -
        current_frame, cards = carddetection.processing(current_frame)

        # - - Place detected cards into columns - - 
        global cards_in_sections
        cards_in_sections = solitairesections.place_cards(current_frame, cards)
        cards_in_sections = card_adapter(cards_in_sections)        

def fix_card():
    fix_input = fix_entry.get()
    if not len(fix_input) == 5:
        return

    fix_input = fix_input.split()
    wrong_name = fix_input[0]
    correct_name = fix_input[1]
    
    #find card in list and fix its name
    for c in cards:
        if c.best_card_name == wrong_name:
            c.best_card_name = correct_name
            break

    #Redraw the names on the frame
    global current_frame
    current_frame = current_frame_clean.copy()
    for c in cards:
        carddetection.draw_results(current_frame, c)

    fix_entry.delete(0, "end")


# - - Initialize - - 
camera_connected = False
video = None #
cards = []
current_frame = None
current_frame_clean = None
board = SolitaireBoard()
cards_in_sections = []
testimg1 = cv2.imread("Cards1.JPG")
testimg2 = cv2.imread("Cards2.JPG")
root = Tk()

# - - UI WIDGETS

ipcam_label = Label(root, text="IP Webcam address:")
ipcam_indicator = Canvas(root, width=20, height=20)
ipcam_indicator_oval = ipcam_indicator.create_oval(2,2,18,18, fill="grey")

ipcam_entry = Entry(root, width=45, borderwidth=5)
ipcam_entry.insert(INSERT, "http://192.168.0.102:8080/video")

ipcam_btn = Button(root, text="Connect", command=connect_to_camera, bg='blue', fg='white')
ipcam_label.grid(row=0, column=0, padx=5, pady=5, columnspan=2)
ipcam_indicator.grid(row=0, column=2, padx=5, pady=5)
ipcam_entry.grid(row=1, column=0, padx=5, pady=5, columnspan=3)
ipcam_btn.grid(row=1, column=3, padx=5, pady=5)

btn_take_pic = Button(root, text="Take picture", command=take_picture, width=10, height=5, bg='blue', fg='white')
btn_take_pic.grid(row=2, column=0, padx=5, pady=5)

btn_view_stream = Button(root, text="View stream", command=view_stream, width=10, height=5, bg='blue', fg='white')
btn_view_stream.grid(row=2, column=1, padx=5, pady=5)

btn_show_current_frame = Button(root, text="Show current frame", command=show_current_frame, width=10, height=5, bg='blue', fg='white')
btn_show_current_frame.grid(row=2, column=2, padx=5, pady=5)

btn_test2 = Button(root, text="Test", width=10, height=5, bg='blue', fg='white')
btn_test2.grid(row=2, column=3, padx=5, pady=5)
btn_test3 = Button(root, text="Test", width=10, height=5, bg='blue', fg='white')
btn_test3.grid(row=3, column=0, padx=5, pady=5)
btn_test4 = Button(root, text="Test", width=10, height=5, bg='blue', fg='white')
btn_test4.grid(row=3, column=1, padx=5, pady=5)
btn_test5 = Button(root, text="Test", width=10, height=5, bg='blue', fg='white')
btn_test5.grid(row=3, column=2, padx=5, pady=5)
btn_test6 = Button(root, text="Test", width=10, height=5, bg='blue', fg='white')
btn_test6.grid(row=3, column=3, padx=5, pady=5)

output_label = Label(root, text="Output box")
output_label.grid(row=4, column=0, padx=5, pady=5, columnspan=2)

output_box = Text(root, height=15, width=35)
output_box.grid(row=5, column=0, padx=5, pady=5, columnspan=3)

fix_label = Label(root, text="Correction input")
fix_label.grid(row=6, column=0, padx=5, pady=5, columnspan=2)

fix_entry = Entry(root, width=45, borderwidth=5)
fix_entry.grid(row=7, column=0, padx=5, pady=5, columnspan=3)


fix_btn = Button(root, text="Fix card", command=fix_card, bg='blue', fg='white', width=10)
fix_btn.grid(row=7, column=3, padx=5, pady=5)


# tekstboks1 = Text(root, width=60, height=15)
# tekstboks1.grid(row=0, column=3, padx=5, pady=5)

# my_canvas = tk.Canvas(root, width=200, height=200)  # Create 200x200 Canvas widget
# my_canvas.pack()

# my_oval = my_canvas.create_oval(50, 50, 100, 100)  # Create a circle on the Canvas
# - - - - -  - - - 

root.mainloop()



# button_1 = Button(root, text="Video", command=stream, width=10, height=5, bg='blue', fg='white')
# button_1.grid(column=0, row=0, padx=5, pady=5)
# button_2 = Button(root, text="Next Move", command=nextMove, width=10, height=5, bg='blue', fg='white')
# button_2.grid(column=1, row=0, padx=5, pady=5)
# button_3 = Button(root, text="Show pic", command=showProcessedPic, width=10, height=5, bg='blue', fg='white')
# button_3.grid(column=0, row=1, padx=5, pady=5)
# button_4 = Button(root, text="Exit program", command=exitProgram, width=10, height=5, bg='blue', fg='white')
# button_4.grid(column=2, row=1, padx=5, pady=5)
# button_5 = Button(root, text="Change deck", command=changeDeck, width=10, height=5, bg='blue', fg='white')
# button_5.grid(column=2, row=0, padx=5, pady=5)
# button_6 = Button(root, text="Show deck", command=showDeck, width=10, height=5, bg='blue', fg='white')
# button_6.grid(column=1, row=1, padx=5, pady=5)
# button_7 = Button(root, text="Take Picture", command=takePicture, width=10, height=5, bg='blue', fg='white')
# button_7.grid(column=0, row=2, padx=5, pady=5)

# tekstboks1 = Text(root, width=60, height=15)
# tekstboks1.grid(row=0, column=3, padx=5, pady=5)
# tekstboks2 = Text(root, width=60, height=15)
# tekstboks2.grid(row=1, column=3, padx=5, pady=5)

# label1 = Label(root, text="Label text")
# label1.grid(row=3, column=0, columnspan=3)









# def stream():
#     while True:
#         ret, frame = video.read()
#         cv2.imshow('s = save photo                               q = exit/return to controls', frame)
#         key = cv2.waitKey(1)
#         if key == ord('s'):
#             img_resized = cv2.imwrite(filename='saved_img.jpg', img=frame)
#             print("Image saved!")
#             # METHOD IMAGE PROCESSING HERE...
#             print("Image processed")
            
#             #TEST
#             cv2.imshow('imagetest', img_resized)

#             #Image.open("saved_img.jpg").show()
#         if key == ord('q'):
#             cv2.destroyAllWindows()
#             break


# def restart():
#     os.execl(sys.executable, sys.executable, *sys.argv)


# def exitProgram():
#     print("Program ends...")
#     sys.exit()


# def nextMove():
#     ret, frame = video.read()
#     cv2.imwrite(filename='testimg.jpg', img=frame)

#     print("Next move...")


# def takePicture():
#     t_end = time.time() + 2
#     while time.time() < t_end:
#         # do whatever you do
#         ret, frame = video.read()

#     global current_frame
#     current_frame = video.read()[1]
#     cv2.imwrite(filename='testimg.jpg', img=current_frame)

# def showProcessedPic():
#     global current_frame

#     cv2.imshow('press any key to close the window', current_frame)
#     cv2.waitKey()
#     cv2.destroyAllWindows()
#     #Image.open("testimg.jpg").show()

 

# def changeDeck():
#     # outout redirection
#     # - - -
#     old_stdout = sys.stdout  
#     result = StringIO()
#     sys.stdout = result
#     board.print_board()
#     result_string = result.getvalue()

#     sys.stdout = old_stdout
#     # - - -

#     tekstboks1.delete("1.0", "end")
#     tekstboks1.insert(INSERT,result_string)

#     #x = input("Command: ")
#     #print("You entered: " + x)
#     #print("Deck changed...")
    

# def showDeck():
#     #print("Card deck...")
    
#     tekstboks1.delete("1.0", "end")
#     tekstboks1.insert(INSERT,str(TEST))
