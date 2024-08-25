import pygame
import json

from tool import Tool
from entity import Entity
from pokemon import Pokemon


class NPC(Entity):
    def __init__(self, name, x, y):
        super().__init__(name, x, y)
        data = json.load(open(f"../assets/json/npcs/{name}.json"))

        self.name = data["dbSymbol"]
        self.klass = data["klass"]

        self.spritesheet = pygame.image.load(f"../assets/spritesheets/{data["spritesheet"]}.png")
        self.active_spritesheet = self.spritesheet

        self.pkmns_mod = data["pkmns_mod"] if "pkmns_mod" in data else None
        self.team = self.init_team(data["team"])
        self.dialogs = data["dialogs"]
        self.dialogs2 = data["dialogs2"] if "dialogs2" in data else None
        self.fighter = data["fighter"] if "fighter" in data else False

        self.direction = data["direction"]
        self.image = Tool.split_spritesheet(self.active_spritesheet)[self.direction][self.sprite_idx]
        self.rect = self.image.get_rect()

        self.scan_range = data["scan"] if "scan" in data else False
        self.scan_rect = pygame.Rect(0, 0, 0, 0)

        self.checkpoints = {1: pygame.Rect(self.position.x, self.position.y, 16, 16)}
        self.checkpoint_idx = 1

    def update(self):
        self.update_scan_rect()
        self.image = Tool.split_spritesheet(self.active_spritesheet)[self.direction][self.sprite_idx]
        self.rect.midbottom = self.hitbox.midbottom
        self.auto_move()
        super().update()

    def update_scan_rect(self):
        if self.scan_range:
            if self.direction == "up":
                self.scan_rect = pygame.Rect(
                    self.position.x, self.position.y - 16 * self.scan_range, 16, 16 * self.scan_range)
            if self.direction == "down":
                self.scan_rect = pygame.Rect(self.position.x, self.position.y + 16, 16, 16 * self.scan_range)
            if self.direction == "right":
                self.scan_rect = pygame.Rect(self.position.x + 16, self.position.y, 16 * self.scan_range, 16)
            if self.direction == "left":
                self.scan_rect = pygame.Rect(
                    self.position.x - 16 * self.scan_range, self.position.y, 16 * self.scan_range, 16)

    def init_team(self, pkmns):
        team = []
        for pkmn in pkmns.items():
            if self.pkmns_mod and pkmn[0] in self.pkmns_mod:
                team.append(Pokemon(pkmn[0], pkmn[1], self.pkmns_mod[pkmn[0]]))
            else:
                team.append(Pokemon(pkmn[0], pkmn[1]))
        return team

    def auto_move(self):
        if not self.stop:
            cc_idx = self.checkpoint_idx
            nc_idx = self.checkpoint_idx + 1

            if nc_idx > len(self.checkpoints):
                nc_idx = 1

            current_checkpoint = self.checkpoints[cc_idx]
            next_checkpoint = self.checkpoints[nc_idx]

            if current_checkpoint.y - next_checkpoint.y > 0:
                self.move("up")
            elif current_checkpoint.y - next_checkpoint.y < 0:
                self.move("down")
            elif current_checkpoint.x - next_checkpoint.x > 0:
                self.move("left")
            elif current_checkpoint.x - next_checkpoint.x < 0:
                self.move("right")

            if self.hitbox.colliderect(next_checkpoint):
                self.checkpoint_idx = nc_idx
