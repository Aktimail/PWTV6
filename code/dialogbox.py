import pygame
from tool import Tool


class DialogBox:
    def __init__(self, screen, player, panel="dialog_box", size=None,  pos=None):
        self.screen = screen
        self.player = player
        self.reading = False

        self.panel_width = self.screen.get_size()[0] // 1.2
        self.panel_height = self.screen.get_size()[1] // 5
        self.panel_size = size if size else (self.panel_width, self.panel_height)

        self.panel_pos = pos if pos else (self.screen.rect.midbottom[0] - self.panel_width // 2,
                                          self.screen.rect.midbottom[1] - self.panel_height - 30)

        self.panel = pygame.transform.scale(pygame.image.load(f"../assets/dialogs/{panel}.png"), self.panel_size)

        self.next_txt_icon = pygame.image.load("../assets/dialogs/next_txt_icon.png")
        self.icon_pos = [1200, 700]
        self.icon_animation_counter = 0

        self.font = pygame.font.Font("../assets/dialogs/PKMN RBYGSC.ttf", 24)
        self.txt_pos = (self.panel_pos[0] + 40, self.panel_pos[1] + 20)
        self.txt_color = (0, 0, 0)

        self.texts = []
        self.txt_idx = 0
        self.txt_progression = 0
        self.txt_speed = 1

    def update(self):
        self.screen.display.blit(self.panel, self.panel_pos)
        if self.texts:
            Tool.render_text(self.screen.display, Tool.formatted_text(
                self.texts[self.txt_idx][:int(self.txt_progression)], self.txt_color, self.font), self.txt_pos)

            if self.txt_progression < len(self.texts[self.txt_idx]):
                self.txt_progression += self.txt_speed
            else:
                self.render_next_txt_icon()

    def next_text(self):
        if self.texts:
            if self.txt_progression >= len(self.texts[self.txt_idx]):
                self.txt_idx += 1
                self.txt_progression = 0
                if self.txt_idx >= len(self.texts):
                    self.txt_idx = 0
                    if self.player.opponent:
                        self.player.fighting = True
                    return False
            return True

    def render_next_txt_icon(self):
        self.screen.display.blit(self.next_txt_icon, self.icon_pos)
        self.icon_animation_counter += 1
        if self.icon_animation_counter >= 25:
            self.icon_animation_counter = 0
            if self.icon_pos[1] == 700:
                self.icon_pos[1] = 695
            elif self.icon_pos[1] == 695:
                self.icon_pos[1] = 700
