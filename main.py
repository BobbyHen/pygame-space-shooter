import pygame
pygame.font.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
SHIP_WIDTH, SHIP_HEIGHT = 50, 50
WINNING_TEXT_FONT = pygame.font.SysFont('comicsans', 100)
WINNING_TEXT = 'YOU WON!'
AMMO_TEXT_FONT = pygame.font.SysFont('comicsans', 50)

# SPRITES
SHIP_IMAGE = pygame.image.load('assets/ship_G.png')
SHIP_IMAGE_SCALED = pygame.transform.scale(SHIP_IMAGE, (SHIP_WIDTH, SHIP_HEIGHT))
ENEMY_IMAGE = pygame.image.load('assets/satellite_D.png')
ENEMY_IMAGE_SCALED = pygame.transform.scale(ENEMY_IMAGE, (SHIP_WIDTH, SHIP_HEIGHT))
BULLET_VELOCITY = 7
MAX_BULLETS = 10

# CUSTOM EVENTS
ENEMY_HIT = pygame.USEREVENT = 1

def handle_player_movement(key_pressed, player):
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

def handle_shooting(bullets, enemy):
    for bullet in bullets:
        bullet.y -= BULLET_VELOCITY
        if enemy.colliderect(bullet):
            bullets.remove(bullet)
            pygame.event.post(pygame.event.Event(ENEMY_HIT))

        # elif bullet.y <= HEIGHT:
        #     bullets.remove(bullet)

def draw_window(player, bullets, enemy, enemy_health, ammo_count):
    WIN.fill(BLACK)

    if enemy_health == 0: # This check is last
        draw_win_text(WINNING_TEXT)
    else:
        WIN.blit(ENEMY_IMAGE_SCALED, (enemy.x, enemy.y))
        for bullet in bullets:
            pygame.draw.rect(WIN, YELLOW, bullet)
        WIN.blit(SHIP_IMAGE_SCALED, (player.x, player.y))
        draw_ammo_text(ammo_count)
        
    pygame.display.update()

def draw_ammo_text(ammo_count):
    ammo_text = AMMO_TEXT_FONT.render("Ammo " + str(ammo_count), 1, WHITE)
    WIN.blit(ammo_text, (10, 10))
    pygame.display.update()

def draw_win_text(WINNING_TEXT):
    draw_text = WINNING_TEXT_FONT.render(WINNING_TEXT, 1, WHITE)
    WIN.blit(draw_text, (WIDTH // 2 - draw_text.get_width() // 2, HEIGHT // 2 - draw_text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(5000)
    main()

def main():
    clock = pygame.time.Clock()
    player = pygame.Rect(440, 425, SHIP_WIDTH, SHIP_HEIGHT)
    enemy = pygame.Rect(470, 150, SHIP_WIDTH, SHIP_HEIGHT)
    bullets = []
    ammo_count = 10
    # HEALTH
    enemy_health = 3

    run = True
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(player.x + player.width // 2 - 5, player.y + player.height // 2, 10, 20)
                    bullets.append(bullet)
                    ammo_count -= 1
                    print(bullets) # print bullets list

            # Enemy kill logic
            if event.type == ENEMY_HIT:
                print("ENEMY HIT")
                enemy_health -= 1

        key_pressed = pygame.key.get_pressed() # Get key pressed (allows continuous presses)
        handle_player_movement(key_pressed, player)
        handle_shooting(bullets, enemy)

        draw_window(player, bullets, enemy, enemy_health, ammo_count)
    pygame.quit()

if __name__ == '__main__':
    main()