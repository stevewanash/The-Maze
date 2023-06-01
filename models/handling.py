"""_summary_
"""
from game_objects import *
from characters import *
from random import choices, randrange


class ObjectHandler:
    """_summary_
    """
    def __init__(self, game):
        """_summary_

        Args:
            game (_type_): _description_
        """
        self.game = game
        self.sprite_list = []
        self.CHR_list = []
        self.CHR_sprite_path = 'resources/sprites/CHR/'
        self.static_sprite_path = 'resources/sprites/static_sprites/'
        self.anim_sprite_path = 'resources/sprites/animated_sprites/'
        add_sprite = self.add_sprite
        add_CHR = self.add_CHR
        self.CHR_positions = {}

        # spawn CHR
        self.enemies = 20  # CHR count
        self.CHR_types = [Enemy]
        self.weights = [70]
        self.restricted_area = {(i, j) for i in range(10) for j in range(10)}
        self.spawn_CHR()

        # sprite map
        add_sprite(AnimatedSprite(game))
        add_sprite(AnimatedSprite(game, pos=(1.5, 1.5)))
        add_sprite(AnimatedSprite(game, pos=(1.5, 7.5)))
        add_sprite(AnimatedSprite(game, pos=(5.5, 3.25)))
        add_sprite(AnimatedSprite(game, pos=(5.5, 4.75)))
        add_sprite(AnimatedSprite(game, pos=(7.5, 2.5)))
        add_sprite(AnimatedSprite(game, pos=(7.5, 5.5)))
        add_sprite(AnimatedSprite(game, pos=(14.5, 1.5)))
        add_sprite(AnimatedSprite(game, pos=(14.5, 4.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path +
                                  'red_light/0.png', pos=(14.5, 5.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path +
                                  'red_light/0.png', pos=(14.5, 7.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path +
                                  'red_light/0.png', pos=(12.5, 7.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path +
                                  'red_light/0.png', pos=(9.5, 7.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path +
                                  'red_light/0.png', pos=(14.5, 12.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path +
                                  'red_light/0.png', pos=(9.5, 20.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path +
                                  'red_light/0.png', pos=(10.5, 20.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path +
                                  'red_light/0.png', pos=(3.5, 14.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path +
                                  'red_light/0.png', pos=(3.5, 18.5)))
        add_sprite(AnimatedSprite(game, pos=(14.5, 24.5)))
        add_sprite(AnimatedSprite(game, pos=(14.5, 30.5)))
        add_sprite(AnimatedSprite(game, pos=(1.5, 30.5)))
        add_sprite(AnimatedSprite(game, pos=(1.5, 24.5)))

        # CHR map
        # add_CHR(SoldierCHR(game, pos=(11.0, 19.0)))
        # add_CHR(SoldierCHR(game, pos=(11.5, 4.5)))
        # add_CHR(SoldierCHR(game, pos=(13.5, 6.5)))
        # add_CHR(SoldierCHR(game, pos=(2.0, 20.0)))
        # add_CHR(SoldierCHR(game, pos=(4.0, 29.0)))
        # add_CHR(CacoDemonCHR(game, pos=(5.5, 14.5)))
        # add_CHR(CacoDemonCHR(game, pos=(5.5, 16.5)))
        # add_CHR(CyberDemonCHR(game, pos=(14.5, 25.5)))

    def spawn_CHR(self):
        """_summary_
        """
        for i in range(self.enemies):
            CHR = choices(self.CHR_types, self.weights)[0]
            pos = x, y = randrange(self.game.map.cols),\
                randrange(self.game.map.rows)
            while (pos in self.game.map.world_map) or (pos in
                                                       self.restricted_area):
                pos = x, y = randrange(self.game.map.cols),\
                    randrange(self.game.map.rows)
            self.add_CHR(CHR(self.game, pos=(x + 0.5, y + 0.5)))

    def check_win(self):
        """_summary_
        """
        if not len(self.CHR_positions):
            pg.display.flip()
            pg.time.delay(1500)
            self.game.new_game()

    def update(self):
        """_summary_
        """
        self.CHR_positions = {CHR.map_pos for CHR in
                              self.CHR_list if CHR.alive}
        [sprite.update() for sprite in self.sprite_list]
        [CHR.update() for CHR in self.CHR_list]
        self.check_win()

    def add_CHR(self, CHR):
        """_summary_

        Args:
            CHR (_type_): _description_
        """
        self.CHR_list.append(CHR)

    def add_sprite(self, sprite):
        """_summary_

        Args:
            sprite (_type_): _description_
        """
        self.sprite_list.append(sprite)
