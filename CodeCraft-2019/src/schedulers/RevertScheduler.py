from schedulers.BaseScheduler import BaseScheduler
from algrithms.EdgeWeightedDigraph import EdgeWeightedDigraph
from algrithms.DijkstraSP import DijkstraSP
import time
import logging


class RevertScheduler(BaseScheduler):
    def __init__(self, id_2_cars, id_2_roads, id_2_cross, init_saturation=0.8):
        super(RevertScheduler, self).__init__(id_2_cars, id_2_roads, id_2_cross)
        self._init_saturation = init_saturation
        self._saturation = init_saturation
        roads = self._id_2_roads.values()
        self._car_id_2_path = {}
        for car_id in self._id_2_cars:
            car = self._id_2_cars[car_id]
            g = EdgeWeightedDigraph(roads, car)
            shortest = DijkstraSP(g, car.get_source_id())
            path = shortest.path_to(car.get_destination_id())
            car.set_path(path)
            self._car_id_2_path[car_id] = path[:]

    def scheduling(self, global_tick):
        # 找出能够开始出发的车辆
        cars_just_run = []
        for car_id in self._not_start_cars_ids:
            car = self._id_2_cars[car_id]
            if car.get_plan_time() > global_tick:
                continue
            car_source = car.get_source()
            first_raod, first_raod_direction = car.get_path()[0]
            if all([l.is_full() for l in first_raod.get_lanes(first_raod_direction)]):
                continue
            if all([r.get_saturation(d) < self._saturation for r, d in car.get_path()]):
                cars_just_run.append(car)
                car.start_running(global_tick)
                self._running_cars.append(car.get_id())
        for car in cars_just_run:
            self._not_start_cars_ids.remove(car.get_id())

    def go_by_tick(self, global_tick):
        super(RevertScheduler, self).go_by_tick(global_tick)

    def dead_lock_handler(self):
        super(RevertScheduler, self).dead_lock_handler()
        self.clear()

    def clear(self):
        self._saturation = max(0.1, self._saturation - 0.1)
        self._global_tick = 1
        self._not_start_cars_ids = sorted(self._id_2_cars.keys())
        self._running_cars = []
        self._arrived_cars = []
        for road in self._id_2_roads.values():
            road.clear()
        for cross in self._id_2_cross.values():
            cross.clear()
        for car_id in self._id_2_cars:
            car = self._id_2_cars[car_id]
            car.clear()
            car.set_path(self._car_id_2_path[car_id][:])
        logging.info("start new epoch with saturation %2f" % self._saturation)

    def multi_scheduling(self):
        start = time.time()
        while not self.is_all_arrived():
            if self._global_tick % 1 == 0:
                logging.info("current tick: %d" % self._global_tick)
            self.go_by_tick(self._global_tick)
            self.scheduling(self._global_tick)
            self._global_tick += 1
        end = time.time()
        logging.info("all cars have arrived, total ticks: %d, total time %d s" % (self._global_tick - 1, end-start))
