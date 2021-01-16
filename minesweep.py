import sys, pygame, math, numpy, random
pygame.init()

### ------------ Gameplay Matrix Legend-------------------- ###
# Within the gameplay matrix, each cell may be surrounded by 
# 0-8 mines the number of mines surrounding a given cell is 
# encoded in the gameplay matrix accordingly (0 = no mines in 
# surrounding cells, 4 = 4 mines in surrounding cells..)
# 
# A 9 in the gameplay matrix represents a mine 
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

# Initialize grids 
mines_grid = [[0 for y in range(usr_grid_y)] for x in range(usr_grid_x)]
flags_grid = [[0 for y in range(usr_grid_y)] for x in range(usr_grid_x)]

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

	adj = [0, 0, 0, 0, 0, 0, 0, 0] # TL, T, TR, ML, MR, BL, B, BR

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

	counter = 0
	for x in adj:
		if x == 9:
			counter +=1
	return(counter)

for y in range(usr_grid_y):
	for x in range(usr_grid_x):
		if mines_grid[x][y] != 9:
			mines_grid[x][y] = get_adj([x,y], mines_grid, usr_grid_x, usr_grid_y)

print(mines_grid)

# Initialize window size
cell_x = 35
cell_y = 35
margin = 5

grid_x = (cell_x*usr_grid_x)+(margin*usr_grid_x)+(margin*2)
grid_y = (cell_y*usr_grid_y)+(margin*usr_grid_y)+(margin*2)
grid_size = grid_x, grid_y 
screen = pygame.display.set_mode(grid_size)



pygame.display.set_caption("Minesweeper")
 
# Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()
 
# -------- Main Program Loop -----------
while not done:
	# --- Main event loop
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
 
	# --- Game logic should go here
 
	# --- Screen-clearing code goes here
 
	# Here, we clear the screen to white. Don't put other drawing commands
	# above this, or they will be erased with this command.
 

	screen.fill(black)
 
	# --- Drawing code should go here
	for y in range(usr_grid_y):
		for x in range(usr_grid_x):
				color = white
				if mines_grid[x][y]==9:
					color = red
				if mines_grid[x][y]==10:
					color = black
				pygame.draw.rect(screen, color, [(margin+cell_x)*x+margin, (margin+cell_y)*y+margin, cell_x, cell_y ])

 
	# --- Go ahead and update the screen with what we've drawn.
	pygame.display.flip()

	# --- Limit to 60 frames per second
	clock.tick(60)
 
# Close the window and quit.
pygame.quit()

