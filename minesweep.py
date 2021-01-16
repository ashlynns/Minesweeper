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

usr_grid_y = int(input("Grid height: ")) # x-axis == grid height
usr_grid_x = int(input("Grid width: ")) # y-axis == grid width 
mines_pct = int(input("Percentage of mines: "))
'''

usr_grid_y = 6
usr_grid_x = 5
mines_pct = 20
'''
number_of_cells = usr_grid_height*usr_grid_width
mines_num = math.ceil(number_of_cells*(mines_pct/100))

print("Your minesweeper game has {} cells, and {} mines".format(number_of_cells, mines_num))

# colors 
black = (0,0,0)
white = (255,255,255)
red = (255, 0, 0)

# Initialize grid 
mines_grid = [[0 for x in range(usr_grid_width)] for y in range(usr_grid_height)]
flags_grid = [[0 for x in range(usr_grid_width)] for y in range(usr_grid_height)]

# place mines 
indices = [(m,n) for m in range(usr_grid_width) for n in range(usr_grid_height)]
mine_idx = random.sample(indices, mines_num)

print(mine_idx)

for mine in mine_idx:
	width = mine[0]
	height = mine[1]
	
	mines_grid[height][width] = 9

def get_adj(idx, grid):
	x = idx[0] 
	y = idx[1]

	adj = []
	adj.append(grid[x-1][y-1]) #top left
	adj.append(grid[x][y-1]) #top
	adj.append(grid[x+1][y-1]) #top right 

	adj.append(grid[x-1][y]) #middle left
	adj.append(grid[x+1][y]) #middle right

	adj.append(grid[x-1][y+1]) #bottom left
	adj.append(grid[x][y+1]) #bottom

	adj.append(grid[x+1][y+1]) #bottom right

	counter = 0

	for x in adj:
		if x == 9:
			print(x)
			counter +=1

	print(counter)
	return(counter)

print(mines_grid)
print(mines_grid[1])
test = get_adj([2,3], mines_grid)
print(mines_grid[2][3])
mines_grid[2][3] = 10

# Initialize window size
cell_height = 35
cell_width = 35
margin = 5

grid_width = (cell_width*usr_grid_width)+(margin*usr_grid_width)+(margin*2)
grid_height = (cell_height*usr_grid_height)+(margin*usr_grid_height)+(margin*2)
grid_size = grid_width, grid_height 
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
	for row in range(usr_grid_height):
		for column in range(usr_grid_width):
				color = white
				if mines_grid[row][column]==9:
					color = red
				if mines_grid[row][column]==10:
					color = black
				pygame.draw.rect(screen, color, [(margin+cell_width)*column+margin, (margin+cell_height)*row+margin, cell_width, cell_height ])


 
	# --- Go ahead and update the screen with what we've drawn.
	pygame.display.flip()

	# --- Limit to 60 frames per second
	clock.tick(60)
 
# Close the window and quit.
pygame.quit()

