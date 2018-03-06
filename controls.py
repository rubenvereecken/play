import itertools
import numpy as np
import logging
logger = logging.getLogger(__name__)


class PygletKeys:
    RETURN = 0xff00 + 13
    SPACE = 32
    ESCAPE = 0xff00 + 27

    LEFT = 0xff00 + 81
    UP = 0xff00 + 82
    RIGHT = 0xff00 + 83
    DOWN = 0xff00 + 84


KEYS_TO_ATARI_ACTION = {
        tuple(): 'NOOP',
        (PygletKeys.SPACE,): 'FIRE',
        (PygletKeys.RIGHT,): 'RIGHT', (PygletKeys.LEFT,): 'LEFT',
        (PygletKeys.DOWN,): 'DOWN', (PygletKeys.UP,): 'UP',
        (PygletKeys.UP, PygletKeys.RIGHT): 'UPRIGHT',
        (PygletKeys.UP, PygletKeys.LEFT): 'UPLEFT',
        (PygletKeys.DOWN, PygletKeys.RIGHT): 'DOWNRIGHT',
        (PygletKeys.DOWN, PygletKeys.LEFT): 'DOWNLEFT',
}

for k, v in list(KEYS_TO_ATARI_ACTION.items()):
    KEYS_TO_ATARI_ACTION[frozenset(k)] = v
    # Append FIRE to all the possible combinations
    if v != 'FIRE':
        KEYS_TO_ATARI_ACTION[frozenset(k + (PygletKeys.SPACE,))] = v + 'FIRE'


ATARI_ACTION_TO_KEYS = { v: k for k, v in KEYS_TO_ATARI_ACTION.items() }


class Controls:
    def __init__(self):
        self.action = 0
        self.restart = False
        self.pause = False


    def capture_key_presses(self):
        """
        There are two models of processing key presses, depending on visualisation
        framework. Pyglet uses event based, PyGame seems to favor manually
        checking what's pressed.
        """


    @property
    def current_action(self):
        active_keys = [key for key, active in self.activated.items() if active]
        # Up to 3 buttons active at a time, at least 0,
        # so see if there is any known combination for an Atari action
        for num_keys in range(max(3, len(active_keys)), -1, -1):
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
        self.available_actions = dict(zip(action_selection, range(len(action_selection))))
        # Maps a key combo to a Gym action (an action index)
        self.keys_to_action = { ATARI_ACTION_TO_KEYS[name]: code for name, code in \
                self.available_actions.items()}

        # Dict to keep tracked of pressed keys
        self.activated = { key: False for name, key in vars(PygletKeys).items() \
                if not name.startswith('__') or name in ['RETURN', 'ESCAPE'] }


    def on_key_press(self, key, mod):
        if key == PygletKeys.RETURN:
            self.restart = True
        elif key == PygletKeys.ESCAPE:
            self.pause = not self.pause
        elif key in self.activated:
            self.activated[key] = True


    def on_key_release(self, key, mod):
        if key in self.activated:
            self.activated[key] = False


    def perform_noop(self):
        return self.available_actions['NOOP']


import pygame

class PygameKeys:
    RETURN = pygame.K_RETURN
    SPACE = pygame.K_SPACE
    ESCAPE = pygame.K_ESCAPE

    LEFT = pygame.K_LEFT
    UP = pygame.K_UP
    RIGHT = pygame.K_RIGHT
    DOWN = pygame.K_DOWN


KEYS_TO_VGDL_ACTION = {
        # Note how this noop is spelled different from the Atari one
        tuple(): 'NO_OP',
        (PygameKeys.SPACE,): 'SPACE',
        (PygameKeys.RIGHT,): 'RIGHT', (PygameKeys.LEFT,): 'LEFT',
        (PygameKeys.DOWN,): 'DOWN', (PygameKeys.UP,): 'UP',
}

for k, v in list(KEYS_TO_VGDL_ACTION.items()):
    KEYS_TO_VGDL_ACTION[frozenset(k)] = v

VGDL_ACTION_TO_KEYS = { v: k for k, v in KEYS_TO_VGDL_ACTION.items() }


class VGDLControls(Controls):
    def __init__(self, action_selection):
        super().__init__()
        # action_selection should be list of keys corresponding to VGDL actions
        self.available_actions = dict(zip(action_selection, range(len(action_selection))))
        # Maps a key combo to a Gym action (an action index)
        self.keys_to_action = { VGDL_ACTION_TO_KEYS[name]: code for name, code in \
                self.available_actions.items()}

        # Dict to keep tracked of pressed keys
        self.activated = { key: False for name, key in vars(PygameKeys).items() \
                if not name.startswith('__') or name in ['RETURN', 'ESCAPE'] }


    def capture_key_presses(self):
        keys = pygame.key.get_pressed()

        for k, v in self.activated.items():
            self.activated[k] = keys[k]


    def perform_noop(self):
        return self.available_actions['NO_OP']
