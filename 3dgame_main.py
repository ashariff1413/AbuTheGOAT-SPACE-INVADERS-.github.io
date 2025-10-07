import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invaders Multiplayer")
pygame.display.set_icon(pygame.image.load("icon.png"))

pygame.mixer.music.load("maintheme.mp3")
pygame.mixer.music.play(-1)  # Play the music indefinitely


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))  # Fill the screen with black
    pygame.display.flip()
    