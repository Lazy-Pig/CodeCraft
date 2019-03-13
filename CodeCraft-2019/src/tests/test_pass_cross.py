import unittest
from ..utils.init_util import build_objects_from_files
from queue import Queue
from ..game.Game import Game


class TestPassCross(unittest.TestCase):
    def test_case1(self):
        g = Game()
        id_2_cars, id_2_roads, id_2_cross, global_exit_queue = \
            build_objects_from_files(car_path='src/tests/test_pass_cross_cases/config1/car.txt',
                                     road_path='src/tests/test_pass_cross_cases/config1/road.txt',
                                     cross_path='src/tests/test_pass_cross_cases/config1/cross.txt')
        global_tick = 1
        lanes1 = id_2_roads[1]._lanes['positive']
        car_id = 100
        for lane in lanes1:
            lane.enter(id_2_cars[car_id], id_2_cars[car_id].get_speed(), global_tick)
            lane.enter(id_2_cars[car_id + 1], id_2_cars[car_id].get_speed(), global_tick)
            car_id += 100

        for car_id in id_2_cars:
            id_2_cars[car_id].set_path([(id_2_roads[2], True)])

        while global_tick < 6:
            g.run(id_2_cross[2])
            for road_id in id_2_roads:
                id_2_roads[road_id].go_by_tick(global_tick)
            for road_id in id_2_roads:
                id_2_roads[road_id].enter_all(global_tick)
            global_exit_queue.clear()
            global_tick += 1
        self.assertEqual(global_exit_queue, {})
