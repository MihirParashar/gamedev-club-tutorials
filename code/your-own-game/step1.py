import random
import pygame

pygame.init()
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
CLOCK = pygame.time.Clock()
FONT = pygame.font.Font(None, 48)
BIG_FONT = pygame.font.Font(None, 96)

INDIGO = (21, 19, 43)
CREAM = (244, 239, 225)
GOLD = (255, 210, 63)

def draw_centered(text, font, color, y):
    image = font.render(text, True, color)
    WIN.blit(image, (WIDTH // 2 - image.get_width() // 2, y))

def wait_for_key(key):
    while True:
        CLOCK.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == key:
                return True

def title_screen():
    WIN.fill(INDIGO)
    draw_centered("My Game", BIG_FONT, GOLD, 170)
    draw_centered("Arrow keys to move", FONT, CREAM, 300)
    draw_centered("Press SPACE to start", FONT, CREAM, 370)
    pygame.display.update()
    return wait_for_key(pygame.K_SPACE)

class Player:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2, HEIGHT // 2, 40, 40)
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
        self.rect.clamp_ip(WIN.get_rect())

    def draw(self):
        pygame.draw.rect(WIN, CREAM, self.rect)

def play():
    player = Player()
    while True:
        CLOCK.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        player.update()
        WIN.fill(INDIGO)
        player.draw()
        pygame.display.update()

def main():
    if title_screen():
        play()

main()
pygame.quit()
