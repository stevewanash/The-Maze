"""module handles all players including enemies"""
from game_objects import *
from random import randint, random


class CHR(AnimatedSprite):
    """character class

    Args:
        AnimatedSprite (Class): parent class
    """
    def __init__(self, game, path='resources/sprites/enemy/0.png', pos=(10.5,
                                                                        5.5),
                 scale=0.6, shift=0.38, animation_time=180):
        """initializes the enemy

        Args:
            game (obj): _description_
            path (str, optional): Defaults to 'resources/sprites/enemy/0.png'.
            pos (tuple, optional): Defaults to (10.5, 5.5).
            scale (float, optional): Defaults to 0.6.
            shift (float, optional): Defaults to 0.38.
            animation_time (int, optional): Defaults to 180.
        """
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.attack_images = self.get_images(self.path + '/attack')
        self.death_images = self.get_images(self.path + '/death')
        self.idle_images = self.get_images(self.path + '/idle')
        self.pain_images = self.get_images(self.path + '/pain')
        self.walk_images = self.get_images(self.path + '/walk')

        self.attack_dist = randint(3, 6)
        self.speed = 0.03
        self.size = 20
        self.health = 100
        self.attack_damage = 10
        self.accuracy = 0.15
        self.alive = True
        self.pain = False
        self.ray_cast_value = False
        self.frame_counter = 0
        self.player_search_trigger = False

    def update(self):
        """updates chr instance
        """
        self.check_animation_time()
        self.get_sprite()
        self.run_logic()
        # self.draw_ray_cast()

    def check_wall(self, x, y):
        """checks if wall

        Args:
            x (int): x coordinate
            y (int): y coordinate

        Returns:
            tuple: position on map
        """
        return (x, y) not in self.game.map.world_map

    def check_wall_collision(self, dx, dy):
        """avoids wall collision

        Args:
            dx (int): x displacement
            dy (int): y displacement
        """
        if self.check_wall(int(self.x + dx * self.size), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * self.size)):
            self.y += dy

    def movement(self):
        """facilitates movement
        """
        next_pos = self.game.pathfinding.get_path(self.map_pos,
                                                  self.game.player.map_pos)
        next_x, next_y = next_pos

        if next_pos not in \
                self.game.object_handler.CHR_positions:
            angle = math.atan2(next_y + 0.5 - self.y, next_x + 0.5 - self.x)
            dx = math.cos(angle) * self.speed
            dy = math.sin(angle) * self.speed
            self.check_wall_collision(dx, dy)

    def attack(self):
        """handles attacks
        """
        if self.animation_trigger:
            if random() < self.accuracy:
                self.game.player.get_damage(self.attack_damage)

    def animate_death(self):
        """animates deaths
        """
        if not self.alive:
            if self.game.global_trigger and self.frame_counter\
                  < len(self.death_images) - 1:
                self.death_images.rotate(-1)
                self.image = self.death_images[0]
                self.frame_counter += 1

    def animate_pain(self):
        """animates pain
        """
        self.animate(self.pain_images)
        if self.animation_trigger:
            self.pain = False

    def check_hit_in_CHR(self):
        """checks if hit
        """
        if self.ray_cast_value and self.game.player.shot:
            if HALF_WIDTH - self.sprite_half_width < self.screen_x <\
                  HALF_WIDTH + self.sprite_half_width:
                self.game.player.shot = False
                self.pain = True
                self.health -= self.game.weapon.damage
                self.check_health()

    def check_health(self):
        """checks health status
        """
        if self.health < 1:
            self.alive = False

    def run_logic(self):
        """runs different functions
        """
        if self.alive:
            self.ray_cast_value = self.ray_cast_player_CHR()
            self.check_hit_in_CHR()

            if self.pain:
                self.animate_pain()

            elif self.ray_cast_value:
                self.player_search_trigger = True

                if self.dist < self.attack_dist:
                    self.animate(self.attack_images)
                    self.attack()
                else:
                    self.animate(self.walk_images)
                    self.movement()

            elif self.player_search_trigger:
                self.animate(self.walk_images)
                self.movement()

            else:
                self.animate(self.idle_images)
        else:
            self.animate_death()

    @property
    def map_pos(self):
        """returns map positions

        Returns:
            tuple: position
        """
        return int(self.x), int(self.y)

    def ray_cast_player_CHR(self):
        """ray casts the enemy

        Returns:
            Boolean: true if within map, false if not
        """
        if self.game.player.map_pos == self.map_pos:
            return True

        wall_dist_v, wall_dist_h = 0, 0
        player_dist_v, player_dist_h = 0, 0

        ox, oy = self.game.player.pos
        x_map, y_map = self.game.player.map_pos

        ray_angle = self.theta

        sin_a = math.sin(ray_angle)
        cos_a = math.cos(ray_angle)

        # horizontals
        y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)

        depth_hor = (y_hor - oy) / sin_a
        x_hor = ox + depth_hor * cos_a

        delta_depth = dy / sin_a
        dx = delta_depth * cos_a

        for i in range(MAX_DEPTH):
            tile_hor = int(x_hor), int(y_hor)
            if tile_hor == self.map_pos:
                player_dist_h = depth_hor
                break
            if tile_hor in self.game.map.world_map:
                wall_dist_h = depth_hor
                break
            x_hor += dx
            y_hor += dy
            depth_hor += delta_depth

        # verticals
        x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)

        depth_vert = (x_vert - ox) / cos_a
        y_vert = oy + depth_vert * sin_a

        delta_depth = dx / cos_a
        dy = delta_depth * sin_a

        for i in range(MAX_DEPTH):
            tile_vert = int(x_vert), int(y_vert)
            if tile_vert == self.map_pos:
                player_dist_v = depth_vert
                break
            if tile_vert in self.game.map.world_map:
                wall_dist_v = depth_vert
                break
            x_vert += dx
            y_vert += dy
            depth_vert += delta_depth

        player_dist = max(player_dist_v, player_dist_h)
        wall_dist = max(wall_dist_v, wall_dist_h)

        if 0 < player_dist < wall_dist or not wall_dist:
            return True
        return False

    def draw_ray_cast(self):
        """draws the ray cast
        """
        pg.draw.circle(self.game.screen, 'red', (100 * self.x, 100 * self.y),
                       15)
        if self.ray_cast_player_CHR():
            pg.draw.line(self.game.screen, 'orange',
                         (100 * self.game.player.x, 100 * self.game.player.y),
                         (100 * self.x, 100 * self.y), 2)


class Enemy(CHR):
    """enemy class

    Args:
        CHR (Class): parent class
    """
    def __init__(self, game, path='resources/sprites/enemy/0.png', pos=(10.5,
                                                                        5.5),
                 scale=0.6, shift=0.38, animation_time=180):
        """initializes enemy class

        Args:
            game (obj): game instance
            path (str, optional): Defaults to 'resources/sprites/enemy/0.png'.
            pos (tuple, optional): Defaults to (10.5, 5.5).
            scale (float, optional): Defaults to 0.6.
            shift (float, optional): Defaults to 0.38.
            animation_time (int, optional): Defaults to 180.
        """
        super().__init__(game, path, pos, scale, shift, animation_time)
