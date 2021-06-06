import pygame
# pygame.font.init()
pygame.init()

# MAIN CONSTANTS
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
SHIP_WIDTH, SHIP_HEIGHT = 50, 50

# FONTS
WINNING_TEXT_FONT = pygame.font.SysFont('comicsans', 100)
WINNING_TEXT = 'YOU WON!'
LOSING_TEXT = "YOU LOSE"
AMMO_TEXT_FONT = pygame.font.SysFont('comicsans', 50)
ENEMY_HEALTH_FONT = pygame.font.SysFont('comicsans', 20)

# SPRITES
SHIP_IMAGE = pygame.image.load('assets/images/ship_G.png')
SHIP_IMAGE_SCALED = pygame.transform.scale(SHIP_IMAGE, (SHIP_WIDTH, SHIP_HEIGHT))
ENEMY_IMAGE = pygame.image.load('assets/images/satellite_D.png')
ENEMY_IMAGE_SCALED = pygame.transform.scale(ENEMY_IMAGE, (SHIP_WIDTH, SHIP_HEIGHT))
BULLET_VELOCITY = 7
MAX_BULLETS = 10

# SOUND EFFECTS
PLAYER_LASER = pygame.mixer.Sound('assets/audio/_sf_laser_18.mp3')
EXPLOSION = pygame.mixer.Sound('assets/audio/_sf_laser_explosion.mp3')

# CUSTOM EVENTS
ENEMY_HIT = pygame.USEREVENT = 1

# FUNCTION HANDLES PLAYER MOVEMENT
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

# FUNCTION HANDLES SOUND
def handle_sound(effect):
    pygame.mixer.Sound.play(effect)

# FUNCTION HANDLES MOVEMENT OF ENEMY
def handle_enemy_movement(enemy, enemy_move): # Needs work!!!!
    if enemy_move == 'right':
        enemy.move_ip(5, 0)
        if enemy.x >= WIDTH - SHIP_WIDTH:
            return 'left'
        return 'right'
    elif enemy_move == 'left':
        enemy.move_ip(-5, 0)
        if enemy.x <= 0:
            return 'right'
        return 'left'

# FUNCTION CONTROLS BULLET LOGIC
def handle_shooting(bullets, enemy):
    for bullet in bullets:
        bullet.y -= BULLET_VELOCITY
        if enemy.colliderect(bullet):
            bullets.remove(bullet)
            pygame.event.post(pygame.event.Event(ENEMY_HIT))

        # elif bullet.y <= HEIGHT:
        #     bullets.remove(bullet)

# FUNCTION HANDLES THE DRAWING MAIN ELEMENTS TO THE WINDOW 
def draw_window(player, bullets, enemy, enemy_health, ammo_count, enemy_health_arr, enemy_health_bar):
    WIN.fill(BLACK)

    if ammo_count == 0 and enemy_health > 0:
        draw_win_text(LOSING_TEXT)
    elif enemy_health == 0:
        draw_win_text(WINNING_TEXT)
    else:
        WIN.blit(ENEMY_IMAGE_SCALED, (enemy.x, enemy.y))
        for bullet in bullets:
            pygame.draw.rect(WIN, YELLOW, bullet)
        WIN.blit(SHIP_IMAGE_SCALED, (player.x, player.y))
        draw_enemy_health(enemy_health, enemy, enemy_health_arr, enemy_health_bar)
        draw_ammo_text(ammo_count)
        
    pygame.display.update()

# FUNCTION DRAWS AMMO INFO
def draw_ammo_text(ammo_count):
    ammo_text = AMMO_TEXT_FONT.render("Ammo " + str(ammo_count), 1, WHITE)
    WIN.blit(ammo_text, (10, 10))
    pygame.display.update()

# FUNCTION DRAWS ENEMY HEALTH BAR
def draw_enemy_health(enemy_health, enemy, enemy_health_arr, enemy_health_bar):
    enemy_health_text = ENEMY_HEALTH_FONT.render("Health " + str(enemy_health), 1, RED)
    # WIN.blit(enemy_health_text, (enemy.x, enemy.y - 10))
    # WIN.blit(e_health_blip, (enemy.x, enemy.y - 10))
    
    pygame.draw.rect(WIN, RED, enemy_health_bar)

    # for blip in enemy_health_arr:
    #     pygame.draw.rect(WIN, RED, blip)

# FUNCTION DRAWS WIN/LOSE MESSAGE
def draw_win_text(text):
    draw_text = WINNING_TEXT_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH // 2 - draw_text.get_width() // 2, HEIGHT // 2 - draw_text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(5000)
    main()

# FUNCTION FOR MAIN GAME LOOP
def main():
    clock = pygame.time.Clock()
    player = pygame.Rect(440, 425, SHIP_WIDTH, SHIP_HEIGHT)
    enemy = pygame.Rect(470, 150, SHIP_WIDTH, SHIP_HEIGHT)
    enemy_move = "right"
    bullets = []
    ammo_count = 10
    # HEALTH
    enemy_health = 3
    enemy_health_arr = []
    print(enemy_health_arr)
    bar_len = SHIP_WIDTH - 5

    run = True
    while run:
        clock.tick(60)
        enemy_health_bar = pygame.Rect(enemy.x, enemy.y - 10, bar_len, 5)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(player.x + player.width // 2 - 5, player.y + player.height // 2, 10, 20) # Spawns a bullet geometric object and centers it at the top of the player ship
                    bullets.append(bullet)
                    handle_sound(PLAYER_LASER)
                    ammo_count -= 1
                    print(bullets) # print bullets list

            # Enemy kill logic
            if event.type == ENEMY_HIT:
                print("ENEMY HIT")
                # enemy_health_arr.pop()
                enemy_health -= 1
                bar_len = bar_len // 3 * 2
                print(enemy_health_arr)

            if enemy_health == 0: # This check is last
                handle_sound(EXPLOSION)

        key_pressed = pygame.key.get_pressed() # Get key pressed (allows continuous presses)
        handle_player_movement(key_pressed, player)
        enemy_move = handle_enemy_movement(enemy, enemy_move) # function returns string representing whether the enemy should move to the right or left
        handle_shooting(bullets, enemy)
        draw_window(player, bullets, enemy, enemy_health, ammo_count, enemy_health_arr, enemy_health_bar)
    pygame.quit()

if __name__ == '__main__':
    main()