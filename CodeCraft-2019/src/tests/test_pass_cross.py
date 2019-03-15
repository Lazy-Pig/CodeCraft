import unittest
from ..utils.init_util import build_objects_from_files
from queue import Queue
from ..game.Game import Game
import logging


logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s] %(levelname)s [%(funcName)s: %(filename)s, %(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filemode='a')


def test_helper(car_path, road_path, cross_path, total_tick=6, start_position=10):
    g = Game()
    id_2_cars, id_2_roads, id_2_cross, global_exit_queue = \
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

    while global_tick < total_tick:
        g.run(id_2_cross[2])
        for road_id in id_2_roads:
            id_2_roads[road_id].go_by_tick(global_tick)
        for road_id in id_2_roads:
            id_2_roads[road_id].enter_all(global_tick)
        global_exit_queue.clear()
        global_tick += 1


class TestPassCross(unittest.TestCase):
    def test_case1(self):
        test_helper(car_path='src/tests/test_pass_cross_cases/config1/car.txt',
                    road_path='src/tests/test_pass_cross_cases/config1/road.txt',
                    cross_path='src/tests/test_pass_cross_cases/config1/cross.txt',
                    total_tick=5)

    def test_case2(self):
        test_helper(car_path='src/tests/test_pass_cross_cases/config2/car.txt',
                    road_path='src/tests/test_pass_cross_cases/config2/road.txt',
                    cross_path='src/tests/test_pass_cross_cases/config2/cross.txt',
                    total_tick=6)

    def test_case3(self):
        test_helper(car_path='src/tests/test_pass_cross_cases/config3/car.txt',
                    road_path='src/tests/test_pass_cross_cases/config3/road.txt',
                    cross_path='src/tests/test_pass_cross_cases/config3/cross.txt',
                    total_tick=6)

    def test_case4(self):
        test_helper(car_path='src/tests/test_pass_cross_cases/config4/car.txt',
                    road_path='src/tests/test_pass_cross_cases/config4/road.txt',
                    cross_path='src/tests/test_pass_cross_cases/config4/cross.txt',
                    total_tick=6,
                    start_position=8)

    def test_case5(self):
        test_helper(car_path='src/tests/test_pass_cross_cases/config5/car.txt',
                    road_path='src/tests/test_pass_cross_cases/config5/road.txt',
                    cross_path='src/tests/test_pass_cross_cases/config5/cross.txt',
                    total_tick=6,
                    start_position=8)

    def test_case6(self):
        """
        目前的道路更新机制是，在当前时刻所有道路都go_by_tick，
        并将每个道路的驶出车辆全部驶出存放于全局的字典global_exit_queue中，
        待所有道路全部go_by_tick结束后统一对每个道路进行enter

        @NOTICE： 未考虑目标道路无法容纳全部想要enter的汽车的情况，如过发生，则会丢弃无法容纳的车辆
        """
        g = Game()
        id_2_cars, id_2_roads, id_2_cross, global_exit_queue = \
            build_objects_from_files(car_path='src/tests/test_pass_cross_cases/config6/car.txt',
                                     road_path='src/tests/test_pass_cross_cases/config6/road.txt',
                                     cross_path='src/tests/test_pass_cross_cases/config6/cross.txt')
        global_tick = 1
        car_id = 100
        for lane in id_2_roads[4]._lanes['positive']:
            lane.enter(id_2_cars[car_id], 10, global_tick)
            lane.enter(id_2_cars[car_id + 1], 10, global_tick)
            car_id += 100
        for lane in id_2_roads[3]._lanes['positive']:
            lane.enter(id_2_cars[car_id], 10, global_tick)
            lane.enter(id_2_cars[car_id + 1], 10, global_tick)
            car_id += 100

        for lane in id_2_roads[1]._lanes['positive']:
            lane.enter(id_2_cars[car_id], 10, global_tick)
            lane.enter(id_2_cars[car_id + 1], 10, global_tick)
            car_id += 100

        for car_id in id_2_cars:
            id_2_cars[car_id].set_path([(id_2_roads[2], 'positive')])

        while global_tick < 6:
            g.run(id_2_cross[5])
            for road_id in id_2_roads:
                id_2_roads[road_id].go_by_tick(global_tick)
            for road_id in id_2_roads:
                id_2_roads[road_id].enter_all(global_tick)
            global_exit_queue.clear()
            global_tick += 1
