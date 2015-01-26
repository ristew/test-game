import sys, pygame
from pygame.locals import *
pygame.init()

size = width, height = 640, 480
speed = [0, 0]
black = 0, 0, 0

screen = pygame.display.set_mode(size)

ball = pygame.image.load("ball.bmp")
ballrect = ball.get_rect()

while 1:
	for event in pygame.event.get():
		speed = [0, 0]
		if event.type == pygame.QUIT: sys.exit()
		elif event.type == KEYDOWN: 
			if event.key == K_UP:
				speed = [0, -10]

			if event.key == K_DOWN:
				speed = [0, 10]

			if event.key == K_RIGHT:
				speed = [10, 0]

			if event.key == K_LEFT:
				speed = [-10, 0]

	ballrect = ballrect.move(speed)
	if ballrect.left < 0 or ballrect.right > width:
		if ballrect.left < 0:
			ballrect.left = 0
		
		if ballrect.right > width:
			ballrect.right = width

	if ballrect.top < 0 or ballrect.bottom > height:
		if ballrect.top < 0:
			ballrect.top = 0
		
		if ballrect.bottom > height:
			ballrect.bottom = height

	screen.fill(black)
	screen.blit(ball, ballrect)
	pygame.display.flip()
	pygame.time.delay(60)
