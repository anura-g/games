import math 
import pygame 
import projectiles 
import constants as c 

class Character():
    def __init__(self, x, y, health, animation_list, char_type, size):
        self.char_type = char_type 
        self.running = False  
        self.flip = False 
        self.update_time = pygame.time.get_ticks() 
        self.animation_list = animation_list[char_type] 
        self.frame_index = 0
        self.action = 0; # 0:idle, 1:run
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = pygame.Rect(x, y, c.TILE_SIZE * size, 40 * size)
        self.float_direction = 1 
        self.hit = False 
        self.alive = True 
        # self.last_hit = pygame.time.get_ticks()
        self.last_attack = pygame.time.get_ticks()
        self.health = health 
        
    
    def move(self, dx, dy):
        self.running = False 

        if dx!=0 or dy!=0:
            self.running = True 
        if dx<0:
            self.flip = True 
        if dx>0:
            self.flip = False 
        
        # diagonal speed check
        if dx != 0 and dy != 0:
            dx = dx * (math.sqrt(2) / 2)
            dy = dy * (math.sqrt(2) / 2)
        
        if self.char_type == 0:
            self.rect.x += dx 
            self.rect.y += dy 


    def float(self, speed, mode=("vertical", "horizontal")):
        max_y = c.SCREEN_HEIGHT - 100 
        min_y = 100

        max_x = c.SCREEN_WIDTH - 200
        min_x = 100

        if mode == "vertical":
            self.rect.y += speed * self.float_direction

            if self.rect.y >= max_y:
                self.rect.y = max_y 
                self.flip = True
                self.float_direction = -1 
            elif self.rect.y <= min_y:
                self.rect.y = min_y 
                self.float_direction = 1
                self.flip = False 
        
        if mode == "horizontal":
            self.rect.x += speed * self.float_direction
            if self.rect.x >= max_x:
                self.rect.x = max_x 
                self.float_direction = -1 
                self.flip = False 
            elif self.rect.x <= min_x:
                self.rect.x = min_x 
                self.float_direction = 1
                self.flip = True         



    def attack(self, projectile_image, player):
        if self.alive:
            attack_cooldown = 500 
            projectile = None 
            if pygame.time.get_ticks() - self.last_attack >= attack_cooldown:
                projectile = projectiles.Projectile(projectile_image, self.rect.centerx, self.rect.centery, player.rect.centerx, player.rect.centery)
                self.last_attack = pygame.time.get_ticks()   
        

        return projectile 


    def update(self):

        if self.health <= 0:
            self.health = 0
            self.alive = False 

        # Handle animation
        if self.running == True:
            self.update_action(1) # run 
        if self.running == False:
            self.update_action(0) # idle 
        
        animation_cooldown = 70

        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks() 
        
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0
        
        self.image = self.animation_list[self.action][self.frame_index]


    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action 
            # update animation settings 
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
    
    def draw(self, surface):
        flipped_image = pygame.transform.flip(self.image, self.flip, False)
        flipped_image.set_colorkey((0, 0, 0))
        if self.char_type == 0:
            surface.blit(flipped_image, (self.rect.x, self.rect.y - c.SCALE*c.OFFSET))
        else:
            surface.blit(flipped_image, (self.rect.x, self.rect.y))
