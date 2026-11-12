import random
import pygame

pygame.init()
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rain Dodge")
CLOCK = pygame.time.Clock()
BG = pygame.transform.scale(pygame.image.load("bg.png"), (WIDTH, HEIGHT))

GOLD = (255, 210, 63)
CREAM = (244, 239, 225)

PLAYER_W, PLAYER_H = 66, 50
SHIP = pygame.transform.smoothscale(pygame.image.load("ship.png"), (PLAYER_W, PLAYER_H))
PLAYER_VEL = 6
DROP_W, DROP_H = 8, 16
DROP_VEL = 5

def move_player(player):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.left - PLAYER_VEL >= 0:
        player.x -= PLAYER_VEL
    if keys[pygame.K_RIGHT] and player.right + PLAYER_VEL <= WIDTH:
        player.x += PLAYER_VEL

def spawn_drop(drops):
    x = random.randint(0, WIDTH - DROP_W)
    drops.append(pygame.Rect(x, -DROP_H, DROP_W, DROP_H))

def move_drops(drops):
    for drop in drops[:]:
        drop.y += DROP_VEL
        if drop.top > HEIGHT:
            drops.remove(drop)

def draw(player, drops):
    WIN.blit(BG, (0, 0))
    WIN.blit(SHIP, player)
    for drop in drops:
        pygame.draw.rect(WIN, CREAM, drop)
    pygame.display.update()

def main():
    player = pygame.Rect(WIDTH // 2, HEIGHT - PLAYER_H, PLAYER_W, PLAYER_H)
    drops = []
    while True:
        CLOCK.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        move_player(player)
        if random.randint(0, 100) < 3:
            spawn_drop(drops)
        move_drops(drops)
        draw(player, drops)

main()
pygame.quit()
