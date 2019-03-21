# -*- coding: UTF-8 -*-
import unittest
from ..utils.init_util import build_objects_from_files
from queue import Queue
from ..game.Game import Game
import logging
from src.schedulers.EmptyScheduler import EmptyScheduler


logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s] %(levelname)s [%(funcName)s: %(filename)s, %(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filemode='a')
DELAY = 0    # 图形化展示路口运转情况时，sleep时间


def test_helper(car_path, road_path, cross_path, total_tick=3, start_position=10, delay=0):
    g = Game()
    id_2_cars, id_2_roads, id_2_cross = \
        build_objects_from_files(car_path=car_path,
                                 road_path=road_path,
                                 cross_path=cross_path)
    global_tick = 1
    lanes1 = id_2_roads[1]._lanes['positive']
    car_id = 100
    for lane in lanes1:
        lane.enter(id_2_cars[car_id], start_position, global_tick)
        lane.enter(id_2_cars[car_id + 1], start_position, global_tick)
        car_id += 100

    for car_id in id_2_cars:
        id_2_cars[car_id].set_path([(id_2_roads[2], 'positive')])
        id_2_cars[car_id]._current_road = id_2_roads[1]

    scheduler = EmptyScheduler(id_2_cars, id_2_roads, id_2_cross)
    for i in id_2_roads:
        id_2_roads[i].set_scheduler(scheduler)

    predict_state = []
    while global_tick < total_tick:
        g.run(id_2_cross[2], delay=delay)
        roads_state = get_current_roads_state(id_2_roads)
        predict_state.append(roads_state)

        global_tick += 1
        for road_id in id_2_roads:
            id_2_roads[road_id].go_by_tick(global_tick)
        for cross_id in sorted(id_2_cross.keys()):
            id_2_cross[cross_id].go_by_tick(global_tick)
    return predict_state


def get_current_roads_state(id_2_roads):
    roads_state = {}
    for road_id in id_2_roads:
        road = id_2_roads[road_id]
        state = dict()
        state['positive'] = [[] for _ in range(road.get_channel_number())]
        for index, lane in enumerate(road.get_lanes('positive')):
            slot_point = lane.get_head()
            while slot_point:
                state['positive'][index].append((slot_point.car.get_id(), slot_point.position))
                slot_point = slot_point.next
        if road.is_duplex():
            state['negative'] = [[] for _ in range(road.get_channel_number())]
            for index, lane in enumerate(road.get_lanes('negative')):
                slot_point = lane.get_head()
                while slot_point:
                    state['negative'][index].append((slot_point.car.get_id(), slot_point.position))
                    slot_point = slot_point.next
        roads_state[road_id] = state
    return roads_state


class TestPassCross(unittest.TestCase):
    def test_case1(self):
        predict_state = test_helper(car_path='src/tests/test_pass_cross_cases/config1/car.txt',
                                    road_path='src/tests/test_pass_cross_cases/config1/road.txt',
                                    cross_path='src/tests/test_pass_cross_cases/config1/cross.txt',
                                    total_tick=4,
                                    delay=DELAY)
        truely_states = [
            {
                1: {'positive': [[(100, 10), (101, 9)], [(200, 10), (201, 9)], [(300, 10), (301, 9)]]},
                2: {'positive': [[], [], []]}
            },
            {
                1: {'positive': [[], [], []]},
                2: {'positive': [[(100, 5), (200, 4), (300, 3), (101, 2), (201, 1)], [(301, 4)], []]}
            },
            {
                1: {'positive': [[], [], []]},
                2: {'positive': [[(100, 10), (200, 9), (300, 8), (101, 7), (201, 6)], [(301, 9)], []]}
            }
        ]
        self.assertEqual(predict_state, truely_states)

    def test_case2(self):
        predict_state = test_helper(car_path='src/tests/test_pass_cross_cases/config2/car.txt',
                                    road_path='src/tests/test_pass_cross_cases/config2/road.txt',
                                    cross_path='src/tests/test_pass_cross_cases/config2/cross.txt',
                                    total_tick=4,
                                    delay=DELAY)
        truely_states = [
            {
                1: {'positive': [[(100, 10), (101, 9)], [(200, 10), (201, 9)], [(300, 10), (301, 9)]]},
                2: {'positive': [[], [], []]}
            },
            {
                1: {'positive': [[], [], []]},
                2: {'positive': [[(100, 5), (200, 3), (300, 2), (101, 1)], [(201, 4), (301, 3)], []]}
            },
            {
                1: {'positive': [[], [], []]},
                2: {'positive': [[(100, 10), (200, 6), (300, 5), (101, 4)], [(201, 9), (301, 8)], []]}
            }
        ]
        self.assertEqual(predict_state, truely_states)

    def test_case3(self):
        predict_state = test_helper(car_path='src/tests/test_pass_cross_cases/config3/car.txt',
                                    road_path='src/tests/test_pass_cross_cases/config3/road.txt',
                                    cross_path='src/tests/test_pass_cross_cases/config3/cross.txt',
                                    total_tick=4,
                                    delay=DELAY)
        truely_states = [
            {
                1: {'positive': [[(100, 10), (101, 9)], [(200, 10), (201, 9)], [(300, 10), (301, 9)]]},
                2: {'positive': [[], [], []]}
            },
            {
                1: {'positive': [[(101, 10)], [], []]},
                2: {'positive': [[(100, 5), (200, 1)], [(300, 1)], [(201, 4), (301, 3)]]}
            },
            {
                1: {'positive': [[], [], []]},
                2: {'positive': [[(100, 10), (200, 2), (101, 1)], [(300, 2)], [(201, 9), (301, 8)]]}
            }
        ]
        self.assertEqual(predict_state, truely_states)

    def test_case4(self):
        predict_state = test_helper(car_path='src/tests/test_pass_cross_cases/config4/car.txt',
                                    road_path='src/tests/test_pass_cross_cases/config4/road.txt',
                                    cross_path='src/tests/test_pass_cross_cases/config4/cross.txt',
                                    total_tick=5,
                                    start_position=8,
                                    delay=DELAY)
        truely_states = [
            {
                1: {'positive': [[(100, 8), (101, 7)], [(200, 8), (201, 7)], [(300, 8), (301, 7)]]},
                2: {'positive': [[], [], []]}
            },
            {
                1: {'positive': [[(100, 10), (101, 9)], [(200, 10), (201, 9)], [(300, 10), (301, 9)]]},
                2: {'positive': [[], [], []]}
            },
            {
                1: {'positive': [[(101, 10)], [(201, 10)], [(301, 10)]]},
                2: {'positive': [[(100, 1)], [(200, 1)], [(300, 1)]]}
            },
            {
                1: {'positive': [[], [], []]},
                2: {'positive': [[(100, 2), (101, 1)], [(200, 2), (201, 1)], [(300, 2), (301, 1)]]}
            }
        ]
        self.assertEqual(predict_state, truely_states)

    def test_case5(self):
        predict_state = test_helper(car_path='src/tests/test_pass_cross_cases/config5/car.txt',
                                    road_path='src/tests/test_pass_cross_cases/config5/road.txt',
                                    cross_path='src/tests/test_pass_cross_cases/config5/cross.txt',
                                    total_tick=4,
                                    start_position=8,
                                    delay=DELAY)
        truely_states = [
            {
                1: {'positive': [[(100, 8), (101, 7)], [(200, 8), (201, 7)], [(300, 8), (301, 7)]]},
                2: {'positive': [[], [], []]}
            },
            {
                1: {'positive': [[], [], []]},
                2: {'positive': [[(100, 3), (200, 2), (300, 1)], [(101, 2), (201, 1)], [(301, 2)]]}
            },
            {
                1: {'positive': [[], [], []]},
                2: {'positive': [[(100, 8), (200, 7), (300, 6)], [(101, 7), (201, 6)], [(301, 7)]]}
            }
        ]
        self.assertEqual(predict_state, truely_states)

    def test_case6(self):
        g = Game()
        id_2_cars, id_2_roads, id_2_cross = \
            build_objects_from_files(car_path='src/tests/test_pass_cross_cases/config6/car.txt',
                                     road_path='src/tests/test_pass_cross_cases/config6/road.txt',
                                     cross_path='src/tests/test_pass_cross_cases/config6/cross.txt')
        global_tick = 1
        car_id = 100
        for lane in id_2_roads[4]._lanes['positive']:
            lane.enter(id_2_cars[car_id], 10, global_tick)
            id_2_cars[car_id]._current_road = id_2_roads[4]
            lane.enter(id_2_cars[car_id + 1], 10, global_tick)
            id_2_cars[car_id + 1]._current_road = id_2_roads[4]
            car_id += 100
        for lane in id_2_roads[3]._lanes['positive']:
            lane.enter(id_2_cars[car_id], 10, global_tick)
            id_2_cars[car_id]._current_road = id_2_roads[3]
            lane.enter(id_2_cars[car_id + 1], 10, global_tick)
            id_2_cars[car_id + 1]._current_road = id_2_roads[3]
            car_id += 100

        for lane in id_2_roads[1]._lanes['positive']:
            lane.enter(id_2_cars[car_id], 10, global_tick)
            id_2_cars[car_id]._current_road = id_2_roads[1]
            lane.enter(id_2_cars[car_id + 1], 10, global_tick)
            id_2_cars[car_id + 1]._current_road = id_2_roads[1]
            car_id += 100

        for car_id in id_2_cars:
            id_2_cars[car_id].set_path([(id_2_roads[2], 'positive')])

        scheduler = EmptyScheduler(id_2_cars, id_2_roads, id_2_cross)
        for i in id_2_roads:
            id_2_roads[i].set_scheduler(scheduler)
        predict_state = []

        while global_tick < 4:
            g.run(id_2_cross[5], delay=0)
            roads_state = get_current_roads_state(id_2_roads)
            predict_state.append(roads_state)
            global_tick += 1
            for road_id in id_2_roads:
                id_2_roads[road_id].go_by_tick(global_tick)
            for cross_id in sorted(id_2_cross.keys()):
                id_2_cross[cross_id].go_by_tick(global_tick)

        truely_states = [
            {
                1: {'positive': [[(700, 10), (701, 9)], [(800, 10), (801, 9)], [(900, 10), (901, 9)]]},
                2: {'positive': [[], [], []]},
                3: {'positive': [[(400, 10), (401, 9)], [(500, 10), (501, 9)], [(600, 10), (601, 9)]]},
                4: {'positive': [[(100, 10), (101, 9)], [(200, 10), (201, 9)], [(300, 10), (301, 9)]]}
            },
            {
                1: {'positive': [[], [], []]},
                2: {'positive': [[(100, 5), (200, 4), (300, 3), (101, 2), (201, 1)],
                                 [(301, 4), (700, 3), (800, 2), (900, 1)],
                                 [(701, 4), (801, 3), (901, 2), (400, 1)]
                                 ]
                    },
                3: {'positive': [[(401, 9)], [(500, 10), (501, 9)], [(600, 10), (601, 9)]]},
                4: {'positive': [[], [], []]}
            },
            {
                1: {'positive': [[], [], []]},
                2: {'positive': [
                    [(100, 10), (200, 9), (300, 8), (101, 7), (201, 6), (600, 5), (401, 4), (500, 3), (601, 2), (501, 1)],
                    [(301, 9), (700, 8), (800, 7), (900, 6)],
                    [(701, 9), (801, 8), (901, 7), (400, 6)]
                ]},
                3: {'positive': [[], [], []]},
                4: {'positive': [[], [], []]}
            }
        ]
        self.assertEqual(predict_state, truely_states)
