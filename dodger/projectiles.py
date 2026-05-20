import math
import pygame 
import constants as c 

class Projectile(pygame.sprite.Sprite):
    def __init__(self, image, x, y, target_x, target_y):
        super().__init__()
        self.original_image = image 
        x_dist = target_x - x 
        y_dist = target_y - y
        self.angle = math.degrees(math.atan2(y_dist, x_dist))
        
        self.image = pygame.transform.rotate(self.original_image, self.angle-90)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        # calculate horizontal and vertical speeds based on the angle 
        # self.dx = math.cos(math.radians(self.angle)) * c.FIREBALL_SPEED 
        # self.dy = (math.sin(math.radians(self.angle)) * c.FIREBALL_SPEED)
        angle = math.atan2(y_dist, x_dist)
        self.dx = math.cos(angle) * c.FIREBALL_SPEED
        self.dy = math.sin(angle) * c.FIREBALL_SPEED

    def update(self, player):
        damage = 10 
        self.rect.x += self.dx
        self.rect.y += self.dy 

        if self.rect.right < 0 or self.rect.left > c.SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > c.SCREEN_HEIGHT:
            self.kill() 
        
        if player.rect.colliderect(self.rect) and player.hit == False:
            player.last_hit = pygame.time.get_ticks() 
            player.health -= damage  
            self.kill() 
    
    def draw(self, surface):
        surface.blit(self.image, (self.rect.centerx - int(self.image.get_width()/2), (self.rect.centery - int(self.image.get_height()/2))))
        
