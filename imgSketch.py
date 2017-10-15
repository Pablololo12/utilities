#!/usr/bin/env python
# Author: pabloheralm@gmail.com
#         @pablololo12

import sys
import getopt
import numpy as np
import cv2
import random


def getColors(image):
	colors = []
	for i in range(image.shape[0]):
		for d in range(image.shape[1]):
			#BGR
			colors.append([image.item(i,d,0), image.item(i,d,1), image.item(i,d,2)])
	return colors

def print_circle(image, colors):
	color = colors[random.randint(0,len(colors)-1)]
	radius = random.randint(5, 20)
	y_pos = random.randint(0,image.shape[0]-1)
	x_pos = random.randint(0,image.shape[1]-1)
	cv2.circle(image, (x_pos,y_pos) , radius, color, -1)
	x1 = x_pos - radius
	x2 = x_pos + radius
	y1 = y_pos - radius
	y2 = y_pos + radius
	
	if x2 < 0:
		x2=0
	elif x2 > image.shape[1]-1:
		x2 = image.shape[1]-1
	if y2 < 0:
		y2=0
	elif y2 > image.shape[0]-1:
		y2 = image.shape[0]-1

	if x1 < 0:
		x1=0
	elif x1 > image.shape[1]-1:
		x1 = image.shape[1]-1
	if y1 < 0:
		y1=0
	elif y1 > image.shape[0]-1:
		y1 = image.shape[0]-1
	
	return image, x1, y1, x2, y2

def print_line(image, colors):
	color = colors[random.randint(0,len(colors)-1)]
	radians = random.uniform(0, 6.28318530718)
	lenth = random.randint(5,30)
	y1 = random.randint(0,image.shape[0]-1)
	x1 = random.randint(0,image.shape[1]-1)
	y2 = int(lenth * np.sin(radians) + y1)
	x2 = int(lenth * np.cos(radians) + x1)
	if x2 < 0:
		x2=0
	elif x2 > image.shape[1]-1:
		x2 = image.shape[1]-1
	if y2 < 0:
		y2=0
	elif y2 > image.shape[0]-1:
		y2 = image.shape[0]-1

	cv2.line(image, (x1, y1), (x2, y2), color)
	if x2 < x1:
		tmp = x2
		x2 = x1
		x1 = tmp
	if y2 < y1:
		tmp = y2
		y2 = y1
		y1 = tmp

	return image, x1, y1, x2, y2

def compare_images(image1, image2):
	acum = np.sum((image1.astype("float") - image2.astype("float")) ** 2)
	#acum = np.sum(abs(image1.astype("float") - image2.astype("float")))
	return acum

def compare_images_box(image1, image2, x1, y1, x2, y2):
	acum = np.sum((image1[y1:y2+1,x1:x2+1].astype("float") - image2[y1:y2+1,x1:x2+1].astype("float")) ** 2)
	return acum


def generateImage(image, iterations, what):
	image1 = np.zeros(image.shape, image.dtype)
	image2 = np.zeros(image.shape, image.dtype)
	colors = getColors(image)
	diff2 = compare_images(image, image2)
	
	for i in range(int(iterations)):
		if what == 0:
			image1, x1, y1, x2, y2 = print_circle(image1, colors)
			diff1 = compare_images_box(image, image1, x1, y1, x2, y2)
			diff2 = compare_images_box(image, image2, x1, y1, x2, y2)
		elif what == 1:
			image1, x1, y1, x2, y2 = print_line(image1, colors)
			diff1 = compare_images_box(image, image1, x1, y1, x2, y2)
			diff2 = compare_images_box(image, image2, x1, y1, x2, y2)
		
		if diff1 < diff2:
			image2 = image1.copy()
		else:
			image1 = image2.copy()

	return image2

def main(argv):
	try:
		opts, args = getopt.getopt(argv,"hf:i:l")
	except getopt.GetoptError:
		print("imgSketch.py [-h | -f [image] | -i numIter] | -l")
		sys.exit(2)

	image = 0
	iterations = 10000
	what = 0
	for opt, arg in opts:
		if opt == '-h':
			print("-h to help")
			print("-f [image]")
			print("-i number of iterations")
			print("-l to use lines")
			sys.exit()
		elif opt == '-f':
			image = arg
		elif opt == '-i':
			iterations = arg
		elif opt == '-l':
			what = 1

	if image == 0:
		sys.exit(0)

	# Extract name
	name = image.split(".")[-2].split("/")[-1]
	ext = image.split(".")[-1]
	name = name + "_sketch." + ext

	image = cv2.imread(image)
	result = generateImage(image, iterations, what)
	cv2.imwrite(name,result)

if __name__ == '__main__':
    main(sys.argv[1:])