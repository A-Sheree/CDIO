from itertools import count
import cv2
from cv2 import VideoCapture
from cv2 import waitKey
import imutils
import numpy as np
import os


class Query_card:
    """Structure to store information about query cards in the camera image."""

    def __init__(self):
        self.contour = [] # Contour of card
        self.width, self.height = 0, 0 # Width and height of card
        self.corner_pts = [] # Corner points of card
        self.center = [] # Center point of card
        self.warp = [] # 200x300, flattened, grayed, blurred image
        self.best_diff = 0
        self.thresh = []
        self.best_card_name = ""

class Trainingcard:
    """Structure to store information about train rank images."""

    def __init__(self):
        self.img = [] # Thresholded, sized rank image loaded from hard drive
        self.name = "Placeholder"

def load_trainingcard(filepath):
    """Loads suit images from directory specified by filepath. Stores
    them in a list of Train_suits objects."""

    trainingcards = []
    i = 0
                                                      
    for Cards in ['AC','AS','AH','AD','2C','2S','2H','2D','3C','3S','3H','3D','4C','4S','4H','4D','5C','5S',
                 '5H', '5D','6C','6S','6H','6D','7C','7S','7H','7D','8C','8S','8H','8D','9C','9S','9H','9D',
                 'TC','TS','TH','TD','JC','JS','JH','JD','QC','QS','QH','QD','KC','KS','KH','KD']:
                
        trainingcards.append(Trainingcard())
        trainingcards[i].name = Cards
        filename = Cards + '.jpg'
        trainingcards[i].img = cv2.imread(filepath+filename,0)
        i = i + 1

    return trainingcards

def flattener(image, pts, w, h):
    """Flattens an image of a card into a top-down 200x300 perspective.
    Returns the flattened, re-sized, grayed image.
    See www.pyimagesearch.com/2014/08/25/4-point-opencv-getperspective-transform-example/"""
    temp_rect = np.zeros((4,2), dtype = "float32")
    
    s = np.sum(pts, axis = 2)

    tl = pts[np.argmin(s)]
    br = pts[np.argmax(s)]

    diff = np.diff(pts, axis = -1)
    tr = pts[np.argmin(diff)]
    bl = pts[np.argmax(diff)]

    # Need to create an array listing points in order of
    # [top left, top right, bottom right, bottom left]
    # before doing the perspective transform

    if w <= 0.8*h: # If card is vertically oriented
        temp_rect[0] = tl
        temp_rect[1] = tr
        temp_rect[2] = br
        temp_rect[3] = bl

    if w >= 1.2*h: # If card is horizontally oriented
        temp_rect[0] = bl
        temp_rect[1] = tl
        temp_rect[2] = tr
        temp_rect[3] = br

    # If the card is 'diamond' oriented, a different algorithm
    # has to be used to identify which point is top left, top right
    # bottom left, and bottom right.
    
    if w > 0.8*h and w < 1.2*h: #If card is diamond oriented
        # If furthest left point is higher than furthest right point,
        # card is tilted to the left.
        if pts[1][0][1] <= pts[3][0][1]:
            # If card is titled to the left, approxPolyDP returns points
            # in this order: top right, top left, bottom left, bottom right
            temp_rect[0] = pts[1][0] # Top left
            temp_rect[1] = pts[0][0] # Top right
            temp_rect[2] = pts[3][0] # Bottom right
            temp_rect[3] = pts[2][0] # Bottom left

        # If furthest left point is lower than furthest right point,
        # card is tilted to the right
        if pts[1][0][1] > pts[3][0][1]:
            # If card is titled to the right, approxPolyDP returns points
            # in this order: top left, bottom left, bottom right, top right
            temp_rect[0] = pts[0][0] # Top left
            temp_rect[1] = pts[3][0] # Top right
            temp_rect[2] = pts[2][0] # Bottom right
            temp_rect[3] = pts[1][0] # Bottom left
            

    maxWidth = 200
    maxHeight = 300

    # Create destination array, calculate perspective transform matrix,
    # and warp card image
    dst = np.array([[0,0],[maxWidth-1,0],[maxWidth-1,maxHeight-1],[0, maxHeight-1]], np.float32)
    M = cv2.getPerspectiveTransform(temp_rect,dst)
    warp = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
    warp = cv2.cvtColor(warp,cv2.COLOR_BGR2GRAY)

    return warp

def imagefilter (frame):
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)
    retval, thresh = cv2.threshold(blur,100,255,cv2.THRESH_BINARY)

    return thresh

def getcontours (dilate):
    contours = cv2.findContours(dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)

    return sorted(contours, key=cv2.contourArea, reverse=True)

def find_cards (contours):
    if len(contours) < 1:
        return []
    first_rect = cv2.minAreaRect(contours[0])
    area = first_rect[1][0] * first_rect[1][1]
    area_lower = area * 0.8
    area_upper = area * 1.2

    cards = []
    count = -1
    for c in contours[:]:
        ((x, y), (w, h),a) = rect = cv2.minAreaRect(c)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        if (area_lower < h*w < area_upper): #if (h > 0 and w > 0):
            ar = w / float(h) if w > h > 0 else h / float(w) 
            if (1.43 <= ar <= 1.58):
                count += 1
                    #make new list with drawn contours
                cards.append(contours[count])
    return cards

def preprocess_card (contour, image ):

    qCard =Query_card()

    qCard.contour = contour

    peri = cv2.arcLength(contour,True)
    approx = cv2.approxPolyDP(contour,0.01*peri,True)
    pts = np.float32(approx)
    qCard.corner_pts = pts

    x,y,w,h = cv2.boundingRect(contour)
    qCard.width, qCard.height = w, h
    
    average = np.sum(pts, axis=0)/len(pts)
    cent_x = int(average[0][0])
    cent_y = int(average[0][1])
    qCard.center = [cent_x, cent_y]

    qCard.warp = flattener(image, pts, w, h)
    blur = cv2.GaussianBlur(qCard.warp,(5,5),2 )
    thresh = cv2.adaptiveThreshold(blur,255,1,1,11,1)
   # thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,51,10)
    blur_thresh = cv2.GaussianBlur(thresh,(5,5),5)
    qCard.thresh = blur_thresh

    return qCard

def match_card(qCard, trainingcards):
    best_name = ""
    best_diff = 250000
    
    i = 0

    if (len(qCard.thresh) != 0):
        
        # Difference the query card rank image from each of the train rank images,
        # and store the result with the least difference
        for CMatch in trainingcards:
            diff_img = cv2.absdiff(qCard.thresh, CMatch.img)
            diff_img = cv2.GaussianBlur(diff_img,(5,5),5)
            flag, diff_img = cv2.threshold(diff_img, 200, 255, cv2.THRESH_BINARY) 
            card_diff = np.sum(diff_img)
            if card_diff < best_diff:
                best_diff = card_diff
                best_name = CMatch.name
    # Return the identiy of the card and the quality of the suit and rank match
    return best_name, best_diff

def draw_results(image, qCard):

    x = qCard.center[0]
    y = qCard.center[1]
    cv2.circle(image,(x,y),5,(255,0,0),-1)

    card_name = qCard.best_card_name

    # Draw card name twice, so letters have black outline
    cv2.putText(image,(card_name),(x-60,y-10),font,1,(0,0,0),3,cv2.LINE_AA)
    cv2.putText(image,(card_name),(x-60,y-10),font,1,(50,200,200),2,cv2.LINE_AA)
    return image

def processing (frame):
    image = frame.copy()
    dilate = imagefilter(frame)
    contours = getcontours(dilate)
    cnts = find_cards(contours)
    if len(cnts) != 0:

        cards = []
        k = 0
        #For each contour detected
        for i in range(len(cnts)):
            cards.append(preprocess_card(cnts[i],image))

            cards[k].best_card_name,cards[k].best_diff, = match_card(cards[k],trainingcards)
            #print(cards[k].best_card_name)
            #print(cards[k].best_diff)
            #cv2.imshow("Image2-{}".format(cards[k].best_diff), cards[k].thresh)
            
            image = draw_results(image, cards[k])
            
            k = k + 1

    return image, cards


# M_WIDTH = 1280
# IM_HEIGHT = 720

# RANK_WIDTH = 70
# RANK_HEIGHT = 125

# CORNER_WIDTH = 32
# CORNER_HEIGHT = 84

# SUIT_WIDTH = 70
# SUIT_HEIGHT = 100

# RANK_DIFF_MAX = 250000
# SUIT_DIFF_MAX = 700

# CARD_MAX_AREA = 120000
# CARD_MIN_AREA = 25000

font = cv2.FONT_HERSHEY_SIMPLEX
path = os.path.dirname(os.path.abspath(__file__))
trainingcards = load_trainingcard( path + '/Card_Imgs/')

if __name__ == "__main__":
    img = cv2.imread("Cards1.JPG")
    img, cards = processing(img)
    cv2.imshow('image', img)
    waitKey(0)

#vid = cv2.VideoCapture(0)
    
#while (True):
    #isTrue, img = vid.read()
   # cv2.imshow('image', processing(image))

  #  if cv2.waitKey(1) & 0xFF == ord('q'):
 #       break

#vid.release()

#cv2.destroyAllWindows()
