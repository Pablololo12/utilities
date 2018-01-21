#!/usr/bin/env python3
# Author: pabloheralm@gmail.com
#         @pablololo12

import pygame
from pygame.locals import *
import math
import random

MIN_ASTEROIDS=25
MAX_ASTEROIDS=30

class Asteroids:

	def __init__(self):
		#self.w=640
		#self.h=480
		self.w=1200
		self.h=700
		self.WHITE=(255,255,255)
		self.BLACK=(0,0,0)
		self.size=(self.w,self.h)
		self.clock = pygame.time.Clock()

		self.exit = False
		self.collision = False

		self.U_P = False
		self.L_P = False
		self.R_P = False
		self.S_P = False
		self.pause = False
		self.reset = False
		self.spawn = False

		self.poship=[self.w/2,self.h/2,0]
		self.vel=[0,0]

		self.shoots=[]

		self.asteroids = []

		random.seed()

		pygame.init()
		self.font = pygame.font.SysFont(pygame.font.get_default_font(),50,bold=True)
		self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE|pygame.RESIZABLE)

	def event(self, event):
		if event.type == QUIT:
			self.exit = True
		if event.type == KEYDOWN:
			if event.key == K_UP:
				self.U_P = True
			if event.key == K_LEFT:
				self.L_P = True
			if event.key == K_RIGHT:
				self.R_P = True
			if event.key == K_SPACE:
				self.S_P = True
			if event.key == K_p:
				self.pause = ~self.pause
			if event.key == K_r:
				self.reset = True
			if event.key == K_q:
				self.exit = True
			if event.key == K_s:
				self.spawn = True
		if event.type == KEYUP:
			if event.key == K_UP:
				self.U_P = False
			if event.key == K_LEFT:
				self.L_P = False
			if event.key == K_RIGHT:
				self.R_P = False
			if event.key == K_s:
				self.spawn = False
		if event.type==VIDEORESIZE:
			self.screen=pygame.display.set_mode(event.dict['size'],pygame.HWSURFACE|pygame.RESIZABLE)
			self.w=event.dict['size'][0]
			self.h=event.dict['size'][1]
			self.size=(self.w,self.h)

	def get_pol_ship(self, pos):
		ship=[]
		r = 10
		angle = pos[2]
		ship.append((pos[0]+r*math.cos(angle),pos[1]+r*math.sin(angle)))
		angle = angle + 2*math.pi/3
		ship.append((pos[0]+r*math.cos(angle),pos[1]+r*math.sin(angle)))

		ship.append((pos[0],pos[1]))
		angle = angle + 2*math.pi/3
		ship.append((pos[0]+r*math.cos(angle),pos[1]+r*math.sin(angle)))
		return ship

	def normalize(self, vec):
		norm = math.sqrt(vec[0]*vec[0]+vec[1]*vec[1])
		return [vec[0]/norm,vec[1]/norm]

	def check_limits(self, pos):
		out = False
		newpos=[pos[0],pos[1]]
		if pos[0] > self.w:
			newpos[0] = 0
			out = True
		if pos[0] < 0:
			newpos[0] = self.w
			out = True
		if pos[1] > self.h:
			newpos[1] = 0
			out = True
		if pos[1] < 0:
			newpos[1] = self.h
			out = True
		return newpos,out

	def get_new_asteroid(self):
		# Random position
		asteroid = [[random.randint(0,self.w),random.randint(0,self.h)]]
		# Random direction
		angle = random.uniform(0,2*math.pi)
		asteroid.append([math.cos(angle)/10,math.sin(angle)/10])

		angles = []
		for i in range(0,random.randint(5,9)):
			angles.append(random.uniform(0,2*math.pi))

		angles.sort()
		pos = asteroid[0]
		for angle in angles:
			rad = random.randint(25,35)
			asteroid.append([pos[0]+rad*math.cos(angle),pos[1]+rad*math.sin(angle)])

		return asteroid

	def inside_triangle(self, point,p0,p1,p2):
		s = p0[1]*p2[0]-p0[0]*p2[1]+(p2[1]-p0[1])*point[0]+(p0[0]-p2[0])*point[1]
		t = p0[0]*p1[1]-p0[1]*p1[0]+(p0[1]-p1[1])*point[0]+(p1[0]-p0[0])*point[1]
		if ((s<0) != (t<0)):
			return False

		A = -p1[1]*p2[0]+p0[1]*(p2[0]-p1[0])+p0[0]*(p1[1]-p2[1])+p1[0]*p2[1]
		if A < 0.0:
			s = -s
			t = -t
			A = -A
		return s > 0 and t > 0 and s+t <= A

	def inside_polygon(self,point, poly, center):
		inside = False
		count = 0
		p1 = poly[-1]
		for i in range(0,len(poly)):
			p2 = poly[i]
			if self.inside_triangle(point,center,p1,p2):
				return True
			p1 = p2
		return False
		

	def main_loop(self):
		for i in range(0,random.randint(MIN_ASTEROIDS,MAX_ASTEROIDS)):
			self.asteroids.append(self.get_new_asteroid())

		while not self.exit:
			for event in pygame.event.get():
				self.event(event)

			if self.reset:
				self.poship=[self.w/2,self.h/2,0]
				self.vel=[0,0]
				self.asteroids=[]
				self.reset=False
				self.collision=False
				for i in range(0,random.randint(MIN_ASTEROIDS,MAX_ASTEROIDS)):
					self.asteroids.append(self.get_new_asteroid())

			if self.pause:
				self.screen.blit(self.font.render("Pause",True,self.WHITE),(self.w/2,self.h/3))
				pygame.display.flip()
				continue

			if self.spawn:
				self.asteroids.append(self.get_new_asteroid())
				#self.spawn = False

			if self.U_P:
				direction=[0,0]
				direction[0] = math.cos(self.poship[2])/50
				direction[1] = math.sin(self.poship[2])/50
				self.vel[0] = self.vel[0] + direction[0]
				self.vel[1] = self.vel[1] + direction[1]
			else:
				self.vel[0] = self.vel[0]/1.03
				self.vel[1] = self.vel[1]/1.03
			if self.L_P:
				self.poship[2] = self.poship[2]-0.08
			if self.R_P:
				self.poship[2] = self.poship[2]+0.08
			if self.S_P:
				self.S_P = False
				shoot=[self.poship[0],self.poship[1],0,0]
				shoot[2] = math.cos(self.poship[2])
				shoot[3] = math.sin(self.poship[2])
				self.shoots.append(shoot)

			self.screen.fill(self.BLACK)

			dt = self.clock.get_time()
			#Update ship position
			self.poship[0] = self.poship[0] + self.vel[0]*dt
			self.poship[1] = self.poship[1] + self.vel[1]*dt
			#check limits
			self.poship[0:2],_ = self.check_limits([self.poship[0],self.poship[1]])
			shippoly = self.get_pol_ship(self.poship)

			#Update shoots pos
			for shoot in self.shoots:
				shoot[0] = shoot[0]+shoot[2]*dt
				shoot[1] = shoot[1]+shoot[3]*dt
				shoot[0:2],out = self.check_limits([shoot[0],shoot[1]])
				if out:
					self.shoots.remove(shoot)
					continue
				pygame.draw.rect(self.screen,self.WHITE,(shoot[0],shoot[1],2,2))

			#Update asteroid positions
			for asteroid in self.asteroids:
				astpos = asteroid[0]
				velast = asteroid[1]

				astpos[0] = astpos[0] + velast[0]*dt
				astpos[1] = astpos[1] + velast[1]*dt
				astposnew,out = self.check_limits(astpos)

				if out:
					change = [astposnew[0]-astpos[0],astposnew[1]-astpos[1]]
					for pos in asteroid[2:]:
						pos[0] = pos[0]+change[0]
						pos[1] = pos[1]+change[1]
				else:
					for pos in asteroid[2:]:
						pos[0] = pos[0] + velast[0]*dt
						pos[1] = pos[1] + velast[1]*dt
				asteroid[0] = astposnew
				pygame.draw.polygon(self.screen,self.WHITE,asteroid[2:],2)
				for shoot in self.shoots:
					if self.inside_polygon(shoot[0:2],asteroid[2:],asteroid[0]):
							self.asteroids.remove(asteroid)
							self.shoots.remove(shoot)
				for vertex in shippoly:
					if self.inside_polygon(vertex,asteroid[2:],asteroid[0]):
						self.collision = True

			if not self.collision:
				pygame.draw.polygon(self.screen,self.WHITE,self.get_pol_ship(self.poship))
			else:
				self.screen.blit(self.font.render("GAME OVER",True,self.WHITE),(self.w/2.5,self.h/3))
			#Update screen
			self.clock.tick(60)
			pygame.display.flip()
			pygame.display.set_caption("fps: " + str(round(self.clock.get_fps())))

def main():
	game = Asteroids()
	game.main_loop()

if __name__ == "__main__":
	main()
