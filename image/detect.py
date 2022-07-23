import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread("./image/target.png") 
plt.figure('original')
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

yellow_filter = [(20, 80, 10), (50, 255, 255)]
red_filter = [(0,100,20), (10,255,255)]
blue_filter = [(90,35,14), (170,255,255)]
green_filter = [(70,22,16), (94,255,255)]
filters = []
filters.append(red_filter)
filters.append(blue_filter)
filters.append(green_filter)
filters.append(yellow_filter)

for f in filters:
    lower_color = np.array(f[0])
    upper_color = np.array(f[1])
    mask = cv2.inRange(hsv, lower_color, upper_color)
    output = cv2.bitwise_and(hsv, hsv, mask = mask)

    chips = output
    chips_gray = cv2.cvtColor(chips, cv2.COLOR_BGR2GRAY)
    chips_preprocessed = cv2.GaussianBlur(chips_gray, (5, 5), 0)
    _, chips_binary = cv2.threshold(chips_preprocessed, 100, 255, cv2.THRESH_BINARY)
    chips_contours, _ = cv2.findContours(chips_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    min_chip_area = 60
    large_contours = [cnt for cnt in chips_contours if cv2.contourArea(cnt) > min_chip_area]
    bounding_img = np.copy(chips)
    for contour in large_contours:
    	rect = cv2.minAreaRect(contour)
    	box = cv2.boxPoints(rect)
    	box = np.int0(box)
    	cgx = int(rect[0][0])
    	cgy = int(rect[0][1])
    	leftx = int(cgx - (rect[1][0]/2.0))
    	lefty = int(cgy - (rect[1][1]/2.0))
    	angle = round(rect[2],1)
    	cv2.drawContours(bounding_img,[box],0,(0,0,255),2)
    	cv2.circle(bounding_img,(cgx,cgy), 10, (255,0,0), -1)
    	font = cv2.FONT_HERSHEY_SIMPLEX
    	cv2.putText(bounding_img,'x='+str(round(leftx))+', y='+str(round(lefty)),(leftx,lefty), font, 0.6, (255,255,255),2,cv2.LINE_AA)

    plt.figure()
    plt.imshow(cv2.cvtColor(bounding_img, cv2.COLOR_BGR2RGB))

plt.show()

