#!/usr/bin/env python
# Author: pabloheralm@gmail.com
#         @pablololo12

import sys
import getopt
import numpy as np
import cv2
import colorsys

threshold = 50.0

def add(colors, color):
	added = 0
	if colors is None:
		colors = []
		colors.append(color)
		return colors
	#print len(colors)
	best_i = 0
	best_diff = 1000.0
	for i in range(len(colors)):
		diff = (colors[i][0]-color[0])**2 + (colors[i][1]-color[1])**2 + (colors[i][2]-color[2])**2
		diff = np.sqrt(diff)
		#print diff
		if diff < threshold:
			if diff < best_diff:
				best_i = i
				best_diff = diff
				added = 1

	if added == 1:
		colors[best_i][0] = (colors[best_i][0] + color[0])/2
		colors[best_i][1] = (colors[best_i][1] + color[1])/2
		colors[best_i][2] = (colors[best_i][2] + color[2])/2
		colors[best_i][3] = colors[best_i][3] + 1

	if added == 0:
		colors.append(color)
	print len(colors)
	return colors

def takeOrder(elem):
    return elem[3]

def getColorsSort(image):
	colors = []
	for i in range(image.shape[0]):
		for d in range(image.shape[1]):
			colors = add(colors, [image.item(i,d,0), image.item(i,d,1), image.item(i,d,2), 0])
	
	colors.sort(key=takeOrder, reverse=True)
	return colors

def draw_with_colors(image, colors):
	aux = np.zeros(image.shape, image.dtype)
	
	for i in range(image.shape[0]):
		for d in range(image.shape[1]):
			best_t = 0
			best_diff = 1000.0
			for t in range(len(colors)):
				diff = (colors[t][0]-image.item(i,d,0))**2 + (colors[t][1]-image.item(i,d,1))**2 + (colors[t][2]-image.item(i,d,2))**2
				diff = np.sqrt(diff)
				if diff < best_diff:
					best_t = t
					best_diff = diff
			aux[i,d] = [colors[best_t][0], colors[best_t][1], colors[best_t][2]]
	return aux


def palette(image):
	image1 = np.ones((image.shape[0]+200+image.shape[0], image.shape[1], image.shape[2]), image.dtype) * 255
	colors = getColorsSort(image)
	# Colocamos la imagen pequena dentro de la grande
	image1[0:image.shape[0], 0:image.shape[1]] = image
	space = image.shape[1]/11
	
	cv2.rectangle(image1, (space*3, image.shape[0]+50), (space*4, image.shape[0]+150), colors[0][0:2], thickness=-1)
	cv2.rectangle(image1, (space*4, image.shape[0]+50), (space*5, image.shape[0]+150), colors[1][0:2], thickness=-1)
	cv2.rectangle(image1, (space*5, image.shape[0]+50), (space*6, image.shape[0]+150), colors[2][0:2], thickness=-1)
	cv2.rectangle(image1, (space*6, image.shape[0]+50), (space*7, image.shape[0]+150), colors[3][0:2], thickness=-1)
	cv2.rectangle(image1, (space*7, image.shape[0]+50), (space*8, image.shape[0]+150), colors[4][0:2], thickness=-1)

	colors = colors[0:5]
	print colors
	image2 = draw_with_colors(image, colors)
	image1[image.shape[0]+200:image1.shape[0], 0:image.shape[1]] = image2

	return image1

def main(argv):
	try:
		opts, args = getopt.getopt(argv,"hf:t:")
	except getopt.GetoptError:
		print("imgSketch.py [-h | -f [image]")
		sys.exit(2)

	image = 0
	for opt, arg in opts:
		if opt == '-h':
			print("-h to help")
			print("-f [image]")
			print("-t [threshold] to change threshold")
			sys.exit()
		elif opt == '-f':
			image = arg
		elif opt == '-t':
			threshold = arg

	if image == 0:
		sys.exit(0)

	# Extract name
	name = image.split(".")[-2].split("/")[-1]
	ext = image.split(".")[-1]
	name = name + "_palette." + ext

	image = cv2.imread(image)
	result = palette(image)
	cv2.imwrite(name,result)

if __name__ == '__main__':
    main(sys.argv[1:])