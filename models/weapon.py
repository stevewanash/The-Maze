"""_summary_
"""
from game_objects import *


class Weapon(AnimatedSprite):
    """_summary_

    Args:
        AnimatedSprite (_type_): _description_
    """
    def __init__(self, game, path='resources/sprites/weapon_shotgun/0.png',
                 scale=0.4, animation_time=90):
        """_summary_

        Args:
            game (_type_): _description_
            path (str, optional): _description_.\
                 Defaults to 'resources/sprites/weapon_shotgun/0.png'.
            scale (float, optional): _description_. Defaults to 0.4.
            animation_time (int, optional): _description_. Defaults to 90.
        """
        super().__init__(game=game, path=path, scale=scale,
                         animation_time=animation_time)
        self.images = deque(
            [pg.transform.smoothscale(img, (self.image.get_width() * scale,
                                            self.image.get_height() * scale))
             for img in self.images])
        self.weapon_pos = (HALF_WIDTH - self.images[0].get_width() // 2,
                           HEIGHT - self.images[0].get_height())
        self.reloading = False
        self.num_images = len(self.images)
        self.frame_counter = 0
        self.damage = 50

    def animate_shot(self):
        """_summary_
        """
        if self.reloading:
            self.game.player.shot = False
            if self.animation_trigger:
                self.images.rotate(-1)
                self.image = self.images[0]
                self.frame_counter += 1
                if self.frame_counter == self.num_images:
                    self.reloading = False
                    self.frame_counter = 0

    def draw(self):
        """_summary_
        """
        self.game.screen.blit(self.images[0], self.weapon_pos)

    def update(self):
        """_summary_
        """
        self.check_animation_time()
        self.animate_shot()
