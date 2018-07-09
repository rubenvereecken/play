#!/usr/bin/env python

def list_envs():
    import gym
    import gym_vgdl
    env_names = list(gym.envs.registry.env_specs.keys())
    return env_names


if __name__ == '__main__':
    envs = list_envs()
    for env in envs:
        print(env)
