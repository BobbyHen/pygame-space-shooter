import pygame

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
BLACK = (0, 0, 0)
SHIP_WIDTH, SHIP_HEIGHT = 50, 50

bullets = []

# Sprites
SHIP_IMAGE = pygame.image.load('assets/ship_G.png')
SHIP_IMAGE_SCALED = pygame.transform.scale(SHIP_IMAGE, (SHIP_WIDTH, SHIP_HEIGHT))
BULLET_VELOCITY = 7
MAX_BULLETS = 5

def handle_movement(key_pressed, player):
    # horizontal movement
    if key_pressed[pygame.K_a] and player.x > 0:
        player.x -= 5
        print("A PRESSED")
    if key_pressed[pygame.K_d] and player.x < WIDTH - SHIP_WIDTH:
        player.x += 5
        print("D PRESSED")
    # Vertical movement
    # if key_pressed[pygame.K_w]:
    #     player.y -= 5
    #     print("W PRESSED")
    # if key_pressed[pygame.K_s]:
    #     player.y += 5
    #     print("S PRESSED")

def draw_window(player):
    WIN.fill(BLACK)
    WIN.blit(SHIP_IMAGE_SCALED, (player.x, player.y))
    pygame.display.update()

def main():
    clock = pygame.time.Clock()
    player = pygame.Rect(440, 425, SHIP_WIDTH, SHIP_HEIGHT)

    bullets = []

    run = True
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(player.x + player.width, player.y + player.height/2 -2, 10, 5)
                    bullets.append(bullet)

        key_pressed = pygame.key.get_pressed() # Get key pressed (allows continuous presses)
        handle_movement(key_pressed, player)
        
        
        

        draw_window(player)
    pygame.quit()

if __name__ == '__main__':
    main()