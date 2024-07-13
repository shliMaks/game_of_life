def game(cells):
    width, height = len(cells[0]), len(cells)
    cells2 = [[0 for i in range(width)] for i in range(height)]

    for n, row in enumerate(cells):
        for n2, cell in enumerate(row):
            neighbours = count_neightbours(cells, n2, n)
            if neighbours == 3 and cells[n][n2] == 0:
                cells2[n][n2] = 1
            if (neighbours == 2 or neighbours == 3) and cells[n][n2] == 1:
                cells2[n][n2] = 1

    return cells2

def count_neightbours(cells, x, y):
    neighbours = 0
    nearby_cells = [[x-1, y-1], [x, y-1], [x+1, y-1], [x+1, y], [x+1, y+1], [x, y+1], [x-1, y+1], [x-1, y]]
    for x, y in nearby_cells:
        if -1 < x < len(cells[0]) and -1 < y < len(cells):
            if cells[y][x] != 0:

                neighbours += 1

    return neighbours

