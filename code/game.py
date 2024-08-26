import pygame

from inputsholder import InputsHolder
from screen import Screen
from map import Map
from player import Player
from dialogbox import DialogBox
from battle import Battle
from cursor import Cursor


class Game:
    def __init__(self):
        self.running = True
        self.menu = False

        self.screen = Screen()

        self.cursor = Cursor()
        self.inputs_holder = InputsHolder()
        self.controller = {
            "up": pygame.K_z,
            "down": pygame.K_s,
            "left": pygame.K_q,
            "right": pygame.K_d,
            "run": pygame.K_LSHIFT,
            "bike": pygame.K_b,
            "interact": pygame.K_SPACE,
            "menu": pygame.K_ESCAPE
        }

        self.map = Map(self.screen)
        self.player = Player("player", "hero_01", 800, 800, self.map, self.inputs_holder,
                             self.controller)

        self.dialog_box = DialogBox(self.screen, self.player)

        self.battle = Battle(self.screen, self.cursor, self.player)

        self.map.switch_map(self.map.map_name)
        self.map.add_player(self.player)

    def save_data(self):
        # self.map.save()
        self.player.save_player()

    def input_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.save_data()
                self.running = False

            elif event.type == pygame.KEYDOWN:
                self.inputs_holder.add_key(event.key)
            elif event.type == pygame.KEYUP:
                self.inputs_holder.remove_key(event.key)
            elif event.type == pygame.MOUSEMOTION:
                self.cursor.position = event.pos
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.cursor.button[0] = True
                elif event.button == 3:
                    self.cursor.button[2] = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.cursor.button[0] = False
                elif event.button == 3:
                    self.cursor.button[2] = False

    def dialogs_handler(self):
        self.dialog_box.texts = self.map.current_dialogs
        self.dialog_box.update()
        if self.player.inputs_holder.key_pressed(self.player.controller["interact"]):
            self.player.inputs_holder.remove_key(self.player.controller["interact"])
            if not self.dialog_box.next_text():
                self.map.rest = False
                self.player.interaction = False

    def battle_handler(self):
        self.battle.update()

    def run(self):
        while self.running:
            self.screen.update()
            if self.player.fighting:
                self.battle.opponent = self.player.opponent
                self.battle_handler()
            else:
                self.map.update()
                if self.map.rest:
                    self.dialogs_handler()

            self.input_handler()
