import sys, pygame, random, copy, math
from pygame.locals import *
from collections import deque

sri = 0

def game(sizex, sizey):
	ticks = 0
	global lost
	pygame.init()
	pygame.display.set_caption("real virtual mcgill")
	score = 0
	shift = 0
	size = width, height = sizex, sizey
	speed = [0.0, 0.0]
	bgcolor = 0, 0, 0
	keypressed = [0, 0, 0, 0]
	
	screen = pygame.display.set_mode(size)
	tilesize = 32
	serie = 0
	h = height / tilesize
	w = width / tilesize
	m = []
	mrows = []
	rows = []
	skyrow = []
	for i in range(h - 7):
		skyrow.append(1)
	rows.append(skyrow + [1, 0, 0, 0, 0, 0, 0])
	rows.append(skyrow + [1, 1, 1, 1, 1, 1, 2])
	rows.append(skyrow + [0, 0, 0, 0, 0, 0, 0])
	rows.append(skyrow + [1, 1, 0, 1, 1, 1, 2])
	skytile = pygame.image.load("sky.bmp").convert()
	groundtile = pygame.image.load("ground.bmp").convert()
	firetile = pygame.image.load("fire.bmp").convert()
	random.seed()
	lastx = 0
	
	def addrow(lastrow, serie):
		global sri
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
			sri += 1
			if prb > 6 + sri:
				mrows.append(1)
				return copy.copy(rows[1])
			elif prb > 4:
				mrows.append(3)
				sri = 0
				return copy.copy(rows[3])
			else:
				mrows.append(0)
				sri = 0
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
		m.append(addrow(mrows[-1], serie))
		m.pop(0)
	
	def initlevel(width):
		serie = 0
		w = width
		for i in range(width):
			m.append(copy.copy(rows[0]))
			mrows.append(0)
	
	guy = pygame.image.load("guy.png")
	guyrect = guy.get_rect()
	guyrect.left = 20
	
	lost = False
	
		
	def getcollide():
		thisrowcent = guyrect.centerx / tilesize
		thisrowright = (guyrect.right - 12) / tilesize
		thisrowleft = (guyrect.left + 12) / tilesize
		thisheight = guyrect.bottom / tilesize
		centrow = m[thisrowcent]
		rightrow = m[thisrowright]
		leftrow = m[thisrowleft]
		if m[thisrowright][thisheight] == 0 or m[thisrowleft][thisheight] == 0 or m[thisrowcent][thisheight] == 0:
			speed[1] = 0
			return True
		else:
			return False
	def getlose():
		if guyrect.bottom / tilesize == h - 1:
			return True
		return False
	
	def getcollideside():
		thisrowright = (guyrect.right - 8) / tilesize
		thisrowleft = (guyrect.left + 8) / tilesize
		thisheight = guyrect.centery / tilesize
		if m[thisrowright][thisheight] == 0 and speed[0] > 0 or m[thisrowleft][thisheight] == 0 and speed[0] < 0:
			speed[0] = 0
	
	pygame.font.init()
	font = pygame.font.SysFont(u'freemono', 36)
	initlevel(w)
	back = False
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
		screen.blit(font.render("score: " + str(score), 0, (255, 0, 0)), (400, 20))
		
		screen.blit(guy, guyrect)
		if getlose() == True:
			screen.blit(font.render("no more red table", 0, (255, 0, 0)), (200, 50))
			pygame.time.delay(200)
			screen.blit(font.render("press f to play again", 0, (255, 0, 0)), (110, 80))
	
	while getlose() == False:
		col = getcollide()
		if col == True:
			if keypressed[1] == 0 and keypressed[2] == 0:
				speed[0] = (speed[0] + 0.5) / 2
			if keypressed[1] == 1: speed[0] = 10
			if keypressed[2] == 1: speed[0] = -10
		else:
			if keypressed[1] == 1 and speed[0] < 5:
				speed[0] += 2
			if keypressed[2] == 1 and speed[0] > -5:
				speed[0] -= 2
			if speed[1] < 16:
				speed[1] += 2
				
		if speed[0] < 0:
			back = True
		elif speed[0] > 0:
			back = False
		if math.fabs(speed[0]) > 0.99:
			if ticks % 10 < 5 or col == False:	
				guy = pygame.transform.flip(pygame.image.load("run1.png"), back, False)
			else:
				guy = pygame.transform.flip(pygame.image.load("run2.png"), back, False)
			ticks += 1
		else:
			guy = pygame.transform.flip(pygame.image.load("guy.png"), back, False)
			
		for event in pygame.event.get():
			if event.type == QUIT: quit = 0#sys.exit()
			elif event.type == KEYDOWN: 
				if event.key == K_UP:
					if keypressed [0] == 0 and col == True:
						speed[1] = -16
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
		guyrect = guyrect.move(speed)
		if guyrect.left < 0 or guyrect.right > width:
			if guyrect.left < 0:
				guyrect.left = 0
			
			if guyrect.right > width:
				guyrect.right = width
	
		if guyrect.bottom < 0 or guyrect.bottom > height:
			if guyrect.top < 0:
				guyrect.top = 0
			
			if guyrect.bottom > height:
				guyrect.bottom = height
		if guyrect.right > 4 * width / 5:
			shift = 1
			score += 1
		elif guyrect.right < 1 * width / 5:
			shift = 0
		if shift == 1:
			m.append(addrow(mrows[-1], serie))
			m.pop(0)
			guyrect.left -= tilesize
		renderlevel();	
		pygame.display.flip()
		pygame.time.delay(60)
	
	while 1:
		pygame.time.delay(30)
		for event in pygame.event.get():
			if event.type == KEYDOWN:
				if event.key == K_f:
					return 1
