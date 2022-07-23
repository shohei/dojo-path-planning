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
    plt.figure()
    plt.imshow(cv2.cvtColor(output, cv2.COLOR_BGR2RGB))

plt.show()
