import random
import pygame

pygame.init()
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shoot Back")
CLOCK = pygame.time.Clock()
BG = pygame.transform.scale(pygame.image.load("bg.png"), (WIDTH, HEIGHT))

GOLD = (255, 210, 63)
CREAM = (244, 239, 225)
TEAL = (86, 184, 170)
CORAL = (226, 109, 92)

PLAYER_W, PLAYER_H = 66, 50
SHIP = pygame.image.load("ship.png")
SHIP = pygame.transform.smoothscale(SHIP, (PLAYER_W, PLAYER_H))
PLAYER_VEL = 7
BULLET_VEL = 10
COOLDOWN = 250
SHOOT = pygame.mixer.Sound("shoot.wav")

def move_player(player):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.left - PLAYER_VEL >= 0:
        player.x -= PLAYER_VEL
    if keys[pygame.K_RIGHT] and player.right + PLAYER_VEL <= WIDTH:
        player.x += PLAYER_VEL

def fire(player, bullets):
    bullets.append(pygame.Rect(player.centerx - 3, player.top, 6, 16))
    SHOOT.play()

def move_bullets(bullets):
    for bullet in bullets[:]:
        bullet.y -= BULLET_VEL
        if bullet.bottom < 0:
            bullets.remove(bullet)

def draw(player, bullets):
    WIN.blit(BG, (0, 0))
    for bullet in bullets:
        pygame.draw.rect(WIN, GOLD, bullet)
    WIN.blit(SHIP, player)
    pygame.display.update()

def main():
    player = pygame.Rect(WIDTH // 2, HEIGHT - PLAYER_H, PLAYER_W, PLAYER_H)
    bullets = []
    last_shot = 0
    while True:
        CLOCK.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                now = pygame.time.get_ticks()
                if now - last_shot >= COOLDOWN:
                    fire(player, bullets)
                    last_shot = now
        move_player(player)
        move_bullets(bullets)
        draw(player, bullets)

main()
pygame.quit()
