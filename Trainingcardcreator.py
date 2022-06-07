from typing import final
import cv2
import imutils
import numpy as np
import os
img_path = os.path.dirname(os.path.abspath(__file__)) + '/Card_Imgs/'
i = 15
M_WIDTH = 1280
IM_HEIGHT = 720

RANK_WIDTH = 70
RANK_HEIGHT = 125

SUIT_WIDTH = 70
SUIT_HEIGHT = 100
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

#basic image filtering
def imagefilter (frame):
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)
    retval, thresh = cv2.threshold(blur,100,255,cv2.THRESH_BINARY)

    return thresh
#finding the contours on the image
def getcontours (dilate):
    contours = cv2.findContours(dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)

    return sorted(contours, key=cv2.contourArea, reverse=True)
#mainscript, first take a copy of a given frame then process it with filter/contours then crop it filter more and save image.
def processing (frame):
    image = frame.copy()
    dilate = imagefilter(frame)
    contours = getcontours(dilate)
    count = -1
    #Check contours to see if they match dimensions of a card
    for c in contours[:]:
        ((x, y), (w, h),a) = rect = cv2.minAreaRect(c)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        if (h > 0 and w > 0):
            ar = w / float(h) if w > h > 0 else h / float(w) 
            if (1.43 <= ar <= 1.58):
                cv2.drawContours(image, [box], -1, (0, 255, 0), 3)
                count += 1 
                #to keep track of how many contours is found for debug purposes    
                print ("contours = ",count)
                #New list of contours post dimension check
                card = contours[count]
                peri = cv2.arcLength(card,True)
                approx = cv2.approxPolyDP(card,0.01*peri,True)
                pts = np.float32(approx)

                x,y,w,h = cv2.boundingRect(card)

                # Flatten the card and convert it to 200x300

                warp = flattener(image,pts,w,h)
                #colours = cv2.inRange(warp, 70, 110)
                #colours = cv2.inRange(warp,0, 70)

                #
                #Below is multiple different threshholds and blurs of different kinds used in different versions of the script throughout the project. 
                #Most are commented out, since they could still be used in a given situation and this script is partly for testing different options
                #
                blur = cv2.GaussianBlur(warp,(5,5),2 )
                thresh = cv2.adaptiveThreshold(blur,255,1,1,101,20)
                #thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,51,10)

                #Currently this is what we return at the end of the code. At this point we have a 200x300 pixel image that has been thresholded again
                blur_thresh = cv2.GaussianBlur(thresh,(5,5),5)

                #The rest of the code is to create zoomed crops of the corners of the cards and process them with image recognition aswell
                #This was used in the beginning but has not been used for the final implementations as we went away from the corner solutions
                #However it is still kept, as it could still be relevant to look for a proper solution using the corners, since that would be most optimal
                corner = warp[0:84, 7:30]
                corner_zoom = cv2.resize(corner, (0,0), fx=4, fy=4)
                corner_blur = cv2.GaussianBlur(corner_zoom,(5,5),0)
                #corner_thresh = cv2.adaptiveThreshold(corner_blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,101,10)
                #corner_thresh = cv2.adaptiveThreshold(corner_blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,101,1)
                corner_thresh = cv2.adaptiveThreshold(corner_blur,255,1,1,251,1)
                #corner_blur = cv2.bilateralFilter(corner_zoom, 10, 150, 10)
                #retval, corner_thresh = cv2.threshold(corner_blur, 180, 255, cv2. THRESH_BINARY_INV)
                     
                if i <= 13: # Isolate rank
                    rank = corner_thresh[20:185, 0:128] # Grabs portion of image that shows rank
                    rank_cnts, hier= cv2.findContours(rank, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
                    rank_cnts = sorted(rank_cnts, key=cv2.contourArea,reverse=True)
                    x,y,w,h = cv2.boundingRect(rank_cnts[0])
                    rank_roi = rank[y:y+h, x:x+w]
                    rank_sized = cv2.resize(rank_roi, (RANK_WIDTH, RANK_HEIGHT), 0, 0)
                    final_img = rank_sized
                if i > 13: # Isolate suit
                    suit = corner_thresh[186:336, 0:128] # Grabs portion of image that shows suit
                    suit_cnts, hier = cv2.findContours(suit, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
                    suit_cnts = sorted(suit_cnts, key=cv2.contourArea,reverse=True)
                    x,y,w,h = cv2.boundingRect(suit_cnts[0])
                    suit_roi = suit[y:y+h, x:x+w]
                    suit_sized = cv2.resize(suit_roi, (SUIT_WIDTH, SUIT_HEIGHT), 0, 0)
                    final_img = suit_sized
                cv2.imshow("Image2-{}".format(count), blur_thresh)
                print (warp)
                cv2.imwrite(img_path+"{}".format(count)+ '.jpg',blur_thresh)


    return image


img = cv2.imread("A-3.jpg")

cv2.imshow('Cards1', processing(img))

cv2.waitKey(0)