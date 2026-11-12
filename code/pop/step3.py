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
SHRINK = 0.25

def spawn_target(targets):
    x = random.randint(START_R, WIDTH - START_R)
    y = random.randint(START_R + 60, HEIGHT - START_R)
    targets.append({"x": x, "y": y, "r": START_R})

def shrink_targets(targets):
    for target in targets[:]:
        target["r"] -= SHRINK
        if target["r"] <= 0:
            targets.remove(target)

def is_inside(target, pos):
    distance = math.hypot(pos[0] - target["x"], pos[1] - target["y"])
    return distance <= target["r"]

def pop_target(targets, pos):
    for target in targets:
        if is_inside(target, pos):
            targets.remove(target)
            return True
    return False

def draw(targets, score):
    WIN.fill(INDIGO)
    for target in targets:
        center = (target["x"], target["y"])
        pygame.draw.circle(WIN, GOLD, center, target["r"])
    WIN.blit(FONT.render(f"Score: {score}", True, CREAM), (16, 16))
    pygame.display.update()

def main():
    targets = []
    score = 0
    while True:
        CLOCK.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if pop_target(targets, event.pos):
                    score += 1
        if random.randint(0, 100) < 3:
            spawn_target(targets)
        shrink_targets(targets)
        draw(targets, score)

main()
pygame.quit()
