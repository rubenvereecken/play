import numpy as np
import gym
import gym.spaces as spaces

class AtariObservationWrapper(gym.Wrapper):
    """
    Meant to make both Atari image and RAM available as observation,
    since the original gym env has you pick
    """

    def __init__(self, env):
        super().__init__(env)

        image_shape = (210, 160, 3)
        image_space = spaces.Box(0, 255, image_shape, np.uint8)
        ram_shape = (128,)
        ram_space = spaces.Box(0, 255, ram_shape, np.uint8)

        self.observation_space = spaces.Tuple((image_space, ram_space))


    def _step(self, action):
        obs, reward, done, info = self.env.step(action)

        new_obs = (self.env.unwrapped._get_image(), self.env.unwrapped._get_ram())
        return new_obs, reward, done, info

    def _reset(self):
        obs = self.env.reset()

        new_obs = (self.env.unwrapped._get_image(), self.env.unwrapped._get_ram())
        return new_obs

