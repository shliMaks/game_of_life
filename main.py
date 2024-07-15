import pygame
import sys
import random
from game_of_life import game
from time import time

pygame.init()

# screen resolution
info = pygame.display.Info()
width, height = info.current_w, info.current_h - 50
screen = pygame.display.set_mode((width, height))
display_surface = pygame.display.get_surface()

# colors
black = (0, 0, 0)
white = (255, 255, 255)
grey =  (170, 170, 170)

# fps clock
clock = pygame.time.Clock()
FPS = 120

# size
cell_size = 20
inbetween_dist = 1
min_size = 6

# calculate resolution of cells grid
width_cells_amount = (width * 3)//(cell_size + inbetween_dist)
height_cells_amount = (height * 3)//(cell_size + inbetween_dist)

# create cells
probability_of_one = 0.0

def generate_cells(prob_of_one=0.5):
    cells = [[random.choices([0, 1], [1 - prob_of_one, prob_of_one])[0] for i in range(width_cells_amount)] for i in range(height_cells_amount)]

    # add layer to cells
    cells[0] = [2 for i in range(width_cells_amount)]
    cells[-1] = [2 for i in range(width_cells_amount)]
    for i in range(len(cells)):
        cells[i][0] = 2
        cells[i][-1] = 2
    
    return cells

# creating cells grid
cells = generate_cells(probability_of_one)
last_cells = [[[0 for i in range(width_cells_amount)] for i in range(height_cells_amount)] for i in range(20)]


# offset
prev_mouse_pos = pygame.mouse.get_pos()
# offset = list(prev_mouse_pos)
offset = [width // 2 + prev_mouse_pos[0], height // 2 + prev_mouse_pos[1]]

wait = 0
generation = 0
game_is_stopped = False
pause1 = time()
pause2 = time()
button_down = False

# buttons rectangles
pause_rect_cords = [width - 85, 20, 70, 70]
pause_rect = pygame.Rect(*pause_rect_cords)

continue_rect_cords = [width - 175, 20, 70, 70]
continue_rect = pygame.Rect(*continue_rect_cords)

clear_rect_cords = [width - 175, 107, 160, 50]
clear_rect = pygame.Rect(*clear_rect_cords)

generate_rect_cords = [width - 175, 174, 160, 50]
generate_rect = pygame.Rect(*generate_rect_cords)


# font
game_font = pygame.font.Font(None, 50)

# main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    screen.fill(black)

    if not game_is_stopped:
        cells = game(cells)
        generation += 1   

        # update cells list
        last_cells.pop(0)
        last_cells.append(cells)


    # if any of the buttons got clicked
    if event.type == pygame.MOUSEBUTTONDOWN and time() - pause1 > 0.2:
        mouse_pos = event.pos
        if pause_rect.collidepoint(mouse_pos):
            game_is_stopped = True

        elif continue_rect.collidepoint(mouse_pos):
            game_is_stopped = False
        
        elif clear_rect.collidepoint(mouse_pos):
            cells = generate_cells(0.0)
            for _ in range(2):
                cells = game(cells)

        elif generate_rect.collidepoint(mouse_pos):
            cells = generate_cells(0.5)
            cells = game(cells)

        else:
            button_down = not button_down

        pause1 = time()
        
    # move through the screen with mouse
    if event.type == pygame.MOUSEMOTION:
        current_mouse_pos = pygame.mouse.get_pos()
        for i in range(2):
            offset[i] += (current_mouse_pos[i] - prev_mouse_pos[i])
        prev_mouse_pos = current_mouse_pos

    # drawing cells
    if button_down:
        row = (offset[1] + mouse_pos[1]) // (cell_size + 1)
        column = (offset[0] + mouse_pos[0]) // (cell_size + 1)
        cells[row][column] = 1

    # start/stop the game
    if keys[pygame.K_SPACE] and time() - pause2 > 0.2:
        game_is_stopped = not game_is_stopped
        pause2 = time()


    # changing scale
    if keys[pygame.K_w]: # scale up
        cell_size += 1
        offset[0] += (width_cells_amount // 2) + (pygame.mouse.get_pos()[0] - width // 2) // 5
        offset[1] += (height_cells_amount // 2) + (pygame.mouse.get_pos()[1] - height // 2) // 5
        wait = 2

    elif keys[pygame.K_s] and cell_size >= min_size: # scale down
        cell_size -= 1
        offset[0] -= (width_cells_amount // 2) + (pygame.mouse.get_pos()[0] - width // 2) // 5
        offset[1] -= (height_cells_amount // 2) + (pygame.mouse.get_pos()[1] - height // 2) // 5
        wait = 2
        
    if wait:
        wait -= 1

    # drawing all cells
    for n, row in enumerate(cells):
        for n2, cell in enumerate(row):
            if cell == 1:
                pygame.draw.rect(screen, white, (n2 * (cell_size + inbetween_dist) - offset[0], n * (cell_size + inbetween_dist) - offset[1], cell_size, cell_size))
            if cell == 2:
                pygame.draw.rect(screen, grey, (n2 * (cell_size + inbetween_dist) - offset[0], n * (cell_size + inbetween_dist) - offset[1], cell_size, cell_size))

            make_blue = 0
            for list in last_cells:
                if list[n][n2] == 1:
                    make_blue += 1
                    streak = True
                else:
                    make_blue = 0
                    streak = False
    
            # add blue if cell is stable
            if make_blue >= len(last_cells):
                pygame.draw.rect(screen, (0, 0, 255), (n2 * (cell_size + inbetween_dist) - offset[0], n * (cell_size + inbetween_dist) - offset[1], cell_size, cell_size))
            elif make_blue > 1:
                color = 255 - make_blue * 12
                pygame.draw.rect(screen, (color, color, 255), (n2 * (cell_size + inbetween_dist) - offset[0], n * (cell_size + inbetween_dist) - offset[1], cell_size, cell_size))


    # generations
    generation_text = game_font.render(str(generation), True, 'grey')
    display_surface.blit(generation_text, (30, height - 80))

    # continue and stop buttons
    pygame.draw.rect(screen, grey, pause_rect)
    pygame.draw.rect(screen, white, (width - 69, 35, 14, 40))
    pygame.draw.rect(screen, white, (width - 45, 35, 14, 40))

    pygame.draw.rect(screen, grey, continue_rect)
    pygame.draw.polygon(screen, white, [(width - 158, 37), (width - 123, 54), (width - 158, 74)])

    pygame.draw.rect(screen, grey, clear_rect)
    clear_text = game_font.render("clear", True, 'white')
    display_surface.blit(clear_text, (width - 140, 113))

    pygame.draw.rect(screen, grey, generate_rect)
    generate_text = game_font.render("generate", True, 'white')
    display_surface.blit(generate_text, (width - 169, 180))


    pygame.display.update()

    clock.tick(FPS)
    


