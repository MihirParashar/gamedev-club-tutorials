import pygame

pygame.init()
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Coin Climb")
CLOCK = pygame.time.Clock()
FONT = pygame.font.Font(None, 40)

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
JUMP = -15
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
    on_ground = False
    for block in blocks:
        if player.colliderect(block):
            if vy > 0:
                player.bottom = block.top
                on_ground = True
            if vy < 0:
                player.top = block.bottom
            vy = 0
    return vy, on_ground

def collect(player, coins):
    for coin in coins[:]:
        if player.colliderect(coin):
            coins.remove(coin)

def win_screen(seconds):
    pygame.draw.rect(WIN, INDIGO, (140, 220, 520, 160))
    text = FONT.render(f"Every coin in {seconds:.1f}s!", True, GOLD)
    WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, 255))
    hint = FONT.render("Press R to play again", True, CREAM)
    WIN.blit(hint, (WIDTH // 2 - hint.get_width() // 2, 315))
    pygame.display.update()
    while True:
        CLOCK.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                return True

def draw(blocks, coins, player, seconds):
    WIN.fill(INDIGO)
    for block in blocks:
        pygame.draw.rect(WIN, SLATE, block)
    for coin in coins:
        pygame.draw.circle(WIN, GOLD, coin.center, 8)
    pygame.draw.rect(WIN, CORAL, player)
    label = f"{seconds:.1f}s   Coins left: {len(coins)}"
    WIN.blit(FONT.render(label, True, CREAM), (48, 6))
    pygame.display.update()

def main():
    blocks, coins, player = build_level()
    vy = 0
    on_ground = False
    start = pygame.time.get_ticks()
    while True:
        CLOCK.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        seconds = (pygame.time.get_ticks() - start) / 1000
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and on_ground:
            vy = JUMP
        move_x(player, blocks)
        vy, on_ground = move_y(player, blocks, vy)
        collect(player, coins)
        draw(blocks, coins, player, seconds)
        if len(coins) == 0:
            return win_screen(seconds)

while main():
    pass
pygame.quit()
