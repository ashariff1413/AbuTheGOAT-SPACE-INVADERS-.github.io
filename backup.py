import pygame
import random

pygame.init()
screen = pygame.display.set_mode((900, 1600))
pygame.display.set_caption("Space Invaders Multiplayer")
pygame.display.set_icon(pygame.image.load("icon.png"))

pygame.mixer.music.load("maintheme.mp3")
pygame.mixer.music.play(-1)

startscreen = pygame.image.load("startscreen.png")
clock = pygame.time.Clock()

# Player
player_x = 750
player_y = 800
player_speed = 5

# Bullets
bullets = []
bullet_speed = 7
last_shot = 0
shoot_cooldown = 200

# Aliens
aliens = []
for row in range(5):
    for col in range(10):
        aliens.append([100 + col * 80, 50 + row * 60])

alien_speed = 3
alien_direction = 1
game_over = False
win = False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and pygame.time.get_ticks() - last_shot > shoot_cooldown:
                bullets.append([player_x + 20, player_y])
                last_shot = pygame.time.get_ticks()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < 1560:
        player_x += player_speed

    # Move bullets
    bullets = [[b[0], b[1] - bullet_speed] for b in bullets if b[1] > 0]

    # Move aliens
    for alien in aliens:
        alien[0] += alien_speed * alien_direction
    
    if any(alien[0] <= 0 or alien[0] >= 1560 for alien in aliens):
        alien_direction *= -1
        for alien in aliens:
            alien[1] += 20

    # Check collisions
    for bullet in bullets[:]:
        for alien in aliens[:]:
            if (alien[0] < bullet[0] < alien[0] + 40 and 
                alien[1] < bullet[1] < alien[1] + 30):
                bullets.remove(bullet)
                aliens.remove(alien)
                break

    # Check win/lose conditions
    if not aliens:
        win = True
        game_over = True
    if any(alien[1] > 750 for alien in aliens):
        game_over = True

    screen.fill((0, 0, 0))
    
    if game_over:
        if win:
            font = pygame.font.Font(None, 74)
            text = font.render("YOU WIN!", True, (0, 255, 0))
            screen.blit(text, (700, 400))
        else:
            font = pygame.font.Font(None, 74)
            text = font.render("GAME OVER!, YOU LOST", True, (255, 0, 0))
            screen.blit(text, (650, 400))
    else:
        # Draw player
        pygame.draw.rect(screen, (0, 255, 0), (player_x, player_y, 40, 30))
        
        # Draw bullets
        for bullet in bullets:
            pygame.draw.rect(screen, (255, 255, 0), (bullet[0], bullet[1], 5, 10))
        
        # Draw aliens
        for alien in aliens:
            pygame.draw.rect(screen, (255, 0, 0), (alien[0], alien[1], 40, 30))
    
    pygame.display.flip()
    clock.tick(60)
    