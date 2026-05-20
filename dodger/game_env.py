import os 
import math 
import numpy as np 
import pygame 
import gymnasium as gym 
import constants as c 
from character import Character
from utils import load_character_animations


class DodgerEnv(gym.Env):
    metadata = {"render_mode": ["human", "rgb_array"], "render_fps": c.FPS}

    def __init__(self, render_mode=None):
        super().__init__()
        self.render_mode = render_mode 
        
        self.action_space = gym.spaces.Discrete(5)

        self.observation_space = gym.spaces.Box(
            low=np.zeros(6, dtype=np.float32),
            high=np.ones(6, dtype=np.float32),
            dtype=np.float32
        )

        pygame.init()

        if render_mode == "human":
            self.screen = pygame.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
        else:
            os.environ["SDL_VIDEODRIVER"] = "dummy"
            pygame.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
            self.screen = pygame.Surface((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
        
        self.clock = pygame.time.Clock()
        self._load_assets()

    def _load_assets(self):
        self.player_animations = load_character_animations("player", 100, 100, 2)
        self.fly_animations = load_character_animations("fly", 64, 64, 2)
        self.fireball_image = pygame.image.load("assets/images/projectiles/fireball.png").convert_alpha()
        self.font = pygame.font.SysFont("Arial", 30) 
    
    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.player = Character(15*c.TILE_SIZE, 10*c.TILE_SIZE, 100, self.player_animations, 0, c.SCALE)
        self.fly = Character(1*c.TILE_SIZE, 3*c.TILE_SIZE, 100, self.fly_animations, 0, c.SCALE)
        self.fireball_group = pygame.sprite.Group() 
        self.step_count = 0 
        return self._get_obs(), {}
    
    def step(self, action):
        self.step_count += 1

        action_map = {
            0: (0, 0),
            1: (0, -c.MOVEMENT_SPEED),
            2: (0,  c.MOVEMENT_SPEED),
            3: (-c.MOVEMENT_SPEED, 0),
            4: ( c.MOVEMENT_SPEED, 0),
        }
        dx, dy = action_map[int(action)]
        self.player.move(dx, dy)
        self.fly.float(speed=2, mode="horizontal")

        fireball = self.fly.attack(self.fireball_image, self.player)
        if fireball:
            self.fireball_group.add(fireball)

        hp_before = self.player.health
        self.player.update()
        self.fly.update()
        self.fireball_group.update(self.player)
        hp_after = self.player.health  

        terminated = not self.player.alive
        truncated = self.step_count >= 2000

        hit_penalty = (hp_before - hp_after)

        if self.fireball_group:
            fb = min(self.fireball_group, key=lambda f: math.hypot(
                f.rect.centerx - self.player.rect.centerx,
                f.rect.centery - self.player.rect.centery
            ))
            dist = math.hypot(fb.rect.centerx - self.player.rect.centerx,
                            fb.rect.centery - self.player.rect.centery)
            safety_bonus = dist / math.hypot(c.SCREEN_WIDTH, c.SCREEN_HEIGHT)
        else:
            safety_bonus = 1

        reward = -100.0 if terminated else 1 + safety_bonus - hit_penalty * 5

        if self.render_mode == "human":
            self._render_frame()

        return self._get_obs(), reward, terminated, truncated, {}

    
    def _get_obs(self):
        W, H = c.SCREEN_WIDTH, c.SCREEN_HEIGHT
        # Nearest fireball (or screen centre if none)
        if self.fireball_group:
            fb = min(self.fireball_group, key=lambda f: abs(f.rect.centerx - self.player.rect.centerx))
            fb_x, fb_y = fb.rect.centerx / W, fb.rect.centery / H
        else:
            fb_x, fb_y = 0.5, 0.5
        return np.array([
            self.player.rect.centerx / W,
            self.player.rect.centery / H,
            self.fly.rect.centerx / W,
            self.fly.rect.centery / H,
            fb_x,
            fb_y,
        ], dtype=np.float32)

    def render(self):
        if self.render_mode == "rgb_array":
            return self._render_frame()

    def _render_frame(self):
        self.screen.fill(c.BG_COLOR)
        self.player.draw(self.screen)
        self.fly.draw(self.screen)
        health_text = self.font.render(f"HP: {self.player.health}", True, "white")
        self.screen.blit(health_text, (10, 10))
        
        for fb in self.fireball_group:
            fb.draw(self.screen)
        if self.render_mode == "human":
            pygame.display.flip()
            # self.clock.tick(c.FPS)
        else:
            return np.transpose(pygame.surfarray.array3d(self.screen), axes=(1, 0, 2))

    def close(self):
        pygame.quit()

