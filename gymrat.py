import sys
import time
import itertools
import numpy as np
import argparse

import gym
from gym_recording.wrappers import TraceRecordingWrapper


class Keys:
    RETURN = 0xff00 + 13
    SPACE = 32
    ESCAPE = 0xff00 + 27

    LEFT = 0xff00 + 81
    UP = 0xff00 + 82
    RIGHT = 0xff00 + 83
    DOWN = 0xff00 + 84

# AA = AtariActions
KEYS_TO_ATARI_ACTION = {
        (Keys.SPACE,): 'FIRE',
        (Keys.RIGHT,): 'RIGHT', (Keys.LEFT,): 'LEFT',
        (Keys.DOWN,): 'DOWN', (Keys.UP,): 'UP',
        (Keys.UP, Keys.RIGHT): 'UPRIGHT',
        (Keys.UP, Keys.LEFT): 'UPLEFT',
        (Keys.DOWN, Keys.RIGHT): 'DOWNRIGHT',
        (Keys.DOWN, Keys.LEFT): 'DOWNLEFT',
}

for k, v in list(KEYS_TO_ATARI_ACTION.items()):
    KEYS_TO_ATARI_ACTION[frozenset(k)] = v
    # Append FIRE to all the possible combinations
    if v != 'FIRE':
        KEYS_TO_ATARI_ACTION[frozenset(k + (Keys.SPACE,))] = v + 'FIRE'


class AtariControls:
    def __init__(self, action_selection):
        # action_selection should be list of keys corresponding to AtariActions
        self.action = 0
        self.restart = False
        self.pause = False
        self.activated = { key: False for name, key in vars(Keys).items() \
                if not name.startswith('__') or name in ['RETURN', 'ESCAPE'] }

        self.available_actions = dict(zip(action_selection, range(len(action_selection))))
        print(self.available_actions)


    def on_key_press(self, key, mod):
        if key == Keys.RETURN:
            self.restart = True
        elif key == Keys.ESCAPE:
            self.pause = not self.pause
        elif key in self.activated:
            self.activated[key] = True


    def on_key_release(self, key, mod):
        if key in self.activated:
            self.activated[key] = False


    @property
    def current_action(self):
        active_keys = [key for key, active in self.activated.items() if active]
        if (len(active_keys)) == 0:
            # return AtariActions.NOOP
            return self.available_actions['NOOP']
        # Up to 3 buttons active at a time,
        # so see if there is any known combination for an Atari action
        for num_keys in range(max(3, len(active_keys)), 0, -1):
            for key_combo in itertools.combinations(active_keys, num_keys):
                key_combo = frozenset(key_combo)
                if key_combo in KEYS_TO_ATARI_ACTION and \
                        KEYS_TO_ATARI_ACTION[key_combo] in self.available_actions:
                    return self.available_actions[KEYS_TO_ATARI_ACTION[key_combo]]
        print('Combo not recognized:', active_keys)
        # return AtariActions.NOOP
        return self.available_actions['NOOP']


class HumanAtariController:
    def __init__(self, env_name=None):
        self.env_name = env_name
        self.env = gym.make(env_name)
        self.env = TraceRecordingWrapper(self.env)
        print(self.env.directory)
        self.env.render(mode='human')
        self.controls = AtariControls(self.env.unwrapped.get_action_meanings())
        self.window = self.env.unwrapped.viewer.window
        self.window.on_key_press = self.controls.on_key_press
        self.window.on_key_release = self.controls.on_key_release
        self.fps = 30

        self.cum_reward = 0



    def play(self):
        # TODO needed?
        self.env.reset()


        for step_i in itertools.count():
            obs, reward, done, info = self.env.step(self.controls.current_action)
            if reward:
                print("reward %0.3f" % reward)

            self.cum_reward += reward
            window_open = self.env.render()

            if not window_open:
                print('Window closed')
                return False

            if done:
                print('Done')
                break

            if self.controls.restart:
                print('Requested restart')
                break

            while self.controls.pause:
                self.env.render()
                time.sleep(1. / self.fps)

            time.sleep(1. / self.fps)




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('env_name', type=str)

    args = parser.parse_args()

    controller = HumanAtariController(args.env_name)
    controller.play()

