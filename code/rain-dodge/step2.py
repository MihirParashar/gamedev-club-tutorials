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

def draw(player):
    WIN.blit(BG, (0, 0))
    WIN.blit(SHIP, player)
    pygame.display.update()

def main():
    player = pygame.Rect(WIDTH // 2, HEIGHT - PLAYER_H, PLAYER_W, PLAYER_H)
    while True:
        CLOCK.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        draw(player)

main()
pygame.quit()
