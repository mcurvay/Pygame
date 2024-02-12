import pygame
import sys
import random

# Pygame başlat
pygame.init()

# Ekran boyutu ve başlık
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Kutu Avı Oyunu")

# Renkler
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Uzay gemisi
spaceship_image = pygame.Surface((50, 50))
spaceship_image.fill(WHITE)
spaceship_rect = spaceship_image.get_rect()
spaceship_rect.centerx = SCREEN_WIDTH // 2
spaceship_rect.bottom = SCREEN_HEIGHT - 10

# Kutular
def create_box():
    box = pygame.Surface((30, 30))
    box.fill(RED)
    box_rect = box.get_rect()
    box_rect.x = random.randint(0, SCREEN_WIDTH - box_rect.width)
    box_rect.y = 0
    return box, box_rect

boxes = []
BOX_SPEED = 5
BOX_SPAWN_RATE = 25  # Kutu yaratma sıklığı (frame)

# Ateş topu
fireball_image = pygame.Surface((10, 20))
fireball_image.fill(WHITE)
fireball_rect = fireball_image.get_rect()
FIREBALL_SPEED = 10
fireball_active = False

# Oyun için puan
score = 0
font = pygame.font.Font(None, 36)

# Ana döngü
clock = pygame.time.Clock()
running = True
while running:
    # Olay işleme
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if not fireball_active:
                fireball_rect.midbottom = spaceship_rect.midtop
                fireball_active = True

    # Kutu oluşturma
    if random.randint(1, BOX_SPAWN_RATE) == 1:
        box, box_rect = create_box()
        boxes.append((box, box_rect))

    # Uzay gemisinin hareketi
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and spaceship_rect.left > 0:
        spaceship_rect.x -= 5
    if keys[pygame.K_RIGHT] and spaceship_rect.right < SCREEN_WIDTH:
        spaceship_rect.x += 5

    # Ateş topunun hareketi ve kutuları vurması
    if fireball_active:
        fireball_rect.y -= FIREBALL_SPEED
        for box, box_rect in boxes:
            if fireball_rect.colliderect(box_rect):
                score += 1
                fireball_active = False
                boxes.remove((box, box_rect))
                break
        if fireball_rect.y < 0:
            fireball_active = False

    # Kutuların hareketi ve çarpışma kontrolü
    for box, box_rect in boxes:
        box_rect.y += BOX_SPEED
        if box_rect.colliderect(spaceship_rect):
            running = False
        elif box_rect.top > SCREEN_HEIGHT:
            boxes.remove((box, box_rect))

    # Ekranı temizle
    screen.fill(BLACK)

    # Kutuları, ateş topunu ve uzay gemisini çiz
    for box, box_rect in boxes:
        screen.blit(box, box_rect)
    if fireball_active:
        screen.blit(fireball_image, fireball_rect)
    screen.blit(spaceship_image, spaceship_rect)

    # Puanı ekrana yazdır
    score_text = font.render("Puan: " + str(score), True, WHITE)
    screen.blit(score_text, (10, 10))

    # Ekranı güncelle
    pygame.display.flip()

    # FPS ayarı
    clock.tick(30)

# Pygame çıkış
pygame.quit()
sys.exit()
