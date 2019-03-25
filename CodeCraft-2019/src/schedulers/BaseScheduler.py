import logging
import time


class BaseScheduler(object):
    def __init__(self, id_2_cars, id_2_roads, id_2_cross):
        self._global_tick = 1
        self._id_2_cars = id_2_cars
        self._id_2_roads = id_2_roads
        self._id_2_cross = id_2_cross
        self._not_start_cars_ids = sorted(id_2_cars.keys())
        self._running_cars = []
        self._arrived_cars = []
        self._dead = False
        self._unfinished_cross_ids = []

    def is_all_arrived(self):
        return len(self._arrived_cars) == len(self._id_2_cars)

    def scheduling(self, global_tick):
        raise NotImplementedError

    def arrived(self, car):
        self._arrived_cars.append(car.get_id())
        self._running_cars.remove(car.get_id())

    def go_by_tick(self, global_tick):
        # 所有道路状态更新
        for road_id in self._id_2_roads:
            self._id_2_roads[road_id].go_by_tick(global_tick)
        # 所有路口状态更新
        self._unfinished_cross_ids = list(sorted(self._id_2_cross.keys()))
        while len(self._unfinished_cross_ids) > 0:
            self._dead = True
            next_cross_ids = []
            for cross_id in self._unfinished_cross_ids:
                cross = self._id_2_cross[cross_id]
                cross.go_by_tick(global_tick)
                if not self._id_2_cross[cross_id].is_done():
                    next_cross_ids.append(cross_id)
                if cross.has_updated() or cross.is_done():
                    self._dead = False
            self._unfinished_cross_ids = next_cross_ids
            if self._dead:
                self.dead_lock_handler()
                break

    def dead_lock_handler(self):
        logging.warning("dead lock in %s" % ",".join([str(id) for id in self._unfinished_cross_ids]))

    def multi_scheduling(self):
        global_tick = 1
        start = time.time()
        while not self.is_all_arrived():
            logging.info("current tick: %d" % global_tick)
            self.go_by_tick(global_tick)
            self.scheduling(global_tick)
            global_tick += 1
        end = time.time()
        logging.info("all cars have arrived, total ticks: %d, total time %d s" % (global_tick - 1, end-start))
