import pygame
import pytmx
import pyscroll
import json

from npc import NPC
from data import DATA


class Map:
    def __init__(self, screen):
        self.screen = screen
        self.player = None

        self.map_name = "Saint-Rémy"
        self.tmx_data = None
        self.map_layer = None
        self.group = None

        self.collisions = []
        self.spawns = []
        self.switches = []
        self.npcs = []
        self.items = {}

        self.gate = None

        self.map_zoom = 4

        self.rest = False
        self.counter = 0
        self.current_dialogs = []

        self.load_data()

    def save(self):
        data = self.map_name
        with open("../save/map.json", "w") as file:
            json.dump(data, file)

    def load_data(self):
        with open("../save/map.json") as file:
            data = json.load(file)
            if data:
                self.map_name = data

    def update(self):
        if not self.rest:
            self.check_interactions()
            self.check_object()

            self.group.update()
            self.group.center(self.player.rect.center)

        self.group.draw(self.screen.display)

    def switch_map(self, map):
        self.map_name = map
        self.tmx_data = pytmx.load_pygame(f"../assets/maps/{self.map_name}.tmx")
        map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.map_layer = pyscroll.BufferedRenderer(map_data, self.screen.display.get_size())
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=50)
        self.map_layer.zoom = self.map_zoom

        self.init_object()

        if self.gate:
            for spawn in self.spawns:
                if spawn["provenance"] == self.gate["destination"] and spawn["port"] == self.gate["port"]:
                    self.add_player(self.player)
                    self.player.position = spawn["position"]
                    if "house" in map:
                        self.player.bike = False

    def init_object(self):
        self.collisions.clear()
        self.spawns.clear()
        self.switches.clear()
        self.npcs.clear()
        self.items.clear()
        DATA.ENTITIES_DESTINATIONS.clear()

        for obj in self.tmx_data.objects:
            if "collision" in obj.type:
                self.collisions.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            if obj.type == "spawn":
                self.spawns.append({"position": pygame.Vector2(obj.x, obj.y),
                                    "provenance": obj.name.split(" ")[1],
                                    "port": obj.name.split(" ")[2]
                                    })
            if obj.type == "switch":
                self.switches.append({"rect": pygame.Rect(obj.x, obj.y, obj.width, obj.height),
                                      "destination": obj.name.split(" ")[1],
                                      "port": obj.name.split(" ")[2]
                                      })
            if obj.type == "npc":
                self.npcs.append(NPC(obj.name, obj.x, obj.y))
                self.add_npc(self.npcs[-1])
            if obj.type == "npc path":
                for npc in self.npcs:
                    if npc.name == obj.name.split(" ")[0]:
                        npc.checkpoints[int(obj.name.split(" ")[1])] = pygame.Rect(obj.x, obj.y, 16, 16)
            if "item" in obj.type:
                self.items[obj.name] = pygame.Rect(obj.x, obj.y, obj.width, obj.height)

    def check_object(self):
        self.player.collision = False

        for collision in self.collisions:
            if self.player.facing_tile.colliderect(collision):
                self.player.collision = True

        for npc in self.npcs:
            npc.collision = False
            if self.player.facing_tile.colliderect(npc.hitbox):
                self.player.collision = True
            if npc.facing_tile.colliderect(self.player.hitbox):
                npc.collision = True

        for switch in self.switches:
            if self.player.hitbox.colliderect(switch["rect"]):
                if self.player.step_progression >= 12:
                    self.gate = switch
                    self.switch_map(switch["destination"])

    def check_interactions(self):
        self.player.stop = False
        for npc in self.npcs:
            if npc.name not in self.player.npcs_encounter:
                if npc.scan_range:
                    if self.player.hitbox.colliderect(npc.scan_rect):
                        self.player.stop = True
                        if not self.player.in_motion:
                            self.player.facing_entity(npc)
                            if not self.player.facing_tile.colliderect(npc.hitbox):
                                npc.move(npc.direction)
                            else:
                                npc.stop = True
                                self.player.interaction = True

        if self.player.interaction:
            for npc in self.npcs:
                if self.player.facing_tile == npc.hitbox:
                    npc.facing_entity(self.player)
                    self.current_dialogs = npc.dialogs
                    if npc.name in self.player.npcs_encounter:
                        if npc.dialogs2:
                            self.current_dialogs = npc.dialogs2
                    npc.scan_range = 0
                    if npc.name not in self.player.npcs_encounter:
                        self.player.npcs_encounter.append(npc.name)
                    if npc.fighter:
                        self.player.opponent = npc
                    self.rest = True

    def add_player(self, player):
        self.player = player
        self.group.add(player)
        self.player.reset_move()

    def add_npc(self, npc):
        self.group.add(npc)
        npc.reset_move()
