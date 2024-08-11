import cv2
import pickle  #we are using pickle to save all the positions of parking spaces and then use them in the main.py

# img = cv2.imread('carParkImg.png')
width, height = 110, 50  # width = 160-50 and height = 240-190

try:
    with open('CarParkPos',"rb") as f:  #checking if we already have the pickle object if yes we just add it to the posList
        posList = pickle.load(f)
except:
    posList = []


def mouseClick(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:  #if we press the left button as an event , then append to our list
        posList.append((x,
                        y))  #here we are appending the x1,y1 and x2,y2 points of the bounding box which we create (by clicking) to the posList
    if events == cv2.EVENT_RBUTTONDOWN:  #to delete an already created bounding box
        for i, pos in enumerate(posList):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                posList.pop(i)

    with open('CarParkPos',"wb") as f:   #here after creating bounding boxes we are saving them as pickle objects (using file handling)
        pickle.dump(posList, f)


while True:
    img = cv2.imread(
        'carParkImg.png')  #Since we use deletion of boxes as well. The image needs to be dynamic hence it should be generated again and again hence it is the loop
    # cv2.rectangle(img,(50,190),(160,240),(255,0,255),2)   #creating a rectangle around the parking spaces x1,y1 is top left of the rectangle and x2,y2 is bottom right of the rectangle

    for pos in posList:
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)

    cv2.imshow('Image', img)
    cv2.setMouseCallback("Image",mouseClick)  #to detect mouse click . On a mouse click the mentioned function will be executed
    # print(posList)
    cv2.waitKey(1)
