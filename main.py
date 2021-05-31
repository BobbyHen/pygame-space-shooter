import pygame

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
BLACK = (0, 0, 0)
SHIP_WIDTH, SHIP_HEIGHT = 50, 50

# Sprites
SHIP_IMAGE = pygame.image.load('assets/ship_G.png')
SHIP_IMAGE_SCALED = pygame.transform.scale(SHIP_IMAGE, (SHIP_WIDTH, SHIP_HEIGHT))

def draw_window(player):
    WIN.fill(BLACK)
    WIN.blit(SHIP_IMAGE_SCALED, (player.x, player.y))
    pygame.display.update()

def main():
    clock = pygame.time.Clock()
    player = pygame.Rect(440, 425, SHIP_WIDTH, SHIP_HEIGHT)

    run = True
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        key_pressed = pygame.key.get_pressed() # Get key pressed
        # horizontal movement
        if key_pressed[pygame.K_a]:
            player.x -= 5
        if key_pressed[pygame.K_d]:
            player.x += 5
        # Vertical movement
        '''if key_pressed[pygame.K_w]:
            player.y -= 5
        if key_pressed[pygame.K_s]:
            player.y += 5'''

        draw_window(player)
    pygame.quit()

if __name__ == '__main__':
    main()