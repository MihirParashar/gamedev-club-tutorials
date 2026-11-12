import math
import random
import pygame

pygame.init()
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pop")
CLOCK = pygame.time.Clock()

INDIGO = (21, 19, 43)
GOLD = (255, 210, 63)
CREAM = (244, 239, 225)

START_R = 40

def draw():
    WIN.fill(INDIGO)
    pygame.draw.circle(WIN, GOLD, (WIDTH // 2, HEIGHT // 2), START_R)
    pygame.display.update()

def main():
    while True:
        CLOCK.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        draw()

main()
pygame.quit()
