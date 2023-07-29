import mediapipe as mp
import cv2
import time
import numpy as np
import serial 

ser = serial.Serial('COM5', 9600)

cap =cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

#initialize the hand class as store in variable
mpHands = mp.solutions.hands

#set the hand function which will hold the landmark points
hands = mpHands.Hands()
#hands = mpHands.Hands()

mpDraw = mp.solutions.drawing_utils
list_marks = np.zeros([21,3])

intensity_list = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

while(cap.isOpened()):
    ret, frame = cap.read()
    if(ret== False):
        break
    if(ret):
        flipped_frame = cv2.flip(frame,1) # if 0 upside down #BGR -opencv 
        
        #so we need to convert to RGB as mediapipe reads in that format
        RGBframe = cv2.cvtColor(flipped_frame,cv2.COLOR_BGR2RGB)
        results = hands.process(RGBframe) #RGB
        #print(results)
        results.multi_hand_landmarks
        #print(results.multi_hand_landmarks) #X, Y, Z z in depth
        
        if(results.multi_hand_landmarks):
            for i in range(0, len(results.multi_hand_landmarks)): # to choose one hand
                handLms = results.multi_hand_landmarks[i] # to choose one hand with the landmark
                for ilm, lm in enumerate(handLms.landmark): # enumerate = to get the index for the array
                    #print(handLms.landmark)
                    h,w,x = flipped_frame.shape
                    lm_x, lm_y = int(lm.x*w), int(lm.y*h)
                    #list_marks.append([i,ilm,lm_x,lm_y]) #i = index of the hand. max 2 hands... ilm = 21 points
                    list_marks[ilm] = [ilm, lm_x, lm_y]
                
                thumb_tip_x = list_marks[4][1]
                thumb_tip_y = list_marks[4][2]
                index_tip_x = list_marks[8][1]
                index_tip_y = list_marks[8][2]
                R = np.sqrt((thumb_tip_x - index_tip_x)**2 + (thumb_tip_y - index_tip_y)**2)
                #print(R)
                val = int((R/250)*25) #
                intesity = intensity_list[val]
                print(val)
                
                ser.write(intesity.encode())
                mpDraw.draw_landmarks(flipped_frame,handLms,mpHands.HAND_CONNECTIONS)
            
        
        cv2.imshow("Frame",flipped_frame)
        
        
        if(cv2.waitKey(1) & 0xFF ==ord('q')):
            cap.release()
            ser.close()
            cv2.destroyAllWindows()
            break
    else:
        break
    
    #virtul reality augmented reality