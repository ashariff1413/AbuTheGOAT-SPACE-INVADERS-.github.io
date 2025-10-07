import pygame
import random

pygame.init()
screen = pygame.display.set_mode((1600, 900))
pygame.display.set_caption("Space Invaders Multiplayer")
pygame.display.set_icon(pygame.image.load("icon.png"))

pygame.mixer.music.load("maintheme.mp3")
pygame.mixer.music.play(-1)

menuscreen = pygame.image.load("before startscreen.jpg")
startscreen = pygame.image.load("startscreen.png")
startscreen = pygame.transform.scale(startscreen, (1600, 900))
player_sprite = pygame.image.load("Player.jpg")
player_sprite = pygame.transform.scale(player_sprite, (30, 20))
player_sprite.set_colorkey((255, 255, 255))
enemy_sprite = pygame.image.load("enemy.png.jpg")
enemy_sprite = pygame.transform.scale(enemy_sprite, (40, 30))
clock = pygame.time.Clock()

# Game states
show_menu = True
show_start = False
show_rules = False
game_started = False

# Player
player_x = 750
player_y = 800
player_speed = 5
player_health = 100
max_health = 100

# Bullets
bullets = []
enemy_bullets = []
bullet_speed = 7
enemy_bullet_speed = 5
last_shot = 0
shoot_cooldown = 200
last_enemy_shot = 0
enemy_shoot_cooldown = 250

# Aliens - scattered formation starting off-screen
aliens = []
# Row 1: 2 aliens
for col in range(2):
    aliens.append([400 + col * 200, -200])
# Row 2: 2 aliens  
for col in range(2):
    aliens.append([350 + col * 250, -280])
# Row 3: 3 aliens
for col in range(3):
    aliens.append([300 + col * 200, -360])
# Row 4: 4 aliens
for col in range(4):
    aliens.append([250 + col * 180, -440])
# Row 5: Full array (10 aliens)
for col in range(10):
    aliens.append([100 + col * 120, -520])
# Row 6: Original grid formation (5 rows x 10 columns)
for row in range(5):
    for col in range(10):
        aliens.append([100 + col * 120, -600 - row * 80])

alien_speed = 1
alien_direction = 1
game_over = False
win = False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if show_menu:
                # Play button
                if 500 <= mouse_x <= 1100 and 350 <= mouse_y <= 450:
                    show_menu = False
                    show_start = True
                # Options button
                elif 500 <= mouse_x <= 1100 and 500 <= mouse_y <= 600:
                    show_menu = False
                    show_rules = True
                # Quit button
                elif 500 <= mouse_x <= 1100 and 650 <= mouse_y <= 750:
                    running = False
            elif show_rules:
                # Back button
                if 50 <= mouse_x <= 250 and 50 <= mouse_y <= 150:
                    show_rules = False
                    show_menu = True
        if event.type == pygame.KEYDOWN:
            if show_start and event.key == pygame.K_RETURN:
                show_start = False
                game_started = True
            elif game_over and event.key == pygame.K_r:
                # Reset game
                game_over = False
                win = False
                player_health = 100
                player_x = 750
                bullets = []
                enemy_bullets = []
                aliens = []
                # Recreate aliens
                for col in range(2):
                    aliens.append([400 + col * 200, -200])
                for col in range(2):
                    aliens.append([350 + col * 250, -280])
                for col in range(3):
                    aliens.append([300 + col * 200, -360])
                for col in range(4):
                    aliens.append([250 + col * 180, -440])
                for col in range(10):
                    aliens.append([100 + col * 120, -520])
                for row in range(5):
                    for col in range(10):
                        aliens.append([100 + col * 120, -600 - row * 80])
            elif game_started and event.key == pygame.K_SPACE and pygame.time.get_ticks() - last_shot > shoot_cooldown:
                bullets.append([player_x + 20, player_y])
                last_shot = pygame.time.get_ticks()

    if show_menu:
        screen.fill((0, 0, 0))
        menu_rect = menuscreen.get_rect(center=(800, 450))
        screen.blit(menuscreen, menu_rect)
        
        # Draw buttons
        font = pygame.font.Font(None, 72)
        # Play button
        pygame.draw.rect(screen, (0, 100, 0), (500, 350, 600, 100))
        play_text = font.render("PLAY", True, (255, 255, 255))
        screen.blit(play_text, (720, 380))
        
        # Options button
        pygame.draw.rect(screen, (0, 0, 100), (500, 500, 600, 100))
        options_text = font.render("OPTIONS", True, (255, 255, 255))
        screen.blit(options_text, (680, 530))
        
        # Quit button
        pygame.draw.rect(screen, (100, 0, 0), (500, 650, 600, 100))
        quit_text = font.render("QUIT", True, (255, 255, 255))
        screen.blit(quit_text, (720, 680))
        
    elif show_rules:
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 64)
        rules = [
            "SPACE INVADERS RULES:",
            "",
            "- Use LEFT/RIGHT arrows to move",
            "- Press SPACE to shoot",
            "- Destroy all aliens to win",
            "- Avoid enemy bullets",
            "- Bullet collisions create blast radius",
            "- Health decreases when hit"
        ]
        for i, rule in enumerate(rules):
            color = (255, 255, 0) if i == 0 else (255, 255, 255)
            text = font.render(rule, True, color)
            screen.blit(text, (100, 100 + i * 70))
        # Back button
        pygame.draw.rect(screen, (100, 100, 100), (50, 50, 200, 100))
        back_text = font.render("BACK", True, (255, 255, 255))
        screen.blit(back_text, (110, 85))
        
    elif show_start:
        screen.blit(startscreen, (0, 0))
    elif game_started:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < 1560:
            player_x += player_speed

        # Move bullets
        bullets = [[b[0], b[1] - bullet_speed] for b in bullets if b[1] > 0]
        # Move enemy bullets with direction
        new_enemy_bullets = []
        for b in enemy_bullets:
            new_x = b[0] + b[2]
            new_y = b[1] + b[3]
            if 0 <= new_x <= 1600 and 0 <= new_y <= 900:
                new_enemy_bullets.append([new_x, new_y, b[2], b[3]])
        enemy_bullets = new_enemy_bullets

        # Enemy shooting - aimed at player
        if pygame.time.get_ticks() - last_enemy_shot > enemy_shoot_cooldown and aliens:
            shooter = random.choice(aliens)
            # Calculate direction to player
            dx = (player_x + 15) - (shooter[0] + 20)
            dy = (player_y + 10) - (shooter[1] + 30)
            distance = (dx**2 + dy**2)**0.5
            if distance > 0:
                bullet_dx = (dx / distance) * enemy_bullet_speed
                bullet_dy = (dy / distance) * enemy_bullet_speed
                enemy_bullets.append([shooter[0] + 20, shooter[1] + 30, bullet_dx, bullet_dy])
            last_enemy_shot = pygame.time.get_ticks()

        # Move aliens down and sideways
        for alien in aliens:
            alien[0] += alien_speed * alien_direction * 0.5
            alien[1] += 0.3  # Slower downward movement
        
        if any(alien[0] <= 0 or alien[0] >= 1560 for alien in aliens if alien[1] > 0):
            alien_direction *= -1

        # Check bullet collisions with aliens
        for bullet in bullets[:]:
            for alien in aliens[:]:
                if (alien[0] < bullet[0] < alien[0] + 40 and 
                    alien[1] < bullet[1] < alien[1] + 30):
                    bullets.remove(bullet)
                    aliens.remove(alien)
                    break

        # Check bullet vs bullet collisions (blast radius)
        for bullet in bullets[:]:
            for enemy_bullet in enemy_bullets[:]:
                if (abs(bullet[0] - enemy_bullet[0]) < 20 and abs(bullet[1] - enemy_bullet[1]) < 20):
                    if bullet in bullets:
                        bullets.remove(bullet)
                    if enemy_bullet in enemy_bullets:
                        enemy_bullets.remove(enemy_bullet)
                    # Blast radius - remove aliens within 100 pixels
                    blast_x, blast_y = bullet[0], bullet[1]
                    for alien in aliens[:]:
                        if (abs(alien[0] - blast_x) < 100 and abs(alien[1] - blast_y) < 100):
                            aliens.remove(alien)
                    break

        # Check enemy bullets hitting player
        for enemy_bullet in enemy_bullets[:]:
            if (player_x < enemy_bullet[0] < player_x + 30 and 
                player_y < enemy_bullet[1] < player_y + 20):
                enemy_bullets.remove(enemy_bullet)
                player_health -= 20
                if player_health <= 0:
                    game_over = True

        # Check win/lose conditions
        if not aliens:
            win = True
            game_over = True
        if any(alien[1] > 850 for alien in aliens):
            game_over = True

        screen.fill((0, 0, 0))
        
        if game_over:
            if win:
                font = pygame.font.Font(None, 74)
                text = font.render("YOU WIN!", True, (0, 255, 0))
                screen.blit(text, (700, 400))
            else:
                font = pygame.font.Font(None, 74)
                text = font.render("GAME OVER!", True, (255, 0, 0))
                screen.blit(text, (650, 400))
            # Play again button
            font = pygame.font.Font(None, 48)
            play_again_text = font.render("Press R to Play Again", True, (255, 255, 255))
            screen.blit(play_again_text, (650, 500))
        else:
            # Draw player
            screen.blit(player_sprite, (player_x, player_y))
            
            # Draw bullets
            for bullet in bullets:
                pygame.draw.rect(screen, (255, 255, 0), (bullet[0], bullet[1], 5, 10))
            
            # Draw enemy bullets
            for enemy_bullet in enemy_bullets:
                pygame.draw.rect(screen, (255, 0, 255), (enemy_bullet[0], enemy_bullet[1], 5, 10))
            
            # Draw health bar
            health_width = int((player_health / max_health) * 200)
            pygame.draw.rect(screen, (255, 0, 0), (50, 50, 200, 20))
            pygame.draw.rect(screen, (0, 255, 0), (50, 50, health_width, 20))
            font = pygame.font.Font(None, 36)
            health_text = font.render(f"Health: {player_health}", True, (255, 255, 255))
            screen.blit(health_text, (50, 80))
            
            # Draw aliens
            for alien in aliens:
                screen.blit(enemy_sprite, (alien[0], alien[1]))
    
    pygame.display.flip()
    clock.tick(60)