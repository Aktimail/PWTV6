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
        self.y_osc_idx_counter = 0

        self.active_menu = None

        self.interactive_rect = {}

        self.player_assets = {}
        self.opp_assets = {}

        self.main_menu_hud = {
            "battle": {
                "image": pygame.image.load("../assets/battle/battlebar.png"),
                "size": (self.screen.get_width() / 16, self.screen.get_height() / 9),
                "pos": (self.screen.get_width() / 1.06666667, self.screen.get_height() / 3)
            },
            "team": {
                "image": pygame.image.load("../assets/battle/battlebar.png"),
                "size": (self.screen.get_width() / 16, self.screen.get_height() / 9),
                "pos": (self.screen.get_width() / 1.06666667, self.screen.get_height() / 2.25)
            },
            "bag": {
                "image": pygame.image.load("../assets/battle/battlebar.png"),
                "size": (self.screen.get_width() / 16, self.screen.get_height() / 9),
                "pos": (self.screen.get_width() / 1.06666667, self.screen.get_height() / 1.5)
            },
            "run": {
                "image": pygame.image.load("../assets/battle/battlebar.png"),
                "size": (self.screen.get_width() / 16, self.screen.get_height() / 9),
                "pos": (self.screen.get_width() / 1.06666667, self.screen.get_height() / 1.8)
            }
        }
        move_asset_size = (self.screen.get_width() / 6.73684211, self.screen.get_height() / 9)
        self.battle_menu_hud = {
            "move1": {
                "image": pygame.image.load("../assets/battle/battlebar.png"),
                "size": move_asset_size,
                "pos": (self.screen.get_width() / 1.27363184, self.screen.get_height() / 3)
            },
            "move2": {
                "image": pygame.image.load("../assets/battle/battlebar.png"),
                "size": move_asset_size,
                "pos": (self.screen.get_width() / 1.27363184, self.screen.get_height() / 2.25)
            },
            "move3": {
                "image": pygame.image.load("../assets/battle/battlebar.png"),
                "size": move_asset_size,
                "pos": (self.screen.get_width() / 1.27363184, self.screen.get_height() / 1.8)
            },
            "move4": {
                "image": pygame.image.load("../assets/battle/battlebar.png"),
                "size": move_asset_size,
                "pos": (self.screen.get_width() / 1.27363184, self.screen.get_height() / 1.5)
            }
        }

        pkmn_asset_size = (self.screen.get_width() / 10.6666667, self.screen.get_height() / 9)
        x = (self.screen.get_width() / 1.19069767) if len(self.player.team) <= 3 else \
            (self.screen.get_height() / 1.34736842)
        self.team_menu_hud = {
            "pkmn1": {
                "image": pygame.image.load("../assets/battle/battlebar.png"),
                "size": pkmn_asset_size,
                "pos": (x, self.screen.get_height() / 2.25)
            },
            "pkmn2": {
                "image": pygame.image.load("../assets/battle/battlebar.png"),
                "size": pkmn_asset_size,
                "pos": (x, self.screen.get_height() / 1.8)
            },
            "pkmn3": {
                "image": pygame.image.load("../assets/battle/battlebar.png"),
                "size": pkmn_asset_size,
                "pos": (x, self.screen.get_height() / 1.5)
            },
            "pkmn4": {
                "image": pygame.image.load("../assets/battle/battlebar.png"),
                "size": pkmn_asset_size,
                "pos": (x + self.screen.get_width() / 10.24, self.screen.get_height() / 2.25)
            },
            "pkmn5": {
                "image": pygame.image.load("../assets/battle/battlebar.png"),
                "size": pkmn_asset_size,
                "pos": (x + self.screen.get_width() / 10.24, self.screen.get_height() / 1.8)
            },
            "pkmn6": {
                "image": pygame.image.load("../assets/battle/battlebar.png"),
                "size": pkmn_asset_size,
                "pos": (x + self.screen.get_width() / 10.24, self.screen.get_height() / 1.5)
            }
        }

        self.dialog_box = DialogBox(self.screen, self.player, "battle_box",
                                    (self.screen.get_width(), self.screen.get_height() / 4.8),
                                    (0, self.screen.get_height() / 1.26315789))

    def init_player_hud(self):
        self.player_assets = {
            "ground": {
                "image": pygame.image.load("../assets/battle/player/ground.png"),
                "size": (self.screen.get_width() / 1.25, self.screen.get_height() / 5.625),
                "pos": (self.screen.get_width() / -25.6, self.screen.get_height() / 1.62895928)
            },
            "pokemon": {
                "image": pygame.image.load(self.player.lead.back_spritesheet),
                "size": (self.screen.get_width() / 1.9047619, self.screen.get_height() / 1.07142857),
                "pos": [self.screen.get_width() / 12.8, self.screen.get_height() /
                        (720 / (self.player.lead.front_offset_y * 7 - self.y_oscillation[self.y_oscillation_idx]))]
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
                "size": (self.screen.get_width() / 4.5, self.screen.get_height() / 9),
                "pos": (0, self.screen.get_height() / 1.5)
            },
            "hp_bar": {
                "image": None,
                "size": (0, 0),
                "pos": (0, 0)
            },
            "hp": {
                "image": self.init_hp_color(self.player.lead),
                "size": (int(self.player.lead.hp / self.player.lead.max_hp * (self.screen.get_width() / 4.5)),
                         self.screen.get_height() / 60),
                "pos": (0, 0)
            },
            "pokeballs": {
                "image": None,
                "size": (0, 0),
                "pos": (0, 0)
            }
        }

    def init_opp_hud(self):
        self.opp_assets = {
            "ground": {
                "image": pygame.image.load("../assets/battle/opponent/ground.png"),
                "size": (self.screen.get_width() / 2.84444444, self.screen.get_height() / 3.6),
                "pos": (self.screen.get_width() / 1.82857143, self.screen.get_height() / 3.2)
            },
            "pokemon": {
                "image": pygame.image.load(self.opponent.lead.spritesheet),
                "size": (self.screen.get_width() / 4.44444444, self.screen.get_height() / 2.5),
                "pos": [self.screen.get_width() / 1.6516129,
                        self.screen.get_height() / (720 / (self.opponent.lead.front_offset_y * 3 + 50))]
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
                "size": (self.screen.get_width() / 4.65454545, self.screen.get_height() / 12),
                "pos": (self.screen.get_width() / 1.27363184, self.screen.get_height() / 144)
            },
            "hp_bar": {
                "image": None,
                "size": (0, 0),
                "pos": (0, 0)
            },
            "hp": {
                "image": self.init_hp_color(self.opponent.lead),
                "size": (int(self.opponent.lead.hp / self.opponent.lead.max_hp * (self.screen.get_width() / 4.5)),
                         self.screen.get_height() / 60),
                "pos": (0, self.screen.get_height() / 24)
            },
            "pokeballs": {
                "image": None,
                "size": (0, 0),
                "pos": (0, 0)
            }
        }

    def blit_main_menu(self):
        for asset in self.main_menu_hud:
            image = self.main_menu_hud[asset]["image"]
            image = pygame.transform.scale(image, self.main_menu_hud[asset]["size"])
            self.display.blit(image, self.main_menu_hud[asset]["pos"])
            self.interactive_rect[asset] = pygame.Rect(self.main_menu_hud[asset]["pos"][0],
                                                       self.main_menu_hud[asset]["pos"][1],
                                                       self.main_menu_hud[asset]["size"][0],
                                                       self.main_menu_hud[asset]["size"][1])

    def blit_battle_menu(self):
        x = 0
        for asset in self.battle_menu_hud:
            x += 1
            if x <= len(self.player.lead.moveset):
                image = self.battle_menu_hud[asset]["image"]
                image = pygame.transform.scale(image, self.battle_menu_hud[asset]["size"])
                self.display.blit(image, self.battle_menu_hud[asset]["pos"])
                self.interactive_rect[asset] = pygame.Rect(self.battle_menu_hud[asset]["pos"][0],
                                                           self.battle_menu_hud[asset]["pos"][1],
                                                           self.battle_menu_hud[asset]["size"][0],
                                                           self.battle_menu_hud[asset]["size"][1])

    def blit_team_menu(self):
        x = 0
        for asset in self.team_menu_hud:
            if x < len(self.player.team):
                x += 1
                image = self.team_menu_hud[asset]["image"]
                image = pygame.transform.scale(image, self.team_menu_hud[asset]["size"])
                self.display.blit(image, self.team_menu_hud[asset]["pos"])
                self.interactive_rect[asset] = pygame.Rect(self.team_menu_hud[asset]["pos"][0],
                                                           self.team_menu_hud[asset]["pos"][1],
                                                           self.team_menu_hud[asset]["size"][0],
                                                           self.team_menu_hud[asset]["size"][1])

    def blit_player_hud(self):
        self.init_player_hud()
        for asset in self.player_assets:
            if self.player_assets[asset]["image"]:
                image = self.player_assets[asset]["image"]
                image = pygame.transform.scale(image, self.player_assets[asset]["size"])
                self.display.blit(image, self.player_assets[asset]["pos"])

    def blit_opp_hud(self):
        self.init_opp_hud()
        for asset in self.opp_assets:
            if self.opp_assets[asset]["image"]:
                image = self.opp_assets[asset]["image"]
                image = pygame.transform.scale(image, self.opp_assets[asset]["size"])
                self.display.blit(image, self.opp_assets[asset]["pos"])

    def blit_hud(self):
        self.interactive_rect.clear()
        self.display.blit(self.background, (0, 0))
        self.blit_opp_hud()
        self.blit_player_hud()
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
        self.player.lead.update_hp()
        self.opponent.lead.update_hp()

        self.blit_hud()
        self.blit_pkmn_info(self.player.lead)
        self.check_interactions()
        self.init_active_menu()

        self.dialog_box.update()

        self.update_oscillation()
        if self.player.lost() or self.opponent.lost():
            self.player.fighting = False
            self.player.opponent = None

    def update_oscillation(self):
        self.y_osc_idx_counter += 1
        if self.y_osc_idx_counter > 15:
            self.y_osc_idx_counter = 0
            self.y_oscillation_idx += 1
            if self.y_oscillation_idx >= len(self.y_oscillation):
                self.y_oscillation_idx = 0

    def init_active_menu(self):
        if self.interactive_rect["battle"].collidepoint(self.cursor.position) and self.cursor.button[0]:
            self.active_menu = "battle"
        elif self.interactive_rect["team"].collidepoint(self.cursor.position) and self.cursor.button[0]:
            if len(self.player.team) > 1:
                self.active_menu = "team"
        elif self.interactive_rect["bag"].collidepoint(self.cursor.position) and self.cursor.button[0]:
            self.active_menu = "bag"
        elif self.interactive_rect["run"].collidepoint(self.cursor.position) and self.cursor.button[0]:
            self.active_menu = "run"
        elif self.cursor.button[0]:
            self.active_menu = None

    def check_interactions(self):
        if self.active_menu == "battle":
            self.blit_battle_menu()
            for i in range(len(self.player.lead.moveset)):
                if (self.interactive_rect["move" + str(i+1)].collidepoint(self.cursor.position)
                        and self.cursor.button[0]):
                    self.player.lead.attack(self.player.lead.moveset[i], self.opponent.lead)

        if self.active_menu == "team":
            self.blit_team_menu()
            for i in range(len(self.player.team)):
                if (self.interactive_rect["pkmn" + str(i+1)].collidepoint(self.cursor.position)
                        and self.cursor.button[0]):
                    self.player.switch(i)

    @staticmethod
    def print_stat_change(boost):
        txt = ""
        for i in range(abs(boost)):
            if boost > 0:
                txt += "▲"
            if boost < 0:
                txt += "▼"
        for i in range(6 - abs(boost)):
            txt += "•"
        return txt

    def blit_pkmn_info(self, pkmn):
        font = pygame.font.Font("../assets/dialogs/SegoeUI-VF/SegoeUI-VF.ttf", 18)

        infos = pkmn.name + "\n"
        type2 = " | " + pkmn.type[1].name if len(pkmn.type) > 1 else ""
        infos += "Type : " + pkmn.type[0].name + type2 + "\n"
        infos += "\n"
        infos += "Ability : " + pkmn.ability.name + "\n"
        item = pkmn.item.name if pkmn.item else ""
        infos += "Item : " + item + "\n"
        infos += "\n"
        stats_name = ["atk", "deff", "aspe", "dspe", "spd"]
        stats = [pkmn.atk, pkmn.deff, pkmn.aspe, pkmn.dspe, pkmn.spd]
        for sn, s in zip(stats_name, stats):
            infos += sn + " : " + str(s) + " " + self.print_stat_change(pkmn.boosts[sn]) + "\n"

        infos = Tool.formatted_text(infos, (0, 0, 0), font)
        Tool.render_text(self.display, infos, (0, 0), 22)
