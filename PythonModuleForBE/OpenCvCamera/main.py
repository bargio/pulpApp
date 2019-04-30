from imageai.Detection import *
from myDetector import *
import cv2
import pandas as pd
import argparse
import numpy as np
import os
from CsvCreator import CsvCreator
import matplotlib.pyplot as plt
from tkinter import *


video = cv2.VideoCapture(0)
ORB_MAX_FEATURES = 500
GOOD_MATCH_PERCENT = 1




def readVideo():
    first_frame = None
    startCount=0
    #csv_saver.createFile()
    # csv = pd.read_csv("C:\\Users\\NttdataSky\\PycharmProjects\\OpenCvCamera\\cuzzy\\gio.csv")
    # print(csv.keys())
    # print(csv.shape)
    # print(csv.image_byte)
    # rows,cols = csv.shape
    # frame_resized = [[0 for x in range(32)] for y in range(32)]
    # for i in range(rows):
    #     for j in range(cols):
    #         frame_resized[i,j]=csv[i][j]
    # cv2.imshow("test",frame_resized)
    # sys.exit()
    while True:
        check, frame = video.read()

        gray,color_frame = modifyFrame(frame)

        #take first frame for show differences
        if first_frame is None:
            first_frame = gray
            continue

        faceDetection(gray,frame,startCount)
        startCount +=1
        drawContour(first_frame,gray,frame)
        imReference = cv2.imread("hand.png", cv2.COLOR_BAYER_RG2BGR)
        #show video
        cv2.imshow("Video", frame)
        #cv2.imshow("Gray", gray)

        (cnts, _) = cv2.findContours(imReference.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for contour in cnts:
            if cv2.contourArea(contour) < 10000:
                continue

        (x, y, w, h) = cv2.boundingRect(contour)
        #cv2.drawContours(frame, contour, -1, (255, 0, 223), 3)
        cv2.rectangle(imReference, (x, y), (x+w, y+h), (0, 255, 0), 3)
        cv2.polylines(imReference,contour,True,(0,255,255))

        cv2.imshow("White",imReference)
        #cv2.imshow("hand.png",imReference)

        #close key
        key = cv2.waitKey(1)
        if key == ord('q'):
            break




        # execution_path = os.getcwd()
        #
        #
        #
        # detector = ObjectDetection()
        # detector.setModelTypeAsYOLOv3()
        # detector.setModelPath(os.path.join(execution_path , "yolo.h5"))
        # detector.loadModel()
        # detections, extracted_images = detector.detectObjectsFromImage(frame,input_type="stream", extract_detected_objects=True)
        #detected_copy = detector.detectObjectsFromVideo(camera_input=video, output_file_path=os.path.join(execution_path, "camera_detected_1"),frames_per_second=29, log_progress=True)

        # cv2.imshow("detected_copy",extracted_images)

def modifyFrame(frame):
    grayframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    colorframe = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    #grayframe =  cv2.GaussianBlur(gratframe,(21,21),0)
    return grayframe, colorframe

def giveDeltaFrame(first_frame,grayframe):
    delta_frame = cv2.absdiff(first_frame,grayframe)
    th_delta = cv2.threshold(delta_frame, 50, 255,cv2.THRESH_BINARY)[1]
    th_delta = cv2.erode(th_delta, None, iterations=2)
    cv2.adaptiveThreshold(grayframe, 110, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 115, 1)
    return th_delta


def faceDetection(gray, frame,count):
    face_cascade = cv2.CascadeClassifier('C:\\Users\\NttdataSky\\PycharmProjects\\CameraOpenCV\\venv\\Lib\\site-packages\\cv2\\data\\haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('C:\\Users\\NttdataSky\\PycharmProjects\\CameraOpenCV\\venv\\Lib\\site-packages\\cv2\\data\\haarcascade_eye.xml')
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        #show face
        cv2.imshow("frame1",gray[y:y+h, x:x+w])
        eyes = eye_cascade.detectMultiScale(roi_gray)
        #savePngForRecognition(gray[y:y+h, x:x+w],count)
        #resizeAndSaveFile(gray[y:y+h, x:x+w])
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

    return

csv_saver =  CsvCreator('gio.csv',"C:\\Users\\NttdataSky\\PycharmProjects\\OpenCvCamera\\cuzzy\\")
def saveCsvFile(image_string):
    #csv_saver.addStringToCsv('gio',32,'1,2,3,4,565,76,7768,34,32,4321,23,4,13,12,312,312,3123123,213,1')
    csv_saver.addStringToCsv(image_string)


def resizeAndSaveFile(gray_frame):
    frame_resized = cv2.resize(gray_frame,(32,32))
    rows,cols = frame_resized.shape
    print(frame_resized.shape)
    for i in range(rows):
        write=''
        for j in range(cols):
            k = frame_resized[i,j]
            write=write+str(k)+','
        saveCsvFile(write)

    cv2.imshow("resized", frame_resized)
    sys.exit()

def savePngForRecognition(frame,count):
    #askName()
    #plt.imshow(frame) #Needs to be in row,col order
    path = 'C:\\Users\\NttdataSky\\PycharmProjects\\OpenCvCamera'
    name = "cuzzy/cuzzy%d.jpg"%count
    completeName = os.path.join(path, name)
    cv2.imwrite(completeName, frame)




window = Tk()
txt = Entry(window,width=10)
def askName():
    window.title("WriteName")
    window.geometry('350x200')
    lbl = Label(window, text="Name?")
    lbl.grid(column=0, row=0)
    txt.grid(column=1, row=0)
    btn = Button(window, text="Save", command=clicked)
    btn.grid(column=2, row=0)
    window.mainloop()


def clicked():
    name = txt.get()
    print("name is " + name)()



def drawContour(firstframe,grayframe,frame):
    th_delta = giveDeltaFrame(firstframe,grayframe)
    (cnts, _) = cv2.findContours(th_delta.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour in cnts:
        if cv2.contourArea(contour) < 10000:
         continue

        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.drawContours(frame, contour, -1, (255, 0, 223), 3)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
        cv2.polylines(th_delta,contour,True,(0,255,255))
    return


def findCorrispondingImage(gray_to_find, gray_frame):
    orb = cv2.ORB_create(ORB_MAX_FEATURES)
    keypoints1, descriptors1 = orb.detectAndCompute(gray_to_find, None)
    keypoints2, descriptors2 = orb.detectAndCompute(gray_frame, None)

    matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMINGLUT)
    matches = matcher.match(descriptors1, descriptors2, None)

    # Sort matches by score
    matches.sort(key=lambda x: x.distance, reverse=False)

    # Remove not so good matches
    numGoodMatches = int(len(matches) * GOOD_MATCH_PERCENT)
    matches = matches[:numGoodMatches]

    # Draw top matches
    imMatches = cv2.drawMatches(gray_to_find, keypoints1, gray_frame, keypoints2, matches, None)
    cv2.imwrite("matches.jpg", imMatches)

    # Extract location of good matches
    points1 = np.zeros((len(matches), 2), dtype=np.float32)
    points2 = np.zeros((len(matches), 2), dtype=np.float32)

    for i, match in enumerate(matches):
        points1[i, :] = keypoints1[match.queryIdx].pt
        points2[i, :] = keypoints2[match.trainIdx].pt

    # Find homography
    h, mask = cv2.findHomography(points1, points2, cv2.RANSAC)

    # Use homography
    height, width = gray_frame.shape
    im1Reg = cv2.warpPerspective(gray_frame, h, (width, height))

    return imMatches



print('--- Start recognize video ---')
print(cv2.__version__)
readVideo()
print('--- End recognize video ---')
