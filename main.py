import sys, pygame, level, random, copy
from pygame.locals import *
from collections import deque
pygame.init()
pygame.display.set_caption("real virtual mcgill")


shift = 0
size = width, height = 640, 480
speed = [0.0, 0.0]
bgcolor = 0, 0, 0
keypressed = [0, 0, 0, 0]

screen = pygame.display.set_mode(size)
tilesize = 32
serie = 0
w = width / tilesize
m = []
mrows = []
rows = []
rows.append([1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0])
rows.append([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2])
rows.append([1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0])
rows.append([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 2])
skytile = pygame.image.load("sky.bmp").convert()
groundtile = pygame.image.load("ground.bmp").convert()
firetile = pygame.image.load("fire.bmp").convert()
random.seed()
lastx = 0

def addrow(lastrow):
	global serie
	prb = random.randint(0, 10)
	if lastrow == 0:
		if prb > 5:
			mrows.append(0)
			return copy.copy(rows[0])
		elif prb > 3:
			mrows.append(1)
			return copy.copy(rows[1])
		else:
			mrows.append(2)
			return copy.copy(rows[2])
	if lastrow == 1:
		if prb > 7 + serie:
			mrows.append(1)
			serie += 1
			return copy.copy(rows[1])
		elif prb > 4:
			serie = 0
			mrows.append(3)
			return copy.copy(rows[3])
		else:
			mrows.append(0)
			serie = 0
			return copy.copy(rows[0])
	if lastrow == 2:
		if prb > 6:
			mrows.append(1)
			return copy.copy(rows[1])
		elif prb > 3:
			mrows.append(2)
			return copy.copy(rows[2])
		else:
			mrows.append(0)
			return copy.copy(rows[0])
	elif lastrow == 3:
		if prb > 5:
			mrows.append(3)
			return copy.copy(rows[3])
		else:
			mrows.append(1)
			return copy.copy(rows[1])
	else:
		mrows.append(0)
		return copy.copy(rows[0])

def shiftright():
	m.append(addrow(mrows[-1]))
	m.pop(0)

def initlevel(width):
	serie = 0
	w = width
	for i in range(width):
		m.append(copy.copy(rows[0]))
		mrows.append(0)

ball = pygame.image.load("ball.bmp")
ballrect = ball.get_rect()
ballrect.left = 20

lost = False

def lose():
	global lost
	lost = True
	
def getcollide():
	thisrowcent = ballrect.centerx / tilesize
	thisrowright = (ballrect.right - 4) / tilesize
	thisrowleft = (ballrect.left + 4) / tilesize
	thisheight = ballrect.bottom / tilesize
	centrow = m[thisrowcent]
	rightrow = m[thisrowright]
	leftrow = m[thisrowleft]
	if thisheight > 13:
		lose()
	if m[thisrowright][thisheight] == 0 or m[thisrowleft][thisheight] == 0 or m[thisrowcent][thisheight] == 0:
		speed[1] = 0
		return True
	else:
		return False

def getcollideside():
	thisrowright = ballrect.right / tilesize
	thisrowleft = ballrect.left / tilesize
	thisheight = ballrect.centery / tilesize
	if m[thisrowright][thisheight] == 0 and speed[0] > 0 or m[thisrowleft][thisheight] == 0 and speed[0] < 0:
		speed[0] = 0


initlevel(w)

m[10][10] = 1

def renderlevel():
	x, y = 0, 0
	for i in range(len(m)):
		for j in range(len(m[i])):
			if m[i][j] == 0:
				screen.blit(groundtile, (x, y))
			elif m[i][j] == 1:
				screen.blit(skytile, (x, y))
			elif m[i][j] == 2:
				screen.blit(firetile, (x, y))
			y += tilesize
		x += tilesize
		y = 0
	if lost == True:
		pygame.font.init()
		font = pygame.font.SysFont(u'nanumgothic', 36)
		screen.blit(font.render("hail satan", 0, (0, 0, 0)), (200, 40))

while lost == False:
	col = getcollide()
	if col == True:
		if keypressed[1] == 0 and keypressed[2] == 0:
			speed[0] = (speed[0] + 0.5) / 2
		if keypressed[0] == 1: speed[1] = -16
		if keypressed[1] == 1: speed[0] = 8
		if keypressed[2] == 1: speed[0] = -8
	else:
		if keypressed[1] == 1 and speed[0] < 4:
			speed[0] += 2
		if keypressed[2] == 1 and speed[0] > -4:
			speed[0] -= 2
		if speed[1] < 16:
			speed[1] += 2
			
	for event in pygame.event.get():
		if event.type == QUIT: sys.exit()
		elif event.type == KEYDOWN: 
			if event.key == K_UP:
				keypressed[0] = 1

			if event.key == K_RIGHT:
				keypressed[1] = 1

			if event.key == K_LEFT:
				keypressed[2] = 1
				
		elif event.type == KEYUP:
			if event.key == K_UP:
				keypressed[0] = 0

			if event.key == K_RIGHT:
				keypressed[1] = 0

			if event.key == K_LEFT:
				keypressed[2] = 0 
			
	getcollideside()
	ballrect = ballrect.move(speed)
	if ballrect.left < 0 or ballrect.right > width:
		if ballrect.left < 0:
			ballrect.left = 0
		
		if ballrect.right > width:
			ballrect.right = width

	if ballrect.bottom < 0 or ballrect.bottom > height:
		if ballrect.top < 0:
			ballrect.top = 0
		
		if ballrect.bottom > height:
			ballrect.bottom = height
	if ballrect.right > 4 * width / 5:
		shift = 1
	elif ballrect.right < 1 * width / 5:
		shift = 0
	if shift == 1:
		m.append(addrow(mrows[-1]))
		m.pop(0)
		ballrect.left -= tilesize
	renderlevel();	
	screen.blit(ball, ballrect)
	pygame.display.flip()
	pygame.time.delay(60)

while 1:
	for event in pygame.event.get():
		if event.type == QUIT: sys.exit()
