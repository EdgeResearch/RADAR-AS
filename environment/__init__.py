from gym.envs.registration import register
from netlogo.simulation_parameters import NetlogoSimulationParameters

register(
    id='fakenewsdetection',
    entry_point='fakenewsdetection.environment:fake_news_diffusion_env',
    max_episode_steps=NetlogoSimulationParameters.NumberOfTicks,
)
