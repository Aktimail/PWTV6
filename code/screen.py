import pygame


class Screen:
    def __init__(self):
        self.display = pygame.display.set_mode((1280, 720))

        self.clock = pygame.time.Clock()
        self.framerate = 60

        self.rect = self.display.get_rect()

    def update(self):
        pygame.display.flip()
        self.display.fill((0, 0, 0))
        self.clock.tick(self.framerate)

    def get_size(self):
        return self.display.get_size()

    def get_display(self):
        return self.display
