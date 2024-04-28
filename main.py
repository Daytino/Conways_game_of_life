import pygame
from random import randrange


WIDTH, HEIGHT = 800, 800
FPS = 10
CELL_SIZE = 20
LINE_WIDTH = 1
GRID_WIDTH, GRID_HEIGHT = WIDTH // CELL_SIZE - 1, HEIGHT // CELL_SIZE - 1
print(GRID_WIDTH, GRID_HEIGHT)

# must-have
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game of Life")
clock = pygame.time.Clock()


positions_of_cells = set()

# цвета
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)
ORANGE = (255, 188, 54)
# --------------


def draw_lines():
    screen.fill(GRAY)
    for col in range(WIDTH // CELL_SIZE):
        pygame.draw.line(screen, BLACK, [col * CELL_SIZE, 0], [col * CELL_SIZE, HEIGHT], LINE_WIDTH)

    for row in range(HEIGHT // CELL_SIZE):
        pygame.draw.line(screen, BLACK, [0, row * CELL_SIZE], [WIDTH, row * CELL_SIZE], LINE_WIDTH)


def draw_cell(position):
    if position not in positions_of_cells:
        position_in_pixels = convert_to_pixels(position)
        pygame.draw.rect(screen, ORANGE, (position_in_pixels[0] + LINE_WIDTH, position_in_pixels[1] + LINE_WIDTH,
                                          CELL_SIZE - LINE_WIDTH,
                                          CELL_SIZE - LINE_WIDTH))
        positions_of_cells.add(position)


def clear():
    positions_of_cells.clear()
    draw_lines()


def generate():
    return set([(randrange(0, GRID_WIDTH + 1), randrange(0, GRID_HEIGHT + 1)) for i in range(randrange(50, 39 ** 2))])


def redraw_grid(positions):
    draw_lines()
    for position in positions:
        position_in_pixels = convert_to_pixels(position)
        pygame.draw.rect(screen, ORANGE, (position_in_pixels[0] + LINE_WIDTH, position_in_pixels[1] + LINE_WIDTH,
                                          CELL_SIZE - LINE_WIDTH,
                                          CELL_SIZE - LINE_WIDTH))


def find_neighbours(position_of_cell):
    neighbours = list()
    x, y = position_of_cell[0], position_of_cell[1]
    for dx in [-1, 0, 1]:
        if (x + dx < 0) or (x + dx > GRID_WIDTH):
            continue
        for dy in [-1, 0, 1]:
            if (dx == 0 and dy == 0) or (y + dy < 0) or (y + dy > GRID_HEIGHT):
                continue
            else:
                if (x + dx, y + dy) in positions_of_cells:
                    neighbours.append((x + dx, y + dy))
    return neighbours


def update_grid():
    new_positions_of_cells = set()

    for x in range(GRID_WIDTH + 1):
        for y in range(GRID_HEIGHT + 1):

            position = (x, y)
            neighbours = find_neighbours(position)

            if position in positions_of_cells:
                if len(neighbours) in [2, 3]:
                    new_positions_of_cells.add(position)
            else:
                if len(neighbours) == 3:
                    new_positions_of_cells.add(position)

    return new_positions_of_cells


def convert_to_num(position):
    return tuple((position[0] // CELL_SIZE, position[1] // CELL_SIZE))


def convert_to_pixels(position):
    return tuple((position[0] * CELL_SIZE, position[1] * CELL_SIZE))


def main():
    global positions_of_cells
    running = True
    start = False

    draw_lines()

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                x, y = convert_to_num((x, y))[0], convert_to_num((x, y))[1]
                draw_cell((x, y))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    if not start:
                        start = True
                    else:
                        start = False
                if event.key == pygame.K_c:
                    clear()
                    start = False
                if event.key == pygame.K_g:
                    print("g")
                    positions_of_cells = generate()
                    redraw_grid(positions_of_cells)

        if start:
            positions_of_cells = update_grid()
            redraw_grid(positions_of_cells)
            if len(positions_of_cells) == 0:
                start = False

        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    main()
