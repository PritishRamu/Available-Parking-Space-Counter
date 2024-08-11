import  cv2
import pickle
import cvzone
import numpy as np

width, height = 110, 50

#Video
cap=cv2.VideoCapture('carPark.mp4')

with open('CarParkPos',"rb") as f:
    posList = pickle.load(f)


def CheckingParkingSpace(imgPro):

    spaceCounter=0  #initialising the variable which will counter the empty parking spaces


    for pos in posList:
        x,y=pos

        imgCrop=imgPro[y:y+height,x:x+width]  #cropping the image according to the condition
        # cv2.imshow(str(x*y),imgCrop)

        count=cv2.countNonZero(imgCrop)   #counting the number of pixels in 'imgCrop'
        cvzone.putTextRect(img,str(count),(x,y+height-3),scale=1,thickness=2 ,offset=0)   #displaying the count of pixels in front of the cropped image i.e parking spot

        if count<900:
            color=(0,255,0)     #if parking spot  is vacant we keep it's color as green
            thickness=5
            spaceCounter=spaceCounter+1   #incrementing the variable by one when the parking space is free
        else:
            color=(0,0,255)   #if parking spot  is not vacant we keep it's color as red
            thickness = 2
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
    cvzone.putTextRect(img,f'Available:{spaceCounter}/{len(posList)}',(100,60),scale=3,thickness=5 ,offset=20,colorR=(0,200,0))   #displaying the count of pixels in front of the cropped image i.e parking spot






while True:

    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):    #LHS will give us the current position of frame and RHS gives us the total number of frames in the video
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)   #we reset the frames if they reach the total amount of frames that the video has

    success,img=cap.read()
    imgGray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)  #converting the image into gray scale so that we can determine whether a car is present in the spot or not
    imgBlur=cv2.GaussianBlur(imgGray,(3,3),1)#blurring the image
    imgThreshold=cv2.adaptiveThreshold(imgBlur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,25,16)

    imgMedian=cv2.medianBlur(imgThreshold,5)
    kernel=np.ones((3,3),np.uint8)
    imgDilate=cv2.dilate(imgMedian,kernel,iterations=1)   #we do this to thicken the borders so we can easily differentiate between empty  parking spot and occupied  parking spot


    CheckingParkingSpace(imgDilate)

    # for pos in posList:

    #
    #
    # cv2.imshow('ImageBlur',imgBlur)
    # cv2.imshow('ImageThreshold',imgThreshold)
    cv2.imshow('Image',img)
    # cv2.resize('Image',600,600)

    # cv2.imshow('ImageMedian',imgMedian)
    # cv2.imshow('ImageDilate',imgDilate)
    cv2.waitKey(10)       #changing the value of cv2.waitKey will adjust the playback speed of the video


#58:57
