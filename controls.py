import itertools
import numpy as np


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
        tuple(): 'NOOP',
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


ATARI_ACTION_TO_KEYS = { v: k for k, v in KEYS_TO_ATARI_ACTION.items() }


class Controls:
    def __init__(self):
        self.action = 0
        self.restart = False
        self.pause = False


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
            return self.perform_noop()
        # Up to 3 buttons active at a time,
        # so see if there is any known combination for an Atari action
        for num_keys in range(max(3, len(active_keys)), 0, -1):
            for key_combo in itertools.combinations(active_keys, num_keys):
                key_combo = frozenset(key_combo)
                if key_combo in self.keys_to_action:
                    return self.keys_to_action[key_combo]
        logger.debug('Combo not recognized:', active_keys)
        return self.perform_noop()


class AtariControls(Controls):
    def __init__(self, action_selection):
        super().__init__()
        # action_selection should be list of keys corresponding to AtariActions
        self.activated = { key: False for name, key in vars(Keys).items() \
                if not name.startswith('__') or name in ['RETURN', 'ESCAPE'] }

        self.available_actions = dict(zip(action_selection, range(len(action_selection))))
        self.keys_to_action = { ATARI_ACTION_TO_KEYS[name]: code for name, code in \
                self.available_actions.items()}


    def perform_noop(self):
        return self.available_actions['NOOP']
