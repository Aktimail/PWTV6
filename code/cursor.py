import pygame


class Cursor:
    def __init__(self):
        self.position = pygame.Vector2(0, 0)
        self.button = [False, False, False]