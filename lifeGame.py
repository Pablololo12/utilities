#!/usr/bin/env python3
# Author: pabloheralm@gmail.com
#         @pablololo12

import sys
import pygame
import time
import random
import getopt
from pygame.locals import *

width = 100
heidth = 100
tileSize = 5
time_millis = 100

colours = {
	0 : (0,0,0),
	1 : (255, 255, 255)
}

def check_board(board):
	aux = [[0 for i in range(width)] for j in range(heidth)]
	for i in range(width):
		for j in range(heidth):
			neighbours = 0
			#down up
			neighbours = neighbours + board[i][j-1]
			neighbours = neighbours + board[i][(j+1)%heidth]
			#right left
			neighbours = neighbours + board[i-1][j]
			neighbours = neighbours + board[(i+1)%width][j]
			#up right left
			neighbours = neighbours + board[i-1][(j+1)%heidth]
			neighbours = neighbours + board[(i+1)%width][(j+1)%heidth]
			#down right left
			neighbours = neighbours + board[i-1][j-1]
			neighbours = neighbours + board[(i+1)%width][j-1]

			if neighbours==3 and board[i][j]==0:
				aux[i][j]=1
			if board[i][j]==1:
				if neighbours==2 or neighbours==3:
					aux[i][j]=1
	return aux


def main(argv):
	board = [[0 for i in range(width)] for j in range(heidth)]
	lastTime = 0
	pause = 1
	rand = 0

	try:
		opts, args = getopt.getopt(argv,"hr")
	except getopt.GetoptError:
		print("lifeGame.py [-h|-r]")
		sys.exit(2)

	for opt, arg in opts:
		if opt == '-h':
			print("-h to help")
			print("-r random board")
			sys.exit()
		elif opt == '-r':
			rand = 1
			for i in range(width):
				for j in range(heidth):
					board[i][j]=random.randint(0,1)
	
	pygame.init()
	DISPLAY = pygame.display.set_mode((width*tileSize, heidth*tileSize+50))
	button = pygame.draw.rect(DISPLAY, (255,0,0), ((width*tileSize)/2-10, heidth*tileSize+10, 20,20))
	if rand==1:
		for i in range(width):
			for j in range(heidth):
				pygame.draw.rect(DISPLAY, colours[board[i][j]], (i*tileSize, j*tileSize, tileSize, tileSize))
	pygame.display.update()

	while True:

		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				pos = pygame.mouse.get_pos()
				if button.collidepoint(pos):
					if pause == 1:
						pause = 0
						button = pygame.draw.rect(DISPLAY, (0,255,0), ((width*tileSize)/2-10, heidth*tileSize+10, 20,20))
					else:
						pause = 1
						button = pygame.draw.rect(DISPLAY, (255,0,0), ((width*tileSize)/2-10, heidth*tileSize+10, 20,20))
				else:
					y = int(pos[1]/tileSize)
					x = int(pos[0]/tileSize)
					if y > heidth-1:
						break
					if board[x][y] == 0:
						board[x][y] = 1
					else:
						board[x][y] = 0
					for i in range(width):
						for j in range(heidth):
							pygame.draw.rect(DISPLAY, colours[board[i][j]], (i*tileSize, j*tileSize, tileSize, tileSize))
				pygame.display.update()


		#Update every second
		milli_sec = int(round(time.time() * 1000))
		if (milli_sec - time_millis) > lastTime and pause == 0:
			lastTime = milli_sec
			board = check_board(board)
			for i in range(width):
				for j in range(heidth):
					pygame.draw.rect(DISPLAY, colours[board[i][j]], (i*tileSize, j*tileSize, tileSize, tileSize))
			pygame.display.update()

if __name__ == '__main__':
    main(sys.argv[1:])
