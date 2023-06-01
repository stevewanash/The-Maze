"""_summary_
"""
import pygame as pg
from settings import *


class ObjectRenderer:
    """_summary_
    """
    def __init__(self, game):
        """_summary_

        Args:
            game (_type_): _description_
        """
        self.game = game
        self.screen = game.screen
        self.wall_textures = self.load_wall_textures()
        self.sky_image = self.get_texture('resources/textures/sky.png',
                                          (WIDTH, HALF_HEIGHT))
        self.sky_offset = 0
        self.blood_screen =\
            self.get_texture('resources/textures/blood_screen.png', RES)
        self.digit_size = 90
        self.digit_images =\
            [self.get_texture(f'resources/textures/digits/{i}.png',
                              [self.digit_size] * 2)
             for i in range(11)]
        self.digits = dict(zip(map(str, range(11)), self.digit_images))

    def draw(self):
        """_summary_
        """
        self.draw_background()
        self.render_game_objects()
        self.draw_player_health()

    def draw_player_health(self):
        """_summary_
        """
        health = str(self.game.player.health)
        for i, char in enumerate(health):
            self.screen.blit(self.digits[char], (i * self.digit_size, 0))
        self.screen.blit(self.digits['10'], ((i + 1) * self.digit_size, 0))

    def player_damage(self):
        """_summary_
        """
        self.screen.blit(self.blood_screen, (0, 0))

    def draw_background(self):
        """_summary_
        """
        self.sky_offset = (self.sky_offset + 4.5 * self.game.player.rel)\
            % WIDTH
        self.screen.blit(self.sky_image, (-self.sky_offset, 0))
        self.screen.blit(self.sky_image, (-self.sky_offset + WIDTH, 0))
        # floor
        pg.draw.rect(self.screen, FLOOR_COLOR, (0, HALF_HEIGHT, WIDTH, HEIGHT))

    def render_game_objects(self):
        """_summary_
        """
        list_objects = sorted(self.game.raycasting.objects_to_render,
                              key=lambda t: t[0], reverse=True)
        for depth, image, pos in list_objects:
            self.screen.blit(image, pos)

    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        """_summary_

        Args:
            path (_type_): _description_
            res (tuple, optional): _description_.\
                 Defaults to (TEXTURE_SIZE, TEXTURE_SIZE).

        Returns:
            _type_: _description_
        """
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)

    def load_wall_textures(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return {
            1: self.get_texture('resources/textures/1.png'),
            2: self.get_texture('resources/textures/2.png'),
            3: self.get_texture('resources/textures/3.png'),
            4: self.get_texture('resources/textures/4.png'),
            5: self.get_texture('resources/textures/5.png'),
        }
