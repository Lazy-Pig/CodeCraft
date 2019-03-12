import pygame
import sys
from pygame.locals import *

BACKGROUND_SIZE = (764, 764)
SLOT_SIZE = (38, 13)


class Game(object):
    def __init__(self):
        pygame.init()
        self._clock = pygame.time.Clock()
        self._screen = pygame.display.set_mode((764, 764))
        pygame.display.set_caption('Traffic')

        # self._images = {
        #     'background': pygame.image.load('images/big_background.png').convert(),
        #     'slot': pygame.image.load('images/slot.png').convert(),
        #     'v_slot': pygame.transform.rotate(pygame.image.load('images/slot.png').convert(), 90),
        # }

        self.generate_cross()

    def generate_cross(self):
        """
        生成固定的路口地图
        """
        big_background_image = pygame.image.load('images/big_background.png').convert()
        slot_image = pygame.image.load('images/slot.png').convert()
        v_slot_image = pygame.transform.rotate(pygame.image.load('images/slot.png').convert(), 90)
        self._screen.blit(big_background_image, (0, 0))
        center_x = BACKGROUND_SIZE[0] // 2
        center_y = BACKGROUND_SIZE[1] // 2
        up_x = center_x - SLOT_SIZE[1]
        up_y = center_y - 3 * SLOT_SIZE[1] - SLOT_SIZE[0] - 2
        down_x = center_x - SLOT_SIZE[1]
        down_y = center_y + 3 * SLOT_SIZE[1] + 2
        left_x = center_x - 3 * SLOT_SIZE[1] - SLOT_SIZE[0] - 2
        left_y = center_y - SLOT_SIZE[1]
        right_x = center_x + 3 * SLOT_SIZE[1] + 2
        right_y = center_y - SLOT_SIZE[1]

        for i in range(10):
            for j in range(3):
                self._screen.blit(v_slot_image, (up_x - j * SLOT_SIZE[1] - 2, up_y))
                self._screen.blit(v_slot_image, (up_x + (j + 1) * SLOT_SIZE[1] + 2, up_y))

                self._screen.blit(v_slot_image, (down_x - j * SLOT_SIZE[1] - 2, down_y))
                self._screen.blit(v_slot_image, (down_x + (j + 1) * SLOT_SIZE[1] + 2, down_y))

                self._screen.blit(slot_image, (left_x, left_y - j * SLOT_SIZE[1] - 2))
                self._screen.blit(slot_image, (left_x, left_y + (j + 1) * SLOT_SIZE[1] + 2))

                self._screen.blit(slot_image, (right_x, right_y - j * SLOT_SIZE[1] - 2))
                self._screen.blit(slot_image, (right_x, right_y + (j + 1) * SLOT_SIZE[1] + 2))
            up_y -= SLOT_SIZE[0]
            down_y += SLOT_SIZE[0]
            left_x -= SLOT_SIZE[0]
            right_x += SLOT_SIZE[0]

        while True:
            pygame.display.update()
            pygame.image.save(self._screen, "images/cross.png")


if __name__ == "__main__":
    g = Game()
