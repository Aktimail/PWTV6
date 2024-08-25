import pygame

from pokemon import Pokemon
from data import DATA


class Entity(pygame.sprite.Sprite):
    def __init__(self, name, x, y):
        super().__init__()

        self.name = name
        self.spritesheet = None
        self.active_spritesheet = None
        self.position = pygame.math.Vector2(x, y)

        self.in_motion = False
        self.reserve_next_tile = True
        self.direction = "down"
        self.step_progression = 0
        self.speed = 1
        self.facing_tile = pygame.Rect(0, 0, 16, 16)
        self.stop = False

        self.still_counter = 0

        self.sprite_idx = 0
        self.anim_cycle = 0

        self.collision = False

        self.hitbox = pygame.Rect(0, 0, 16, 16)

        self.pkmn_mods = None
        self.team = []
        self.lead = None

    def update(self):
        self.hitbox.topleft = self.position
        self.movement_update()
        self.facing_tile_update()
        self.animation_cycle()

    def reset_move(self):
        self.in_motion = False
        self.step_progression = 0
        while self.position.x % 16:
            self.position.x -= 1
        while self.position.y % 16:
            self.position.y -= 1

    def move(self, direction):
        if not self.in_motion:
            if self.direction == direction:
                if not self.collision:
                    if self.grid_check():
                        self.in_motion = True
            else:
                self.direction = direction

    def movement_update(self):
        if self.in_motion:
            self.step_progression += self.speed
            if self.direction == "left":
                self.position.x -= self.speed
            elif self.direction == "right":
                self.position.x += self.speed
            elif self.direction == "up":
                self.position.y -= self.speed
            elif self.direction == "down":
                self.position.y += self.speed

            if self.step_progression >= 16:
                self.step_progression = 0
                self.in_motion = False

    def animation_cycle(self):
        if self.in_motion:
            self.still_counter = 0
            self.anim_cycle += 1
            if not self.anim_cycle % 8:
                self.sprite_idx += 1

            if self.sprite_idx > 3:
                self.sprite_idx = 0
            if self.anim_cycle >= 16:
                self.anim_cycle = 0

        if not self.in_motion:
            self.still_counter += 1
        if self.still_counter >= 2:
            if self.sprite_idx % 2:
                self.sprite_idx += 1
                if self.sprite_idx > 3:
                    self.sprite_idx = 0
            self.still_counter = 0

    def facing_tile_update(self):
        self.facing_tile.topleft = self.position
        if self.direction == "left":
            self.facing_tile.x -= 16
        if self.direction == "right":
            self.facing_tile.x += 16
        if self.direction == "up":
            self.facing_tile.y -= 16
        if self.direction == "down":
            self.facing_tile.y += 16

    def facing_entity(self, entity):
        if not self.in_motion:
            if entity.position.x - self.position.x > 0:
                self.direction = "right"
            if entity.position.x - self.position.x < 0:
                self.direction = "left"
            if entity.position.y - self.position.y > 0:
                self.direction = "down"
            if entity.position.y - self.position.y < 0:
                self.direction = "up"

    def grid_check(self):
        if not (self.facing_tile.x, self.facing_tile.y) in DATA.ENTITIES_DESTINATIONS.values():
            DATA.ENTITIES_DESTINATIONS[self.name] = (self.facing_tile.x, self.facing_tile.y)
            return True
        return False

    def init_team(self, pkmns):
        team = []
        for pkmn in pkmns.items():
            if self.pkmn_mods and pkmn[0] in self.pkmn_mods:
                team.append(Pokemon(pkmn[0], pkmn[1], self.pkmn_mods[pkmn[0]]))
            else:
                team.append(Pokemon(pkmn[0], pkmn[1]))
        return team

    def attack(self, move, opp):
        self.lead.attack(move, opp.lead)

    def switch(self, pkmn):
        self.lead.boosts = {"atk": 0, "deff": 0, "aspe": 0, "dspe": 0, "spd": 0}
        self.team[0], self.team[pkmn] = self.team[pkmn], self.team[0]
        self.lead = self.team[0]
