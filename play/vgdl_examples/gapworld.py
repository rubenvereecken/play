import pygame
from vgdl.ontology import MovingAvatar, RIGHT


class RightMovingJumpingAvatar(MovingAvatar):
    """
    Only moves and jumps to the right
    """

    @classmethod
    def declare_possible_actions(cls):
        from pygame.locals import K_RIGHT, K_SPACE
        actions = {}
        actions["RIGHT"] = K_RIGHT
        actions["SPACE"] = K_SPACE
        actions["NO_OP"] = 0
        return actions


    def update(self, game):
        from vgdl.core import VGDLSprite
        from pygame.locals import K_SPACE

        VGDLSprite.update(self, game)

        if game.keystate[K_SPACE]:
            x = self.rect.x / game.block_size
            # Jump up to 2 far, but may be less if near end of corridor
            jump_size = min(2, game.width - x - 1)
            self.physics.activeMovement(self, RIGHT, jump_size)
        else:
            action = self._readAction(game)
            self.physics.activeMovement(self, action)
