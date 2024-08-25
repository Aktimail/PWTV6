import pygame

from dialogbox import DialogBox
from tool import Tool


class Battle:
    def __init__(self, screen, cursor, player):
        self.screen = screen
        self.cursor = cursor
        self.display = screen.display
        self.player = player
        self.opponent = player.opponent

        self.background = pygame.transform.scale(
            pygame.image.load("../assets/battle/back_grass.png"), self.screen.get_size())

        self.y_oscillation = (0, 5, 10, 5)
        self.y_oscillation_idx = 0
        self.y_osc_idx_adaptator = 0

        self.comments = []

        self.interactive_rect = {}

        self.player_assets = {}
        self.opp_assets = {}

        self.main_menu_assets = {
            "battle": {
                "image": pygame.image.load("../assets/battle/battlebar.png"),
                "size": (80, 80),
                "pos": (1200, 240)
            },
            "team": {
                "image": pygame.image.load("../assets/battle/battlebar.png"),
                "size": (80, 80),
                "pos": (1200, 320)
            },
            "bag": {
                "image": pygame.image.load("../assets/battle/battlebar.png"),
                "size": (80, 80),
                "pos": (1200, 400)
            },
            "run": {
                "image": pygame.image.load("../assets/battle/battlebar.png"),
                "size": (80, 80),
                "pos": (1200, 480)
            }
        }
        battle_assets_size = (190, 80)
        self.battle_menu_assets = {
            "move1": {
                "image": pygame.image.load("../assets/battle/battlebar.png"),
                "size": battle_assets_size,
                "pos": (1005, 240)
            },
            "move2": {
                "image": pygame.image.load("../assets/battle/battlebar.png"),
                "size": battle_assets_size,
                "pos": (1005, 320)
            },
            "move3": {
                "image": pygame.image.load("../assets/battle/battlebar.png"),
                "size": battle_assets_size,
                "pos": (1005, 400)
            },
            "move4": {
                "image": pygame.image.load("../assets/battle/battlebar.png"),
                "size": battle_assets_size,
                "pos": (1005, 480)
            }
        }

        team_assets_size = (120, 80)
        x = 1075 if len(self.player.team) <= 3 else 950
        self.team_menu_assets = {
            "pkmn2": {
                "image": pygame.image.load("../assets/battle/battlebar.png"),
                "size": team_assets_size,
                "pos": (x, 320)
            },
            "pkmn3": {
                "image": pygame.image.load("../assets/battle/battlebar.png"),
                "size": team_assets_size,
                "pos": (x, 400)
            },
            "pkmn4": {
                "image": pygame.image.load("../assets/battle/battlebar.png"),
                "size": team_assets_size,
                "pos": (x, 480)
            },
            "pkmn5": {
                "image": pygame.image.load("../assets/battle/battlebar.png"),
                "size": team_assets_size,
                "pos": (x + 125, 320)
            },
            "pkmn6": {
                "image": pygame.image.load("../assets/battle/battlebar.png"),
                "size": team_assets_size,
                "pos": (x + 125, 400)
            }
        }

        self.dialog_box = DialogBox(self.screen, self.player, "battle_box", (1280, 150), (0, 570))

    def init_player_assets(self):
        self.player_assets = {
            "ground": {
                "image": pygame.image.load("../assets/battle/player/ground.png"),
                "size": (1024, 128),
                "pos": (-50, 442)
            },
            "pokemon": {
                "image": pygame.image.load(self.player.team[0].back_spritesheet),
                "size": (672, 672),
                "pos": [100, self.player.team[0].front_offset_y * 7 - self.y_oscillation[self.y_oscillation_idx]]
            },
            "pkmn_name": {
                "image": None,
                "size": (0, 0),
                "pos": (0, 0)
            },
            "pkmn_lvl": {
                "image": None,
                "size": (0, 0),
                "pos": (0, 0)
            },
            "battlebar": {
                "image": pygame.image.load("../assets/battle/battlebar.png"),
                "size": (275, 80),
                "pos": (0, 480)
            },
            "hp_bar": {
                "image": None,
                "size": (0, 0),
                "pos": (0, 0)
            },
            "hp": {
                "image": self.init_hp_color(self.player.team[0]),
                "size": (int(self.player.team[0].hp / self.player.team[0].max_hp * 276), 12),
                "pos": (0, 0)
            },
            "pokeballs": {
                "image": None,
                "size": (0, 0),
                "pos": (0, 0)
            }
        }

    def init_opp_assets(self):
        self.opp_assets = {
            "ground": {
                "image": pygame.image.load("../assets/battle/opponent/ground.png"),
                "size": (450, 200),
                "pos": (700, 225)
            },
            "pokemon": {
                "image": pygame.image.load(self.opponent.team[0].spritesheet),
                "size": (288, 288),
                "pos": [775, self.opponent.team[0].front_offset_y * 3 + 50]
            },
            "pkmn_name": {
                "image": None,
                "size": (0, 0),
                "pos": (0, 0)
            },
            "pkmn_lvl": {
                "image": None,
                "size": (0, 0),
                "pos": (0, 0)
            },
            "battlebar": {
                "image": pygame.image.load("../assets/battle/battlebar.png"),
                "size": (275, 60),
                "pos": (1005, 5)
            },
            "hp_bar": {
                "image": None,
                "size": (0, 0),
                "pos": (0, 0)
            },
            "hp": {
                "image": self.init_hp_color(self.opponent.team[0]),
                "size": (int(self.opponent.team[0].hp / self.opponent.team[0].max_hp * 276), 12),
                "pos": (0, 30)
            },
            "pokeballs": {
                "image": None,
                "size": (0, 0),
                "pos": (0, 0)
            }
        }

    def blit_main_menu(self):
        for asset in self.main_menu_assets:
            image = self.main_menu_assets[asset]["image"]
            image = pygame.transform.scale(image, self.main_menu_assets[asset]["size"])
            self.display.blit(image, self.main_menu_assets[asset]["pos"])
            self.interactive_rect[asset] = pygame.Rect(self.main_menu_assets[asset]["pos"][0],
                                                       self.main_menu_assets[asset]["pos"][1],
                                                       self.main_menu_assets[asset]["size"][0],
                                                       self.main_menu_assets[asset]["size"][1])

    def blit_battle_menu(self):
        x = 0
        for asset in self.battle_menu_assets:
            x += 1
            if x <= len(self.player.team[0].moveset):
                image = self.battle_menu_assets[asset]["image"]
                image = pygame.transform.scale(image, self.battle_menu_assets[asset]["size"])
                self.display.blit(image, self.battle_menu_assets[asset]["pos"])
                self.interactive_rect[asset] = pygame.Rect(self.battle_menu_assets[asset]["pos"][0],
                                                           self.battle_menu_assets[asset]["pos"][1],
                                                           self.battle_menu_assets[asset]["size"][0],
                                                           self.battle_menu_assets[asset]["size"][1])

    def blit_team_menu(self):
        x = 0
        for asset in self.team_menu_assets:
            x += 1
            if x < len(self.player.team):
                image = self.team_menu_assets[asset]["image"]
                image = pygame.transform.scale(image, self.team_menu_assets[asset]["size"])
                self.display.blit(image, self.team_menu_assets[asset]["pos"])
                self.interactive_rect[asset] = pygame.Rect(self.team_menu_assets[asset]["pos"][0],
                                                           self.team_menu_assets[asset]["pos"][1],
                                                           self.team_menu_assets[asset]["size"][0],
                                                           self.team_menu_assets[asset]["size"][1])

    def blit_player_assets(self):
        self.init_player_assets()
        for asset in self.player_assets:
            if self.player_assets[asset]["image"]:
                image = self.player_assets[asset]["image"]
                image = pygame.transform.scale(image, self.player_assets[asset]["size"])
                self.display.blit(image, self.player_assets[asset]["pos"])

    def blit_opp_assets(self):
        self.init_opp_assets()
        for asset in self.opp_assets:
            if self.opp_assets[asset]["image"]:
                image = self.opp_assets[asset]["image"]
                image = pygame.transform.scale(image, self.opp_assets[asset]["size"])
                self.display.blit(image, self.opp_assets[asset]["pos"])

    def blit_all_assets(self):
        self.interactive_rect.clear()
        self.display.blit(self.background, (0, 0))
        self.blit_opp_assets()
        self.blit_player_assets()
        self.blit_main_menu()

    @staticmethod
    def init_hp_color(pkmn):
        hp_bars = pygame.image.load("../assets/battle/hp.png")
        hp_bars = Tool.split_hp_bars(hp_bars)
        if pkmn.hp == pkmn.max_hp:
            active_bar = hp_bars[-1]
        else:
            active_bar = hp_bars[int((pkmn.hp / pkmn.max_hp) * 6)]
        return active_bar

    def update(self):
        self.blit_all_assets()
        self.check_cursor()
        self.dialog_box.update()

        self.update_oscillation()

    def update_oscillation(self):
        self.y_osc_idx_adaptator += 1
        if self.y_osc_idx_adaptator > 15:
            self.y_osc_idx_adaptator = 0
            self.y_oscillation_idx += 1
            if self.y_oscillation_idx >= len(self.y_oscillation):
                self.y_oscillation_idx = 0

    def check_cursor(self):
        if self.interactive_rect["battle"].collidepoint(self.cursor.position) and self.cursor.button[0]:
            self.blit_battle_menu()
        elif self.interactive_rect["team"].collidepoint(self.cursor.position) and self.cursor.button[0]:
            pass
        elif self.interactive_rect["bag"].collidepoint(self.cursor.position) and self.cursor.button[0]:
            pass
        elif self.interactive_rect["run"].collidepoint(self.cursor.position) and self.cursor.button[0]:
            pass
