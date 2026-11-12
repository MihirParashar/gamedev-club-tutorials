import math
import random
import pygame

pygame.init()
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pop")
CLOCK = pygame.time.Clock()
FONT = pygame.font.Font(None, 48)

INDIGO = (21, 19, 43)
GOLD = (255, 210, 63)
CREAM = (244, 239, 225)

START_R = 40

def move_target(target):
    target["x"] = random.randint(START_R, WIDTH - START_R)
    target["y"] = random.randint(START_R + 60, HEIGHT - START_R)

def is_inside(target, pos):
    distance = math.hypot(pos[0] - target["x"], pos[1] - target["y"])
    return distance <= target["r"]

def draw(target, score):
    WIN.fill(INDIGO)
    center = (target["x"], target["y"])
    pygame.draw.circle(WIN, GOLD, center, target["r"])
    WIN.blit(FONT.render(f"Score: {score}", True, CREAM), (16, 16))
    pygame.display.update()

def main():
    target = {"x": WIDTH // 2, "y": HEIGHT // 2, "r": START_R}
    score = 0
    while True:
        CLOCK.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if is_inside(target, event.pos):
                    score += 1
                    move_target(target)
        draw(target, score)

main()
pygame.quit()
