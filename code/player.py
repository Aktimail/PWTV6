import pygame
import json

from tool import Tool
from entity import Entity
from pokemon import Pokemon
from move import Move


class Player(Entity):
    def __init__(self, name, spritesheet, x, y, map, inputs_holder, controller):
        super().__init__(name, x, y)
        self.map = map

        self.team = [Pokemon("haxorus", 50, {"moveset": ["dragon_claw", "pound"]}),
                     Pokemon("togekiss", 50),
                     Pokemon("pikachu", 50),
                     Pokemon("garchomp", 50),
                     Pokemon("zekrom", 50),
                     Pokemon("reshiram", 50)]
        self.lead = self.team[0] if self.team else None

        self.inventory = {
            "Items": [],
            "Balls": [],
            "CT & CS": [],
            "Berries": [],
            "Rare Items": []
        }
        self.pokedollars = 0

        self.spritesheet = pygame.image.load(f"../assets/spritesheets/{spritesheet}.png")
        self.spritesheet_walk = self.spritesheet
        self.spritesheet_run = pygame.image.load(f"../assets/spritesheets/{spritesheet}_run.png")
        self.spritesheet_bicycle = pygame.image.load(f"../assets/spritesheets/{spritesheet}_cycle_roll.png")
        self.active_spritesheet = self.spritesheet

        self.image = Tool.split_spritesheet(self.active_spritesheet)[self.direction][self.sprite_idx]
        self.rect = self.image.get_rect()

        self.inputs_holder = inputs_holder
        self.controller = controller

        self.interaction = False
        self.npcs_encounter = []
        self.opponent = None
        self.fighting = False

        self.bike = False

        self.load_data()

    def save_player(self):
        data = {
            "position": (self.position.x, self.position.y),
            "direction": self.direction,
            "team": self.save_team(),
            "inventory": self.inventory,
            "pokedollars": self.pokedollars,
            "npcs encounter": self.npcs_encounter
        }
        with open("../save/player.json", "w") as file:
            json.dump(data, file)

    def save_team(self):
        team_data = []
        for pkmn in self.team:
            team_data.append(
                {
                    "name": pkmn.name,
                    "level": pkmn.level,
                    "gender": pkmn.gender,
                    "ability": pkmn.ability,
                    "moveset": self.save_moves(pkmn),
                    "item": pkmn.item,
                    "ivs": pkmn.ivs,
                    "evs": pkmn.evs,
                    "nature": pkmn.nature,
                    "status": pkmn.status,
                    "exp": pkmn.exp
                }
            )
        return team_data

    @staticmethod
    def save_moves(pkmn):
        moves_data = []
        for move in pkmn.moveset:
            moves_data.append((move.name, move.pp))
        return moves_data

    def load_data(self):
        with open("../save/player.json") as file:
            data = json.load(file)
            if data:
                self.position = pygame.Vector2(data["position"][0], data["position"][1])
                self.direction = data["direction"]
                self.inventory = data["inventory"]
                self.pokedollars = data["pokedollars"]
                self.npcs_encounter = data["npcs encounter"]

                self.team.clear()
                for pkmn in data["team"]:
                    P = Pokemon(pkmn["name"], pkmn["level"])
                    P.gender = pkmn["gender"]
                    P.ability = pkmn["ability"]
                    P.item = pkmn["item"]
                    P.ivs = pkmn["ivs"]
                    P.evs = pkmn["evs"]
                    P.nature = pkmn["nature"]
                    P.status = pkmn["status"]
                    P.exp = pkmn["exp"]
                    P.moveset.clear()
                    for move in pkmn["moveset"]:
                        P.moveset.append(Move(move[0]))
                        P.moveset[-1].pp = move[1]
                    self.team.append(P)
                    self.lead = self.team[0]

    def update(self):
        self.check_inputs()
        self.image = Tool.split_spritesheet(self.active_spritesheet)[self.direction][self.sprite_idx]
        self.rect.midbottom = self.hitbox.midbottom
        super().update()

    def check_inputs(self):
        if not self.in_motion:
            if not self.stop:
                if self.inputs_holder.key_pressed(self.controller["up"]):
                    self.move("up")
                elif self.inputs_holder.key_pressed(self.controller["down"]):
                    self.move("down")
                elif self.inputs_holder.key_pressed(self.controller["left"]):
                    self.move("left")
                elif self.inputs_holder.key_pressed(self.controller["right"]):
                    self.move("right")

            if not self.bike:
                self.switch_walk()

            if self.inputs_holder.key_pressed(self.controller["run"]):
                self.switch_run()

            if self.inputs_holder.key_pressed(self.controller["bike"]):
                self.inputs_holder.remove_key(self.controller["bike"])
                self.switch_bike()

            self.interaction = False
            if self.inputs_holder.key_pressed(self.controller["interact"]):
                self.inputs_holder.remove_key(self.controller["interact"])
                self.interaction = True

    def switch_walk(self):
        if not self.position.x % 2 and not self.position.y % 2:
            self.speed = 1
            self.active_spritesheet = self.spritesheet_walk

    def switch_run(self):
        if not self.bike:
            if self.in_motion:
                self.speed = 2
                self.active_spritesheet = self.spritesheet_run

    def switch_bike(self):
        if "house" not in self.map.map_name:
            if not self.bike:
                self.bike = True
                self.speed = 4
                self.active_spritesheet = self.spritesheet_bicycle
            elif self.bike:
                self.bike = False
                self.speed = 1
                self.active_spritesheet = self.spritesheet_walk
