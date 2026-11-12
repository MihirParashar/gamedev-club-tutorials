import pygame

pygame.init()
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brick Buster")
CLOCK = pygame.time.Clock()

INDIGO = (21, 19, 43)
CREAM = (244, 239, 225)
GOLD = (255, 210, 63)

PADDLE_W, PADDLE_H = 120, 14
PADDLE_VEL = 10

def move_paddle(paddle):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left - PADDLE_VEL >= 0:
        paddle.x -= PADDLE_VEL
    if keys[pygame.K_RIGHT] and paddle.right + PADDLE_VEL <= WIDTH:
        paddle.x += PADDLE_VEL

def draw(paddle):
    WIN.fill(INDIGO)
    pygame.draw.rect(WIN, CREAM, paddle)
    pygame.display.update()

def main():
    paddle = pygame.Rect(340, 560, PADDLE_W, PADDLE_H)
    while True:
        CLOCK.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        move_paddle(paddle)
        draw(paddle)

main()
pygame.quit()
