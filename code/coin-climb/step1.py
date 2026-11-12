import pygame

pygame.init()
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Coin Climb")
CLOCK = pygame.time.Clock()

INDIGO = (21, 19, 43)
CREAM = (244, 239, 225)
GOLD = (255, 210, 63)
SLATE = (88, 84, 140)
CORAL = (235, 110, 100)

TILE = 40
LEVEL = [
    "####################",
    "#..................#",
    "#..................#",
    "#...o...........o..#",
    "#..####.......####.#",
    "#.........o........#",
    "#........###.......#",
    "#...............o..#",
    "#.............####.#",
    "#..........o.......#",
    "#........####......#",
    "#.....o............#",
    "#.P..###...........#",
    "#.........o......o.#",
    "####################",
]

def build_level():
    blocks = []
    for row in range(len(LEVEL)):
        for col in range(len(LEVEL[row])):
            tile = LEVEL[row][col]
            x = col * TILE
            y = row * TILE
            if tile == "#":
                blocks.append(pygame.Rect(x, y, TILE, TILE))
    return blocks

def draw(blocks):
    WIN.fill(INDIGO)
    for block in blocks:
        pygame.draw.rect(WIN, SLATE, block)
    pygame.display.update()

def main():
    blocks = build_level()
    while True:
        CLOCK.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        draw(blocks)

main()
pygame.quit()
