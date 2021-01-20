import sys, pygame, math, numpy, random
pygame.init()

### ------------ Gameplay Matrix Legend-------------------- ###
# Within the gameplay matrix, each cell may be surrounded by 
# 0-8 mines the number of mines surrounding a given cell is 
# encoded in the gameplay matrix accordingly (0 = no mines in 
# surrounding cells, 4 = 4 mines in surrounding cells..)
# 
# A 9 in the gameplay matrix represents a mine 
# A 10 in the gameplay matrix represents a user placed flag 
### ------------------------------------------------------###


# User input game parameters
'''
usr_grid_x = int(input("Grid Width: ")) # x-axis == grid width 
usr_grid_y = int(input("Grid Height: ")) # y-axis == grid height
mines_pct = int(input("Percentage of Mines: "))
'''

usr_grid_x = 6
usr_grid_y = 5
mines_pct = 20

number_of_cells = usr_grid_x*usr_grid_y
mines_num = math.ceil(number_of_cells*(mines_pct/100))

print("Your minesweeper game has {} cells, and {} mines".format(number_of_cells, mines_num))

# Colors 
black = (0,0,0)
white = (255,255,255)
red = (255, 0, 0)
grey = (128, 128, 128)

# Initialize grids 
mines_grid = [[0 for y in range(usr_grid_y)] for x in range(usr_grid_x)]
flags_grid = [[12 for y in range(usr_grid_y)] for x in range(usr_grid_x)]

# Randomly place mines 
indices = [(x,y) for x in range(usr_grid_x) for y in range(usr_grid_y)]
mine_idx = random.sample(indices, mines_num)

for mine in mine_idx:
	x = mine[0]
	y = mine[1]
	
	mines_grid[x][y] = 9

def get_adj(idx, grid, x_len, y_len):
	x = idx[0] 
	y = idx[1]

	x_len = x_len -1 # get index rater than length 
	y_len = y_len -1 # get index rater than length

	adj = [11, 11, 11, 11, 11, 11, 11, 11] # TL, T, TR, ML, MR, BL, B, BR

	if x == 0:
		if y == 0:
			adj[4] = grid[x+1][y] #middle right
			adj[6] = grid[x][y+1] #bottom
			adj[7] = grid[x+1][y+1] #bottom right
		elif y == y_len: 
			adj[1] = grid[x][y-1] #top
			adj[2] = grid[x+1][y-1] #top right 
			adj[4] = grid[x+1][y] #middle right
		else: 
			adj[1] = grid[x][y-1] #top
			adj[2] = grid[x+1][y-1] #top right 
			adj[4] = grid[x+1][y] #middle right
			adj[6] = grid[x][y+1] #bottom
			adj[7] = grid[x+1][y+1] #bottom right
	
	elif y == 0: 
		if x == x_len:
			adj[3] = grid[x-1][y] #middle left
			adj[5] = grid[x-1][y+1] #bottom left
			adj[6] = grid[x][y+1] #bottom
		else:
			adj[3] = grid[x-1][y] #middle left
			adj[4] = grid[x+1][y] #middle right
			adj[5] = grid[x-1][y+1] #bottom left
			adj[6] = grid[x][y+1] #bottom
			adj[7] = grid[x+1][y+1] #bottom right
	
	elif y == y_len:
		if x == x_len: 
			adj[0] =grid[x-1][y-1] #top left
			adj[1] = grid[x][y-1] #top
			adj[3] = grid[x-1][y] #middle left
		else:
			adj[0] =grid[x-1][y-1] #top left
			adj[1] = grid[x][y-1] #top
			adj[2] = grid[x+1][y-1] #top right 

			adj[3] = grid[x-1][y] #middle left
			adj[4] = grid[x+1][y] #middle right
	
	elif x == x_len:
		adj[0] =grid[x-1][y-1] #top left
		adj[1] = grid[x][y-1] #top
		adj[3] = grid[x-1][y] #middle left
		adj[5] = grid[x-1][y+1] #bottom left
		adj[6] = grid[x][y+1] #bottom

	else: 		
		adj[0] =grid[x-1][y-1] #top left
		adj[1] = grid[x][y-1] #top
		adj[2] = grid[x+1][y-1] #top right 

		adj[3] = grid[x-1][y] #middle left
		adj[4] = grid[x+1][y] #middle right

		adj[5] = grid[x-1][y+1] #bottom left
		adj[6] = grid[x][y+1] #bottom
		adj[7] = grid[x+1][y+1] #bottom right

	#counter = 0
	#for x in adj:
	#	if x == 9:
	#		counter +=1
	return(adj)

for y in range(usr_grid_y): # Loop through all indces to get adj values 
	for x in range(usr_grid_x):
		if mines_grid[x][y] != 9: # dont overwrite the mines 
			adj = get_adj([x,y], mines_grid, usr_grid_x, usr_grid_y)
			counter = 0 
			for i in adj: 
				if i == 9: 
					counter +=1
			mines_grid[x][y] = counter
			#mines_grid[x][y] = get_adj([x,y], mines_grid, usr_grid_x, usr_grid_y)


# Initialize window size
cell_x = 35
cell_y = 35
margin = 5

grid_x = (cell_x*usr_grid_x)+(margin*usr_grid_x)+(margin*2)
grid_y = (cell_y*usr_grid_y)+(margin*usr_grid_y)+(margin*2)
grid_size = grid_x, grid_y 
screen = pygame.display.set_mode(grid_size)

# Text numbers 
font = pygame.font.Font('freesansbold.ttf', 22)
zero = font.render('0', True, black, white)
one = font.render('1', True, black, white)
two = font.render('2', True, black, white)
three = font.render('3', True, black, white)
four = font.render('4', True, black, white)
five = font.render('5', True, black, white)
six = font.render('6', True, black, white)
seven = font.render('7', True, black, white)
eight = font.render('8', True, black, white)
flag = font.render('!', True, black, white)
bomb = font.render('B', True, black, red)


pygame.display.set_caption("Minesweeper")
 
# Loop until the user clicks the close button.
#first click --> 
done = False
lost = False 
clock = pygame.time.Clock()
 
# -------- Main Program Loop -----------
while not done:
	for event in pygame.event.get(): # block ensures game can be closed once lost 
		if event.type == pygame.QUIT:
			done = True
	while not lost: 
		# --- Main event loop
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True
			if event.type == pygame.MOUSEBUTTONDOWN:
				pos = pygame.mouse.get_pos() # location of click 
				pos_x = pos[0]//(cell_x+margin) # Map location to index 
				pos_y = pos[1]//(cell_y+margin)
				if event.button == 1: # left click 
					if mines_grid[pos_x][pos_y] == 9:
						# clicked on a mine and game over 
						screen.fill(red)
						flags_grid[pos_x][pos_y] = mines_grid[pos_x][pos_y]
						lost = True
					else:
						flags_grid[pos_x][pos_y] = mines_grid[pos_x][pos_y]

				elif event.button == 3: # right click 
					flags_grid[pos_x][pos_y] = 10
	 
		# --- Drawing code should go here
		for y in range(usr_grid_y):
			for x in range(usr_grid_x):
				if flags_grid[x][y] != 9: 
					color = white
					pygame.draw.rect(screen, color, [(margin+cell_x)*x+margin, (margin+cell_y)*y+margin, cell_x, cell_y ])
					if flags_grid[x][y]==0:
						text_rect = zero.get_rect(center = ((margin+cell_x)*x+margin+(0.5*cell_x), (margin+cell_y)*y+margin+(0.5*cell_y) ))
						screen.blit(zero, text_rect)
					elif flags_grid[x][y]==1:
						text_rect = one.get_rect(center = ((margin+cell_x)*x+margin+(0.5*cell_x), (margin+cell_y)*y+margin+(0.5*cell_y) ))
						screen.blit(one, text_rect)
					elif flags_grid[x][y]==2:
						text_rect = two.get_rect(center = ((margin+cell_x)*x+margin+(0.5*cell_x), (margin+cell_y)*y+margin+(0.5*cell_y) ))
						screen.blit(two, text_rect)
					elif flags_grid[x][y]==3:
						text_rect = three.get_rect(center = ((margin+cell_x)*x+margin+(0.5*cell_x), (margin+cell_y)*y+margin+(0.5*cell_y) ))
						screen.blit(three, text_rect)
					elif flags_grid[x][y]==4:
						text_rect = four.get_rect(center = ((margin+cell_x)*x+margin+(0.5*cell_x), (margin+cell_y)*y+margin+(0.5*cell_y) ))
						screen.blit(four, text_rect)										
					elif flags_grid[x][y]==5:
						text_rect = five.get_rect(center = ((margin+cell_x)*x+margin+(0.5*cell_x), (margin+cell_y)*y+margin+(0.5*cell_y) ))
						screen.blit(five, text_rect)
					elif flags_grid[x][y]==6:
						text_rect = six.get_rect(center = ((margin+cell_x)*x+margin+(0.5*cell_x), (margin+cell_y)*y+margin+(0.5*cell_y) ))
						screen.blit(six, text_rect)
					elif flags_grid[x][y]==7:
						text_rect = seven.get_rect(center = ((margin+cell_x)*x+margin+(0.5*cell_x), (margin+cell_y)*y+margin+(0.5*cell_y) ))
						screen.blit(seven, text_rect)
					elif flags_grid[x][y]==8:
						text_rect = eight.get_rect(center = ((margin+cell_x)*x+margin+(0.5*cell_x), (margin+cell_y)*y+margin+(0.5*cell_y) ))
						screen.blit(eight, text_rect)
						#pygame.draw.rect(screen, red, [(margin+cell_x)*x+margin, (margin+cell_y)*y+margin, cell_x, cell_y ])
					elif flags_grid[x][y]==10:
						text_rect = flag.get_rect(center = ((margin+cell_x)*x+margin+(0.5*cell_x), (margin+cell_y)*y+margin+(0.5*cell_y) ))
						screen.blit(flag, text_rect)
				else: 
					text_rect = bomb.get_rect(center = ((margin+cell_x)*x+margin+(0.5*cell_x), (margin+cell_y)*y+margin+(0.5*cell_y) ))
					screen.blit(bomb, text_rect)

	 
		# --- Go ahead and update the screen with what we've drawn.
		pygame.display.flip()

		# --- Limit to 60 frames per second
		clock.tick(60)
	 
# Close the window and quit.
pygame.quit()

