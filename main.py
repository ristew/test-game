import sys, pygame
from pygame.locals import *
pygame.init()

size = width, height = 640, 480
speed = [0.0, 0.0]
bgcolor = 200, 200, 50
keypressed = [0, 0, 0, 0]

screen = pygame.display.set_mode(size)

ball = pygame.image.load("ball.bmp")
ballrect = ball.get_rect()

while 1:
	if keypressed[2] == 0 and keypressed[3] == 0:
		speed[0] = (speed[0] + 0.5) / 2
	if keypressed[0] == 0 and keypressed[1] == 0:
		speed[1] = (speed[1] + 0.5) / 2
	for event in pygame.event.get():
		if event.type == QUIT: sys.exit()
		elif event.type == KEYDOWN: 
			if event.key == K_UP:
				speed[1] = -8
				keypressed[0] = 1

			if event.key == K_DOWN:
				speed[1] = 8
				keypressed[1] = 1

			if event.key == K_RIGHT:
				speed[0] = 8
				keypressed[2] = 1

			if event.key == K_LEFT:
				speed[0] = -8
				keypressed[3] = 1
				
		elif event.type == KEYUP:
			if event.key == K_UP:
				keypressed[0] = 0

			if event.key == K_DOWN:
				keypressed[1] = 0

			if event.key == K_RIGHT:
				keypressed[2] = 0

			if event.key == K_LEFT:
				keypressed[3] = 0 

	pygame.event.clear()
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

	screen.fill(bgcolor)
	screen.blit(ball, ballrect)
	pygame.display.flip()
	pygame.time.delay(60)
