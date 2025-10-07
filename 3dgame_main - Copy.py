import pygame, sys, random

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Game")

clock = pygame.time.Clock()

# --- Load images ---
background = pygame.image.load("background.png").convert()
start_image = pygame.image.load("startscreen.png").convert_alpha()
playbutton = pygame.image.load("playbutton.png").convert_alpha()
options_surf = pygame.image.load("options.png").convert_alpha()
quit_surf = pygame.image.load("quit.png").convert_alpha()

# --- Player and invader ---
player1_orig = pygame.image.load("player1.png").convert_alpha()
target_player_width = 64
pw, ph = player1_orig.get_size()
scale = target_player_width / pw
player1 = pygame.transform.smoothscale(player1_orig, (int(pw * scale), int(ph * scale)))

try:
    player2_orig = pygame.image.load("player2.png").convert_alpha()
    player2 = pygame.transform.smoothscale(player2_orig, (int(pw * scale), int(ph * scale)))
except Exception:
    player2 = player1.copy()

equipped_skin = player1
equipped_rect = equipped_skin.get_rect()

invader_orig = pygame.image.load("invader.png").convert_alpha()
invader = pygame.transform.smoothscale(invader_orig, (40, 30))

# --- UI setup ---
image_rect = start_image.get_rect(center=(screen.get_width()//2, screen.get_height()//2 - 100))
button_padding = 40

font = pygame.font.SysFont("Arial", 32)
def get_retro_font(size):
    return pygame.font.SysFont("Consolas", size, bold=True)

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# --- Game state ---
running = True
moving = False
state = 'start'
show_options_menu = False

# Hover states
play_hover = options_hover = quit_hover = False

# Player variables
player_x = 368
player_y = 480
player_speed = 5

# Shooting
bullets = []
bullet_speed = 7
shoot_cooldown = 500
last_shot = 0

# Invaders
aliens = []
alien_speed = 100
spawn_timer = 2.0
spawn_interval = 2.0
spawned_invaders = 0
max_invaders = 10

# Game states
game_over = False
win = False

speed = 600  # start screen slide speed

# --- Main loop ---
while running:
    dt = clock.tick(60) / 1000.0
    click = False
    mx, my = pygame.mouse.get_pos()

    # --- Event loop ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_o:
                if not moving:
                    moving = True
                    pygame.mixer.music.stop()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            click = True

    # --- Update hover states ---
    if state == 'start' and not moving:
        play_rect = playbutton.get_rect(midtop=(image_rect.centerx, image_rect.bottom + button_padding))
        options_rect = options_surf.get_rect(midtop=(image_rect.centerx, image_rect.bottom + button_padding + 60))
        quit_rect = quit_surf.get_rect(midtop=(image_rect.centerx, options_rect.bottom + 10))

        play_hover = play_rect.collidepoint(mx, my)
        options_hover = options_rect.collidepoint(mx, my)
        quit_hover = quit_rect.collidepoint(mx, my)

        if click:
            if play_rect.collidepoint((mx, my)):
                moving = True
                pygame.mixer.music.stop()
            elif options_rect.collidepoint((mx, my)):
                show_options_menu = True
                moving = True
                pygame.mixer.music.stop()
            elif quit_rect.collidepoint((mx, my)):
                pygame.quit()
                sys.exit()

    # --- Move start screen down ---
    if moving and state == 'start':
        image_rect.y += int(speed * dt)
        if image_rect.top >= screen.get_height():
            moving = False
            if show_options_menu:
                state = 'skin_select'
                show_options_menu = False
            else:
                state = 'playing'

    # --- Drawing ---
    screen.blit(background, (0, 0))

    if state == 'start':
        screen.blit(start_image, image_rect)
        screen.blit(playbutton, play_rect)
        screen.blit(options_surf, options_rect)
        screen.blit(quit_surf, quit_rect)

        # Hover scaling
        if play_hover:
            scaled = pygame.transform.rotozoom(playbutton, 0, 1.08)
            screen.blit(scaled, scaled.get_rect(center=play_rect.center))
        if options_hover:
            scaled = pygame.transform.rotozoom(options_surf, 0, 1.08)
            screen.blit(scaled, scaled.get_rect(center=options_rect.center))
        if quit_hover:
            scaled = pygame.transform.rotozoom(quit_surf, 0, 1.08)
            screen.blit(scaled, scaled.get_rect(center=quit_rect.center))

    elif state == 'skin_select':
        font_small = get_retro_font(20)
        center_x = screen.get_width() // 2
        spacing = 220

        left_x = center_x - spacing // 2 - player1.get_width() // 2
        right_x = center_x + spacing // 2 - player2.get_width() // 2
        y_pos = 200

        left_rect = player1.get_rect(topleft=(left_x, y_pos))
        right_rect = player2.get_rect(topleft=(right_x, y_pos))
        screen.blit(player1, left_rect)
        screen.blit(player2, right_rect)

        equip_w, equip_h = 120, 36
        left_equip_rect = pygame.Rect(left_rect.x + (player1.get_width() - equip_w)//2, left_rect.bottom + 20, equip_w, equip_h)
        right_equip_rect = pygame.Rect(right_rect.x + (player2.get_width() - equip_w)//2, right_rect.bottom + 20, equip_w, equip_h)
        pygame.draw.rect(screen, (40, 40, 40), left_equip_rect)
        pygame.draw.rect(screen, (40, 40, 40), right_equip_rect)
        pygame.draw.rect(screen, (255, 255, 255), left_equip_rect, 2)
        pygame.draw.rect(screen, (255, 255, 255), right_equip_rect, 2)

        left_txt = font_small.render("EQUIP", True, (255, 255, 255))
        right_txt = font_small.render("EQUIP", True, (255, 255, 255))
        screen.blit(left_txt, left_txt.get_rect(center=left_equip_rect.center))
        screen.blit(right_txt, right_txt.get_rect(center=right_equip_rect.center))

        hint = font_small.render("Choose a skin to play as", True, (200, 200, 200))
        screen.blit(hint, hint.get_rect(center=(center_x, y_pos - 40)))

        if click:
            if left_equip_rect.collidepoint((mx, my)):
                equipped_skin = player1
                state = 'playing'
            elif right_equip_rect.collidepoint((mx, my)):
                equipped_skin = player2
                state = 'playing'

    elif state == 'playing':
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < screen.get_width() - equipped_skin.get_width():
            player_x += player_speed
        if keys[pygame.K_SPACE] and pygame.time.get_ticks() - last_shot > shoot_cooldown:
            bullets.append([player_x + equipped_skin.get_width()//2, player_y])
            last_shot = pygame.time.get_ticks()

        bullets = [[b[0], b[1] - bullet_speed] for b in bullets if b[1] > 0]

        spawn_timer -= dt
        if spawn_timer <= 0 and spawned_invaders < max_invaders:
            sx = random.randint(20, screen.get_width() - 60)
            sy = -40
            aliens.append([sx, sy])
            spawned_invaders += 1
            spawn_timer = spawn_interval

        for alien in aliens:
            alien[1] += alien_speed * dt

        for bullet in bullets[:]:
            for alien in aliens[:]:
                if (alien[0] < bullet[0] < alien[0] + 40 and
                    alien[1] < bullet[1] < alien[1] + 30):
                    if bullet in bullets:
                        bullets.remove(bullet)
                    if alien in aliens:
                        aliens.remove(alien)
                    break

        if not aliens and spawned_invaders >= max_invaders:
            win = True
            game_over = True
        if any(alien[1] > player_y for alien in aliens):
            game_over = True

        equipped_rect.midtop = (player_x + equipped_skin.get_width()//2, player_y)
        screen.blit(equipped_skin, equipped_rect)

        for bullet in bullets:
            pygame.draw.rect(screen, (255, 255, 0), (bullet[0], bullet[1], 5, 10))

        for alien in aliens:
            screen.blit(invader, (alien[0], alien[1]))

        if game_over:
            font_big = get_retro_font(48)
            if win:
                text = font_big.render("LEVEL COMPLETE!", True, (0, 255, 0))
            else:
                text = font_big.render("GAME OVER!", True, (255, 0, 0))
            rect = text.get_rect(center=(screen.get_width()//2, screen.get_height()//2))
            screen.blit(text, rect)

    pygame.display.flip()
