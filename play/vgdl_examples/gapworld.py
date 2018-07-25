import pygame
from vgdl.ontology import MovingAvatar, RIGHT


class RightMovingJumpingAvatar(MovingAvatar):
    """
    Only moves and jumps to the right
    """

    @classmethod
    def declare_possible_actions(cls):
        # TODO port
        from vgdl.core import Action
        from pygame.locals import K_RIGHT, K_SPACE
        actions = {}
        actions["RIGHT"] = Action(K_RIGHT)
        actions["SPACE"] = Action(K_SPACE)
        actions["NO_OP"] = Action()
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
            action = action.as_force()
            self.physics.activeMovement(self, action)
