import pygame 
from stable_baselines3 import PPO
from game_env import DodgerEnv

model = PPO.load("dodger_agent", device='cpu')
env = DodgerEnv(render_mode="human")

obs, _ = env.reset()
while True:
    action, _ = model.predict(obs, deterministic=True)
    obs, reward, terminated, truncated, _ = env.step(action)
    env.render()

    # Handle quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            env.close()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                env.close()
                exit()

    if terminated or truncated:
        obs, _ = env.reset()