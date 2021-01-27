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

usr_grid_x = int(input("Grid Width (max 40): ")) # x-axis == grid width 
if usr_grid_x > 40: 
	print("Grid width too large. Automatically set to max.")
	usr_grid_x = 40

usr_grid_y = int(input("Grid Height (max 20): ")) # y-axis == grid height
if  usr_grid_y > 20: 	
	print("Grid height too large. Automatically set to max.")
	usr_grid_y = 20

mines_pct = int(input("Percentage of Mines (min 10): "))
if mines_pct < 10: 
	print("Not enough mines. Automatically set to min.")
	mines_pct = 10	

'''

usr_grid_x = 10
usr_grid_y = 10
mines_pct = 20
'''
number_of_cells = usr_grid_x*usr_grid_y
mines_num = math.ceil(number_of_cells*(mines_pct/100))

print("Your minesweeper game has {} cells, and {} mines".format(number_of_cells, mines_num))

# Colors 
black = (0,0,0)
white = (255,255,255)
red = (255, 0, 0)
green = (0, 255, 0)


# Initialize window size
cell_x = 35
cell_y = 35
margin = 5


grid_x = (cell_x*usr_grid_x)+(margin*usr_grid_x)+(margin*2)
grid_y = (cell_y*usr_grid_y)+(margin*usr_grid_y)+(margin*2)
grid_size = grid_x, grid_y 
screen = pygame.display.set_mode(grid_size)


# Text numbers 
font = pygame.font.Font('freesansbold.ttf', 24)
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
		adj[0] = grid[x-1][y-1] #top left
		adj[1] = grid[x][y-1] #top
		adj[3] = grid[x-1][y] #middle left
		adj[5] = grid[x-1][y+1] #bottom left
		adj[6] = grid[x][y+1] #bottom

	else: 		
		adj[0] = grid[x-1][y-1] #top left
		adj[1] = grid[x][y-1] #top
		adj[2] = grid[x+1][y-1] #top right 

		adj[3] = grid[x-1][y] #middle left
		adj[4] = grid[x+1][y] #middle right

		adj[5] = grid[x-1][y+1] #bottom left
		adj[6] = grid[x][y+1] #bottom
		adj[7] = grid[x+1][y+1] #bottom right

	return(adj)

# Initialize grids 
'''
mines_grid = [[0 for y in range(usr_grid_y)] for x in range(usr_grid_x)]
flags_grid = [[12 for y in range(usr_grid_y)] for x in range(usr_grid_x)]
win_grid = [[0 for y in range(usr_grid_y)] for x in range(usr_grid_x)]
lose_grid = [[12 for y in range(usr_grid_y)] for x in range(usr_grid_x)]
'''
indices = [(x,y) for x in range(usr_grid_x) for y in range(usr_grid_y)]

def place_adj(pos_x, pos_y, mines_grid, win_grid, lose_grid): 
	indices.remove((pos_x, pos_y)) # makes sure first click isnt a mine 
	mine_idx = random.sample(indices, mines_num) # chooses mine indexes 
	for mine in mine_idx: 
		x = mine[0]
		y = mine[1]
		mines_grid[x][y] = 9 # places mines 
		lose_grid[x][y] = 9
		win_grid[x][y] = 10 

		for y in range(usr_grid_y): 
			for x in range(usr_grid_x):
				if mines_grid[x][y] != 9: 
					adj = get_adj([x,y], mines_grid, usr_grid_x, usr_grid_y)
					counter = 0 
					for i in adj: 
						if i ==9: 
							counter+=1
					mines_grid[x][y] = counter # fills remainder of the grid 	
					win_grid[x][y] = counter 
	return(mines_grid, win_grid, lose_grid)					

def adj_idx_map(idx, pos_x, pos_y): 
	if idx == 0: 
		return(pos_x-1, pos_y-1)
	elif idx == 1: 
		return(pos_x, pos_y-1)
	elif idx == 2: 
		return(pos_x+1, pos_y-1)
	elif idx == 3:
		return(pos_x-1, pos_y)
	elif idx == 4: 
		return(pos_x+1, pos_y)
	elif idx == 5: 
		return(pos_x-1, pos_y+1)
	elif idx == 6: 
		return(pos_x, pos_y+1)
	elif idx == 7:  
		return(pos_x+1, pos_y+1)

def open_adj(pos_x, pos_y, mines_grid, flags_grid, lose_grid):
	adj = get_adj([pos_x,pos_y], mines_grid, usr_grid_x, usr_grid_y)
	for idx, ad in enumerate(adj): 
		if ad != 11 and ad != 9: 
			idx_x, idx_y = adj_idx_map(idx, pos_x, pos_y)
			flags_grid[idx_x][idx_y] = ad
			lose_grid[idx_x][idx_y] = ad
			if ad == 0: 
				adj1 = get_adj([idx_x,idx_y], mines_grid, usr_grid_x, usr_grid_y)
				for idx1, ad1 in enumerate(adj1): 
					if ad1 != 11 and ad1 != 9: 
						idx_x1, idx_y1 = adj_idx_map(idx1, idx_x, idx_y)
						flags_grid[idx_x1][idx_y1] = ad1
						lose_grid[idx_x1][idx_y1] = ad1
	return(mines_grid, flags_grid, lose_grid)					

pygame.display.set_caption("Minesweeper")
 


 
# -------- Main Program Loop -----------
def play(grid_size):

	done = False # Loop until user clicks close button 
	lost = False # Loop until game is lost 
	click_count = 0 

	mines_grid = [[0 for y in range(usr_grid_y)] for x in range(usr_grid_x)]
	flags_grid = [[12 for y in range(usr_grid_y)] for x in range(usr_grid_x)]
	win_grid = [[0 for y in range(usr_grid_y)] for x in range(usr_grid_x)]
	lose_grid = [[12 for y in range(usr_grid_y)] for x in range(usr_grid_x)]

	clock = pygame.time.Clock()
	screen = pygame.display.set_mode(grid_size)
	while not done:
		for event in pygame.event.get(): # block ensures game can be closed once lost 
			if event.type == pygame.QUIT:
				done = True
			if event.type == pygame.KEYDOWN: 	
				if event.key == pygame.K_r: 
					play(grid_size)		
		while not lost: 
			# --- Main event loop
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					done = True
					lost = True
				if event.type == pygame.MOUSEBUTTONDOWN:
					pos = pygame.mouse.get_pos() # location of click 
					pos_x = pos[0]//(cell_x+margin) # Map location to index 
					pos_y = pos[1]//(cell_y+margin)
					if click_count == 0: # First click -- generates the locations of the mines 
						mines_grid, win_grid, lose_grid = place_adj(pos_x, pos_y, mines_grid, win_grid, lose_grid) # place adjacent values 
						mines_grid, flags_grid, lose_grid = open_adj(pos_x, pos_y, mines_grid, flags_grid, lose_grid)
						click_count +=1
						#print(mines_grid)

					if event.button == 1: # left click 
						if mines_grid[pos_x][pos_y] == 9: # clicked on a mine, game over
							# clicked on a mine and game over 
							screen.fill(red)
							flags_grid = lose_grid
							lost = True
						else:
							flags_grid[pos_x][pos_y] = mines_grid[pos_x][pos_y]
							lose_grid[pos_x][pos_y] = mines_grid[pos_x][pos_y]

					elif event.button == 3: # right click 
						flags_grid[pos_x][pos_y] = 10

					if flags_grid == win_grid: 
						screen.fill(green)
						lost = True


			# --- Drawing code
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
						lost = True
						gameover = font.render("Press R to Play Again", False, black, white)
						rect = gameover.get_rect()
						rect.center = screen.get_rect().center
						screen.blit(gameover, rect)

		 
			# --- Go ahead and update the screen with what we've drawn.
			pygame.display.flip()

			# --- Limit to 60 frames per second
			clock.tick(60)
	 
	# Close the window and quit.
	pygame.quit()

play(grid_size)
