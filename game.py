import pygame
import random
pygame.init()

file = open("settings.txt", "r")
file_lines = file.readlines()
for i in range(len(file_lines)):
	try:
		file_lines[i] = int("".join(file_lines[i][:-1]).lower())
	except:
		pass

grid_width = file_lines[1]
grid_height = file_lines[4]
box_size = file_lines[7]
color_amount = file_lines[10]

if color_amount > 13:
	color_amount = 13
elif color_amount < 2:
	color_amount = 2

moves = grid_width * grid_height // 100 * color_amount + color_amount
#                dark red      orange        yellow         green        dark blue    light purple    light blue      cyan           brown         light green      white      black			gold
color_options = [(180, 0, 0), (255, 60, 0), (230, 230, 0), (0, 140, 0), (0, 0, 255), (130, 60, 255), (50, 100, 255), (0, 200, 255), (80, 30, 15), (128, 255, 128), (0, 0, 0), (255, 255, 255), (210, 130, 50)]
color_options = color_options[:color_amount]

"""
new_colors = []
for i in range(color_amount):
	num = random.randint(0, len(color_options) - 1)
	new_colors.append(color_options[num])
	color_options.pop(num)

color_options = new_colors
"""

screen_width = grid_width * box_size
screen_height = grid_height * box_size + 100

win = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
pygame.display.set_caption("Flood It")

class Square(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.color = random.choice(color_options)

	# to draw the certain box
	def draw(self):
		pygame.draw.rect(win, self.color, (self.x, self.y, box_size, box_size))


def change_surround(x, y, color):
	if x > 0:
		if grid[x-1][y].color == color and (x - 1, y) not in set_colors:
			set_colors.append((x-1, y))
	if x < grid_width - 1:
		if grid[x+1][y].color == color and (x + 1, y) not in set_colors:
			set_colors.append((x+1, y))
	if y > 0:
		if grid[x][y-1].color == color and (x, y - 1) not in set_colors:
			set_colors.append((x, y-1))
	if y < grid_height - 1:
		if grid[x][y+1].color == color and (x, y + 1) not in set_colors:
			set_colors.append((x, y+1))


def move(x, y, first=False):
	global old_color, moves
	old_color = grid[0][0].color
	color = grid[x][y].color
	if color != old_color or first:
		moves -= 1
		for pos in set_colors:
			grid[pos[0]][pos[1]].color = color
			change_surround(pos[0], pos[1], color)


def click(x, y):
	global moves
	for i, row in enumerate(grid):
		for j, box in enumerate(row):
			if x > box.x and x < box.x + box_size:
				if y > box.y and y < box.y + box_size:
					move(i, j)

def text_objects(text, font):
	textSurface = font.render(text, True, (255, 255, 255))
	return textSurface, textSurface.get_rect()

def display_score(text):
	largeText = pygame.font.Font('freesansbold.ttf', 60)
	TextSurf, TextRect = text_objects(text, largeText)
	TextRect.center = (round(screen_width * 0.5), 50)
	win.blit(TextSurf, TextRect)


def redraw_window():
	win.fill((0, 0, 0))

	for x in grid:
		for y in x:
			y.draw()

	display_score(f" {str(moves)} moves left.   {str(int(len(set_colors) / (grid_width * grid_height) * 100))}% completed.")

	pygame.display.update()


grid = []
set_colors = [(0, 0)]
for i in range(grid_width):
	grid.append([])
	for j in range(grid_height):
		grid[i].append(Square(i * box_size, j * box_size + 100))

move(0, 0, True)
run = True
while run:
	clock.tick(60)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.MOUSEBUTTONUP:
			if moves > 0 and (len(set_colors) / (grid_width * grid_height) * 100) != 100:
				click(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

	keys = pygame.key.get_pressed()

	redraw_window()


pygame.quit()
