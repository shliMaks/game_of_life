import pygame
import sys
import random
from game_of_life import game
import time

pygame.init()

# screen resolution
info = pygame.display.Info()
width, height = info.current_w, info.current_h - 50
screen = pygame.display.set_mode((width, height))

# colors
black = (0, 0, 0)
white = (255, 255, 255)

# fps clock
clock = pygame.time.Clock()
FPS = 60

# size
cell_size = 20
inbetween_dist = 1

# genetare random cells
width_cells_amount = (width)//(cell_size + inbetween_dist) * 2
height_cells_amount = (height)//(cell_size + inbetween_dist) * 2

# create cells
probabilities_of_one = 0.6
cells = [[random.choices([0, 1], [1 - probabilities_of_one, probabilities_of_one])[0] for i in range(width_cells_amount)] for i in range(height_cells_amount)]
last_cells = [[[0 for i in range(width_cells_amount)] for i in range(height_cells_amount)] for i in range(20)]

# offset
prev_mouse_pos = pygame.mouse.get_pos()
offset = list(prev_mouse_pos)
# offset = [width // 2 + prev_mouse_pos[0], height // 2 + prev_mouse_pos[1]]

wait = 0

# main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    start = time.time()

    screen.fill(black)
    cells = game(cells)

    if event.type == pygame.MOUSEMOTION:
        current_mouse_pos = pygame.mouse.get_pos()
        for i in range(2):
            offset[i] += (current_mouse_pos[i] - prev_mouse_pos[i])
        prev_mouse_pos = current_mouse_pos

    if event.type == pygame.MOUSEWHEEL:
        if event.y > 0:
            cell_size += event.y
            offset[0] += width_cells_amount // 2 * event.y
            offset[1] += height_cells_amount // 2 * event.y
            wait = 2

        elif event.y < 0 and not wait:
            if cell_size > 10:
                cell_size += event.y
                offset[0] += width_cells_amount // 2 * event.y
                offset[1] += height_cells_amount // 2 * event.y
                wait = 2
            
    if wait:
        wait -= 1
        
            

        
            

    for n, row in enumerate(cells):
        for n2, cell in enumerate(row):
            if cell == 1:
                pygame.draw.rect(screen, white, (n2 * (cell_size + inbetween_dist) - offset[0], n * (cell_size + inbetween_dist) - offset[1], cell_size, cell_size))

            make_blue = 0
            for list in last_cells:
                if list[n][n2] == 1:
                    make_blue += 1
                    streak = True
                else:
                    make_blue = 0
                    streak = False
      
            if make_blue >= len(last_cells):
                pygame.draw.rect(screen, (0, 0, 255), (n2 * (cell_size + inbetween_dist) - offset[0], n * (cell_size + inbetween_dist) - offset[1], cell_size, cell_size))
            elif make_blue > 1:
                color = 255 - make_blue * 12
                pygame.draw.rect(screen, (color, color, 255), (n2 * (cell_size + inbetween_dist) - offset[0], n * (cell_size + inbetween_dist) - offset[1], cell_size, cell_size))
    
    last_cells.pop(0)
    last_cells.append(cells)
    
    pygame.display.update()

    clock.tick(FPS)



