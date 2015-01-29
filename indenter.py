f = open('main.py', 'r')
w = open('game.py', 'w')
for line in f:
	w.write('	')
	w.write(line)
