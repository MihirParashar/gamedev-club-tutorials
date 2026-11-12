import os
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
FONT = pygame.font.Font(None, 48)

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

def load_best():
    if os.path.exists("best.txt"):
        with open("best.txt") as file:
            return int(file.read())
    return 0

def save_best(score):
    with open("best.txt", "w") as file:
        file.write(str(score))

def game_over(score):
    best = load_best()
    if score > best:
        best = score
        save_best(best)
    text = FONT.render(f"Game over! You lasted {score}s", True, GOLD)
    WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
    hint = FONT.render(f"Best: {best}s. Press R to play again", True, CREAM)
    WIN.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT // 2 + 60))
    pygame.display.update()
    while True:
        CLOCK.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                return True

def draw(player, drops, score, lives):
    WIN.blit(BG, (0, 0))
    WIN.blit(SHIP, player)
    for drop in drops:
        pygame.draw.rect(WIN, CREAM, drop)
    WIN.blit(FONT.render(f"{score}s", True, CREAM), (16, 16))
    text = FONT.render(f"Lives: {lives}", True, CREAM)
    WIN.blit(text, (WIDTH - text.get_width() - 16, 16))
    pygame.display.update()

def main():
    player = pygame.Rect(WIDTH // 2, HEIGHT - PLAYER_H, PLAYER_W, PLAYER_H)
    drops = []
    lives = 3
    start = pygame.time.get_ticks()
    while True:
        CLOCK.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        score = (pygame.time.get_ticks() - start) // 1000
        move_player(player)
        if random.randint(0, 100) < 3 + score // 2:
            spawn_drop(drops)
        move_drops(drops)
        hit = player.collidelist(drops)
        if hit != -1:
            drops.pop(hit)
            lives -= 1
            if lives == 0:
                return game_over(score)
        draw(player, drops, score, lives)

while main():
    pass
pygame.quit()
