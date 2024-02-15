import cv2
import numpy as np

image1 = cv2.imread('C:/Users/SalmanTrader/OneDrive/Pictures/CS Logo.png')
image2 = cv2.imread('C:/Users/SalmanTrader/OneDrive/Pictures/Comfy Sloth Link.jpg')

width, height = 500, 500
image1 = cv2.resize(image1, (width, height))
image2 = cv2.resize(image2, (width, height))

collage = np.zeros((height, width * 2, 3), dtype=np.uint8)

collage[:height, :width] = image1
collage[:height, width:] = image2

cv2.imshow('Collage', collage)
cv2.waitKey(0)
cv2.destroyAllWindows()
