import pygame
import sys
from pygame.locals import *
import time

BACKGROUND_SIZE = (842, 842)
SLOT_SIZE = (38, 13)
DIGIT_SIZE = (9, 13)

START_POSITIONS = {
    'up': {'positive': (406, 0), 'negative': (423, 371)},
    'down': {'positive': (423, 833), 'negative': (406, 462)},
    'left': {'positive': (0, 423), 'negative': (342, 406)},
    'right': {'positive': (804, 406), 'negative': (462, 423)}
}
POSITIONS_DELTA = {
    'up': {'positive': (-13, 38), 'negative': (13, -38)},
    'down': {'positive': (13, -38), 'negative': (-13, 38)},
    'left': {'positive': (38, 13), 'negative': (-38, -13)},
    'right': {'positive': (-38, -13), 'negative': (38, 13)}
}
DIGIT_DELTA = {
    'up': {'positive': (0, 9), 'negative': (0, -9)},
    'down': {'positive': (0, -9), 'negative': (0, 9)},
    'left': {'positive': (9, 0), 'negative': (-9, 0)},
    'right': {'positive': (-9, 0), 'negative': (9, 0)}
}


class Game(object):
    def __init__(self):
        pygame.init()
        self._clock = pygame.time.Clock()
        self._screen = pygame.display.set_mode(BACKGROUND_SIZE)
        pygame.display.set_caption('Traffic')

        self._images = {
            'background': pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/cross.png').convert(),
            'digits': {
                'up': {'positive': [
                    pygame.transform.rotate(
                        pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/0.png').convert(),
                        270),
                    pygame.transform.rotate(
                        pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/1.png').convert(),
                        270),
                    pygame.transform.rotate(
                        pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/2.png').convert(),
                        270),
                    pygame.transform.rotate(
                        pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/3.png').convert(),
                        270),
                    pygame.transform.rotate(
                        pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/4.png').convert(),
                        270),
                    pygame.transform.rotate(
                        pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/5.png').convert(),
                        270),
                    pygame.transform.rotate(
                        pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/6.png').convert(),
                        270),
                    pygame.transform.rotate(
                        pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/7.png').convert(),
                        270),
                    pygame.transform.rotate(
                        pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/8.png').convert(),
                        270),
                    pygame.transform.rotate(
                        pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/9.png').convert(),
                        270),
                ], 'negative': [
                    pygame.transform.rotate(
                        pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/0.png').convert(),
                        90),
                    pygame.transform.rotate(
                        pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/1.png').convert(),
                        90),
                    pygame.transform.rotate(
                        pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/2.png').convert(),
                        90),
                    pygame.transform.rotate(
                        pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/3.png').convert(),
                        90),
                    pygame.transform.rotate(
                        pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/4.png').convert(),
                        90),
                    pygame.transform.rotate(
                        pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/5.png').convert(),
                        90),
                    pygame.transform.rotate(
                        pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/6.png').convert(),
                        90),
                    pygame.transform.rotate(
                        pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/7.png').convert(),
                        90),
                    pygame.transform.rotate(
                        pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/8.png').convert(),
                        90),
                    pygame.transform.rotate(
                        pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/9.png').convert(),
                        90),
                ]},
                'down': {'positive': [
                    pygame.transform.rotate(
                        pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/0.png').convert(),
                        90),
                    pygame.transform.rotate(
                        pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/1.png').convert(),
                        90),
                    pygame.transform.rotate(
                        pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/2.png').convert(),
                        90),
                    pygame.transform.rotate(
                        pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/3.png').convert(),
                        90),
                    pygame.transform.rotate(
                        pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/4.png').convert(),
                        90),
                    pygame.transform.rotate(
                        pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/5.png').convert(),
                        90),
                    pygame.transform.rotate(
                        pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/6.png').convert(),
                        90),
                    pygame.transform.rotate(
                        pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/7.png').convert(),
                        90),
                    pygame.transform.rotate(
                        pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/8.png').convert(),
                        90),
                    pygame.transform.rotate(
                        pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/9.png').convert(),
                        90),
                ], 'negative': [
                    pygame.transform.rotate(
                        pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/0.png').convert(),
                        270),
                    pygame.transform.rotate(
                        pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/1.png').convert(),
                        270),
                    pygame.transform.rotate(
                        pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/2.png').convert(),
                        270),
                    pygame.transform.rotate(
                        pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/3.png').convert(),
                        270),
                    pygame.transform.rotate(
                        pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/4.png').convert(),
                        270),
                    pygame.transform.rotate(
                        pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/5.png').convert(),
                        270),
                    pygame.transform.rotate(
                        pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/6.png').convert(),
                        270),
                    pygame.transform.rotate(
                        pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/7.png').convert(),
                        270),
                    pygame.transform.rotate(
                        pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/8.png').convert(),
                        270),
                    pygame.transform.rotate(
                        pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/9.png').convert(),
                        270),
                ]},
                'left': {'positive': [
                    pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/0.png').convert(),
                    pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/1.png').convert(),
                    pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/2.png').convert(),
                    pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/3.png').convert(),
                    pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/4.png').convert(),
                    pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/5.png').convert(),
                    pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/6.png').convert(),
                    pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/7.png').convert(),
                    pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/8.png').convert(),
                    pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/9.png').convert(),
                ], 'negative': [
                    pygame.transform.rotate(
                        pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/0.png').convert(),
                        180),
                    pygame.transform.rotate(
                        pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/1.png').convert(),
                        180),
                    pygame.transform.rotate(
                        pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/2.png').convert(),
                        180),
                    pygame.transform.rotate(
                        pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/3.png').convert(),
                        180),
                    pygame.transform.rotate(
                        pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/4.png').convert(),
                        180),
                    pygame.transform.rotate(
                        pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/5.png').convert(),
                        180),
                    pygame.transform.rotate(
                        pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/6.png').convert(),
                        180),
                    pygame.transform.rotate(
                        pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/7.png').convert(),
                        180),
                    pygame.transform.rotate(
                        pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/8.png').convert(),
                        180),
                    pygame.transform.rotate(
                        pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/9.png').convert(),
                        180),
                ]},
                'right': {'positive': [
                    pygame.transform.rotate(
                        pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/0.png').convert(),
                        180),
                    pygame.transform.rotate(
                        pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/1.png').convert(),
                        180),
                    pygame.transform.rotate(
                        pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/2.png').convert(),
                        180),
                    pygame.transform.rotate(
                        pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/3.png').convert(),
                        180),
                    pygame.transform.rotate(
                        pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/4.png').convert(),
                        180),
                    pygame.transform.rotate(
                        pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/5.png').convert(),
                        180),
                    pygame.transform.rotate(
                        pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/6.png').convert(),
                        180),
                    pygame.transform.rotate(
                        pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/7.png').convert(),
                        180),
                    pygame.transform.rotate(
                        pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/8.png').convert(),
                        180),
                    pygame.transform.rotate(
                        pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/9.png').convert(),
                        180),
                ], 'negative': [
                    pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/0.png').convert(),
                    pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/1.png').convert(),
                    pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/2.png').convert(),
                    pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/3.png').convert(),
                    pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/4.png').convert(),
                    pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/5.png').convert(),
                    pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/6.png').convert(),
                    pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/7.png').convert(),
                    pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/8.png').convert(),
                    pygame.image.load('/home/judy/SDK/SDK_python/CodeCraft-2019/src/game/images/9.png').convert(),
                ]}
            }
        }

    def run(self, cross):
        self.cross = cross
        self._screen.blit(self._images['background'], (0, 0))
        up_road, right_road, down_road, left_road = cross.get_road_list()
        self.draw_cars_on_road(up_road, 'up')
        self.draw_cars_on_road(down_road, 'down')
        self.draw_cars_on_road(left_road, 'left')
        self.draw_cars_on_road(right_road, 'right')
        pygame.display.update()
        time.sleep(1)

    def draw_cars_on_road(self, road, direction):
        if road is None:
            return
        start_positions = START_POSITIONS[direction]
        positive_negative_digits = self._images['digits'][direction]
        position_delta = POSITIONS_DELTA[direction]
        digit_delta = DIGIT_DELTA[direction]

        draw_direction = 'negative' if road.get_source() == self.cross else 'positive'
        self.draw_cars_one_side(road.get_positive_lanes(), start_positions[draw_direction],
                                positive_negative_digits[draw_direction], position_delta[draw_direction], digit_delta[draw_direction], direction)
        if road.is_duplex():
            draw_direction = 'positive' if road.get_destination() == self.cross else 'negative'
            self.draw_cars_one_side(road.get_negative_lanes(), start_positions[draw_direction],
                                    positive_negative_digits[draw_direction], position_delta[draw_direction], digit_delta[draw_direction], direction)

    def draw_cars_one_side(self, lanes, start_position, digits, position_delta, digit_delta, direction):
        start_x, start_y = start_position
        delta_x, delta_y = position_delta
        digit_delta_x, digit_delta_y = digit_delta
        for i, lane in enumerate(lanes):
            p = lane.get_head()
            while p:
                if direction in ('left', 'right'):
                    x = start_x + (p.position - 1) * delta_x
                    y = start_y + i * delta_y
                else:
                    x = start_x + i * delta_x
                    y = start_y + (p.position - 1) * delta_y
                car_id = [int(x) for x in list(str(p.car.get_id()))]
                for j, d in enumerate(car_id):
                    self._screen.blit(digits[d], (x + digit_delta_x * j, y + digit_delta_y * j))
                p = p.next

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
    # 生成cross地图
    # g.generate_cross()
    g.run()
