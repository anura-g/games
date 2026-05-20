import pygame 
import constants as c 
from character import Character 
from utils import load_character_animations

pygame.init() 
screen = pygame.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
background = pygame.Surface(screen.get_size())
ui_layer = pygame.Surface(screen.get_size(), pygame.SRCALPHA)

pygame.display.set_caption(c.GAME_TITLE)

clock = pygame.time.Clock() 


player_animations = load_character_animations("player", 100, 100, 2)
fly_animations = load_character_animations("fly", 64, 64, 2) 
fireball_image = pygame.image.load("assets/images/projectiles/fireball.png").convert_alpha() 


player = Character(15*c.TILE_SIZE, 10*c.TILE_SIZE, 100, player_animations, 0, c.SCALE)
fly = Character(1*c.TILE_SIZE, 3*c.TILE_SIZE, 100, fly_animations, 0, c.SCALE) 

# create sprite groups 
fireball_group = pygame.sprite.Group()

running = True
while running: 
    clock.tick(c.FPS)
    background.fill(c.BG_COLOR)

    if player.alive:
        # Movements 
        keys = pygame.key.get_pressed()
        dx = (keys[pygame.K_d] - keys[pygame.K_a]) * c.MOVEMENT_SPEED
        dy = (keys[pygame.K_s] - keys[pygame.K_w]) * c.MOVEMENT_SPEED
        
        player.move(dx, dy)
        fly.float(speed=2, mode="horizontal")

        # Updates
        fireball = fly.attack(fireball_image, player)
        if fireball:
            fireball_group.add(fireball)

        player.update()
        fly.update()
        fireball_group.update(player)
    
    else:
        running = False 

    

    # Draw 
    screen.blit(background, (0, 0))
    player.draw(screen)
    fly.draw(screen)
    # health 
    # draw health
    font = pygame.font.SysFont("Arial", 30)
    health_text = font.render(f"HP: {player.health}", True, "white")
    screen.blit(health_text, (10, 10))

    for fireball in fireball_group:
        fireball.draw(screen)

    for x in range(1, c.SCREEN_WIDTH // c.TILE_SIZE):
        pygame.draw.line(screen, "white", (0, c.SCREEN_HEIGHT // c.TILE_SIZE * x), (c.SCREEN_WIDTH, c.SCREEN_HEIGHT // c.TILE_SIZE * x))
        pygame.draw.line(screen, "white", (c.SCREEN_WIDTH // c.TILE_SIZE * x, 0), (c.SCREEN_WIDTH // c.TILE_SIZE * x, c.SCREEN_HEIGHT))

    # Event Handler 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_ESCAPE:
                running = False
        
    pygame.display.update()


pygame.quit()