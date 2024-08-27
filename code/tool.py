import pygame


class Tool:

    @staticmethod
    def split_spritesheet(spritesheet):
        all_images = {"down": [],
                      "left": [],
                      "right": [],
                      "up": []
                      }
        width = spritesheet.get_width() // 4
        height = spritesheet.get_height() // 4
        for j, k in enumerate(all_images.keys()):
            for i in range(4):
                all_images[k].append(spritesheet.subsurface(pygame.Rect(i * width, j * height, 24, 32)))
        return all_images

    @staticmethod
    def split_hp_bars(image):
        all_images = []
        width = image.get_width()
        height = image.get_height() // 6
        for i in range(6):
            all_images.append(image.subsurface(pygame.Rect(0, i * height, width, height)))
        return all_images

    @staticmethod
    def blit_animation(screen, anim_sprite, position):
        screen.display.blit(anim_sprite[0], position)

    @staticmethod
    def formatted_text(text, color, font):
        texts = text.split("\n")
        surfaces = []
        for text in texts:
            surfaces.append(font.render(text, True, color))
        return surfaces

    @staticmethod
    def render_text(surface, texts, position, gap):
        for index, text in enumerate(texts):
            surface.blit(text, (position[0], position[1] + index * gap))
