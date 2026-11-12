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
PLAYER_SIZE = 30
SPEED = 5
GRAVITY = 1
MAX_FALL = 20
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
    coins = []
    player = pygame.Rect(0, 0, PLAYER_SIZE, PLAYER_SIZE)
    for row in range(len(LEVEL)):
        for col in range(len(LEVEL[row])):
            tile = LEVEL[row][col]
            x = col * TILE
            y = row * TILE
            if tile == "#":
                blocks.append(pygame.Rect(x, y, TILE, TILE))
            if tile == "o":
                coins.append(pygame.Rect(x + 12, y + 12, 16, 16))
            if tile == "P":
                player.x = x + 5
                player.y = y + 5
    return blocks, coins, player

def move_x(player, blocks):
    keys = pygame.key.get_pressed()
    dx = 0
    if keys[pygame.K_LEFT]:
        dx = -SPEED
    if keys[pygame.K_RIGHT]:
        dx = SPEED
    player.x += dx
    for block in blocks:
        if player.colliderect(block):
            if dx > 0:
                player.right = block.left
            if dx < 0:
                player.left = block.right

def move_y(player, blocks, vy):
    vy += GRAVITY
    if vy > MAX_FALL:
        vy = MAX_FALL
    player.y += vy
    for block in blocks:
        if player.colliderect(block):
            player.bottom = block.top
            vy = 0
    return vy

def draw(blocks, coins, player):
    WIN.fill(INDIGO)
    for block in blocks:
        pygame.draw.rect(WIN, SLATE, block)
    for coin in coins:
        pygame.draw.circle(WIN, GOLD, coin.center, 8)
    pygame.draw.rect(WIN, CORAL, player)
    pygame.display.update()

def main():
    blocks, coins, player = build_level()
    vy = 0
    while True:
        CLOCK.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        move_x(player, blocks)
        vy = move_y(player, blocks, vy)
        draw(blocks, coins, player)

main()
pygame.quit()
