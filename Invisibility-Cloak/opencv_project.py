import cv2
import numpy as np
import time

win_name = "Invisibilty-cloak"
cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)

source = cv2.VideoCapture(0)
time.sleep(3)
count = 0
background = 0

#Capture the background in range of 60
for i in range(60):
    has_frame, background = source.read()
    if not has_frame:
        continue
background = np.flip(background, 1)  # flipping the frame

#Detect the red colored cloak using color detection
#and segmentation algorithm.

#Read every frame from the webcam
while (source.isOpened()):
    has_frame, image = source.read()
    if not has_frame:
        print("Camera not identified")
        break
    count += 1
    image = np.flip(image, 1)

    #Convert the color space from BGR to HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    #Generate masks to detect red color
    #Uncomment the others to detect other colors
    # Defining lower range for red color detection.
    # lower_red = np.array([0, 120, 70])
    # upper_red = np.array([10, 255, 255])
    # mask1 = cv2.inRange(hsv, lower_red, upper_red)

    # Defining upper range for red color detection
    # lower_red = np.array([170, 120, 70])
    # upper_red = np.array([180, 255, 255])
    # mask2 = cv2.inRange(hsv, lower_red, upper_red)

    low_blue = np.array([94, 80, 2])
    high_blue = np.array([126, 255, 255])
    mask3 = cv2.inRange(hsv, low_blue, high_blue)

    # low_green = np.array([25, 52, 72])
    # high_green = np.array([102, 255, 255])
    # mask = cv2.inRange(hsv, low_green, high_green)

    #to detect any color except white
    # low = np.array([0, 42, 0])
    # high = np.array([179, 255, 255])
    # mask5 = cv2.inRange(hsv, low, high)

    # Adding two masks to generate the final mask
    mask = mask3

    #Dilate the mask image
    mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8))

    #Generate final Augmented Output
    #Replacing pixels corresponding to cloak with the background pixels
    image[np.where(mask == 255)] = background[np.where(mask == 255)]
    cv2.imshow(win_name, image)
    if cv2.waitKey(10) == 27:
        break

source.release()
cv2.destroyAllWindows()
