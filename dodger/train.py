from stable_baselines3 import PPO
from game_env import DodgerEnv

env = DodgerEnv(render_mode="human")   

model = PPO("MlpPolicy", env, verbose=1, tensorboard_log="./tb_logs/")
model.learn(total_timesteps=500_000)
model.save("dodger_agent")