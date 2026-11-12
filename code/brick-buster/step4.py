import pygame

pygame.init()
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brick Buster")
CLOCK = pygame.time.Clock()

INDIGO = (21, 19, 43)
CREAM = (244, 239, 225)
GOLD = (255, 210, 63)
CORAL = (217, 108, 95)
TEAL = (86, 163, 166)

PADDLE_W, PADDLE_H = 120, 14
PADDLE_VEL = 10
BALL_SIZE = 16
START_X, START_Y = 392, 432
ROWS, COLS = 4, 9
BRICK_W, BRICK_H = 80, 24
GAP = 8
WALL_TOP = 60
ROW_COLORS = [CORAL, GOLD, TEAL, CREAM]

def move_paddle(paddle):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left - PADDLE_VEL >= 0:
        paddle.x -= PADDLE_VEL
    if keys[pygame.K_RIGHT] and paddle.right + PADDLE_VEL <= WIDTH:
        paddle.x += PADDLE_VEL

def make_bricks():
    bricks = []
    for row in range(ROWS):
        for col in range(COLS):
            x = GAP + col * (BRICK_W + GAP)
            y = WALL_TOP + row * (BRICK_H + GAP)
            bricks.append(pygame.Rect(x, y, BRICK_W, BRICK_H))
    return bricks

def draw(paddle, ball, bricks):
    WIN.fill(INDIGO)
    for brick in bricks:
        row = (brick.y - WALL_TOP) // (BRICK_H + GAP)
        pygame.draw.rect(WIN, ROW_COLORS[row], brick)
    pygame.draw.rect(WIN, CREAM, paddle)
    pygame.draw.circle(WIN, GOLD, ball.center, BALL_SIZE // 2)
    pygame.display.update()

def main():
    paddle = pygame.Rect(340, 560, PADDLE_W, PADDLE_H)
    ball = pygame.Rect(START_X, START_Y, BALL_SIZE, BALL_SIZE)
    dx, dy = 3, -5
    bricks = make_bricks()
    while True:
        CLOCK.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        move_paddle(paddle)
        ball.x += dx
        ball.y += dy
        if ball.left <= 0:
            dx = abs(dx)
        if ball.right >= WIDTH:
            dx = -abs(dx)
        if ball.top <= 0:
            dy = abs(dy)
        if ball.colliderect(paddle):
            dy = -abs(dy)
            dx = (ball.centerx - paddle.centerx) // 10
        if ball.top > HEIGHT:
            ball.x, ball.y = START_X, START_Y
            dx, dy = 3, -5
        draw(paddle, ball, bricks)

main()
pygame.quit()
