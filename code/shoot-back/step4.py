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
ENEMY_SIZE = 44
HIT = pygame.mixer.Sound("hit.wav")
FONT = pygame.font.Font(None, 48)

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

class Enemy:
    def __init__(self, x, speed, health, color):
        self.rect = pygame.Rect(x, -ENEMY_SIZE, ENEMY_SIZE, ENEMY_SIZE)
        self.speed = speed
        self.health = health
        self.color = color

    def update(self):
        self.rect.y += self.speed

    def draw(self):
        r = self.rect
        points = [r.midtop, r.midright, r.midbottom, r.midleft]
        pygame.draw.polygon(WIN, self.color, points)
        if self.health == 2:
            pygame.draw.circle(WIN, CREAM, r.center, 8)

def spawn_enemy(enemies):
    x = random.randint(0, WIDTH - ENEMY_SIZE)
    if random.randint(1, 4) == 1:
        enemies.append(Enemy(x, 1, 2, CORAL))
    else:
        enemies.append(Enemy(x, random.randint(2, 4), 1, TEAL))

def hit_enemies(bullets, enemies):
    points = 0
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if bullet.colliderect(enemy.rect):
                bullets.remove(bullet)
                enemy.health -= 1
                if enemy.health == 0:
                    enemies.remove(enemy)
                HIT.play()
                points += 10
                break
    return points

def draw(player, bullets, enemies, score):
    WIN.blit(BG, (0, 0))
    for bullet in bullets:
        pygame.draw.rect(WIN, GOLD, bullet)
    for enemy in enemies:
        enemy.draw()
    WIN.blit(SHIP, player)
    WIN.blit(FONT.render(f"{score}", True, CREAM), (16, 16))
    pygame.display.update()

def main():
    player = pygame.Rect(WIDTH // 2, HEIGHT - PLAYER_H, PLAYER_W, PLAYER_H)
    bullets = []
    enemies = []
    last_shot = 0
    score = 0
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
        if random.randint(0, 100) < 2:
            spawn_enemy(enemies)
        for enemy in enemies[:]:
            enemy.update()
            if enemy.rect.top > HEIGHT:
                enemies.remove(enemy)
        score += hit_enemies(bullets, enemies)
        draw(player, bullets, enemies, score)

main()
pygame.quit()
