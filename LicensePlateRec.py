import numpy as np
import cv2
from copy import deepcopy
from PIL import Image
import pytesseract as tess

def preprocess(img):
	imgBlurred = cv2.GaussianBlur(img, (5,5), 0)
	gray = cv2.cvtColor(imgBlurred, cv2.COLOR_BGR2GRAY)
	sobelx = cv2.Sobel(gray,cv2.CV_8U,1,0,ksize=3)
	ret2,threshold_img = cv2.threshold(sobelx,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

	return threshold_img

def extract_contours(threshold_img):
	element = cv2.getStructuringElement(shape=cv2.MORPH_RECT, ksize=(17, 3))
	morph_img_threshold = threshold_img.copy()
	cv2.morphologyEx(src=threshold_img, op=cv2.MORPH_CLOSE, kernel=element, dst=morph_img_threshold)
	_, contours, hierarchy= cv2.findContours(morph_img_threshold,mode=cv2.RETR_EXTERNAL,method=cv2.CHAIN_APPROX_NONE)
	
	return contours

def detect(img):
	threshold_img = preprocess(img)
	contours= extract_contours(threshold_img)
	
	if (len(contours) > 0):
		return True	 

def main():
	for c in range(0,600):
		img = cv2.imread('1/'+str(c)+'.jpg')
		print(str(c)+'  ', end='')
		detect(img)

if __name__ == '__main__':
	main()
	
