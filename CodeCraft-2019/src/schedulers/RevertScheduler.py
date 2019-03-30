from schedulers.BaseScheduler import BaseScheduler
from algrithms.EdgeWeightedDigraph import EdgeWeightedDigraph
from algrithms.DijkstraSP import DijkstraSP
import time
import logging
from collections import defaultdict
import math


class RevertScheduler(BaseScheduler):
    def __init__(self, id_2_cars, id_2_roads, id_2_cross,
                 init_saturation=0.5, first_road_saturation=1.0, satisfied_num=20, car_num_ratio=0.04):
        super(RevertScheduler, self).__init__(id_2_cars, id_2_roads, id_2_cross)
        self._init_saturation = init_saturation
        self._first_road_saturation = first_road_saturation
        self._satisfied_num = satisfied_num
        self._car_num_ratio = car_num_ratio
        self._saturation = init_saturation
        self._map_capacity = sum([self._id_2_roads[road_id].get_capacity() for road_id in self._id_2_roads])
        roads = self._id_2_roads.values()
        self._car_id_2_path = {}
        car_group = defaultdict(list)
        for car_id in self._id_2_cars:
            car = self._id_2_cars[car_id]
            car_group[car.get_source_id()].append(car)
        s_t = time.time()
        for source_id in car_group:
            g = EdgeWeightedDigraph(roads)
            shortest = DijkstraSP(g, source_id)
            for car in car_group[source_id]:
                if shortest.has_path_to(car.get_destination_id()):
                    path = shortest.path_to(car.get_destination_id())
                else:
                    path = shortest.bfs(car.get_destination_id())
                car.set_path(path)
                self._car_id_2_path[car.get_id()] = path[:]
        e_t = time.time()
        logging.info("DijkstraSP time cost: %d" % (e_t - s_t))
        self._not_start_cars_ids.sort(key=self.sort_by_total_time)
        self._not_start_cars_ids_back = self._not_start_cars_ids[:]

    def sort_by_total_time(self, car_id):
        return self._id_2_cars[car_id]._total_time

    def scheduling(self, global_tick):
        # 找出能够开始出发的车辆
        cars_just_run = []
        for car_id in self._not_start_cars_ids:
            if len(self._running_cars) > math.ceil(self._map_capacity * self._car_num_ratio):
            # if len(self._running_cars) > len(self._id_2_cars) * self._car_num_ratio:
                break

            car = self._id_2_cars[car_id]
            if car.get_plan_time() > global_tick:
                continue

            first_raod, first_raod_direction = car.get_path()[0]
            if all([l.is_full() for l in first_raod.get_lanes(first_raod_direction)]):
                continue

            if len(self._running_cars) < len(self._id_2_cars) // 100:
                can_start = True
            else:
                # flags = []
                # for r, d in car.get_path():
                #     if len(flags) >= self._satisfied_num:
                #         break
                #     flags.append(r.get_saturation(d) < self._saturation)
                can_start = all([r.get_saturation(d) < self._saturation for r, d in car.get_path()])

            if can_start:
                cars_just_run.append(car)
                car.start_running(global_tick)
                self._running_cars.append(car.get_id())
        for car in cars_just_run:
            self._not_start_cars_ids.remove(car.get_id())

    def dead_lock_handler(self):
        super(RevertScheduler, self).dead_lock_handler()
        self.clear()

    def clear(self):
        self._saturation = max(0.1, self._saturation - 0.1)
        # self._first_road_saturation = max(0.1, self._first_road_saturation - 0.1)
        self._global_tick = 1
        self._not_start_cars_ids = self._not_start_cars_ids_back[:]
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
        super(RevertScheduler, self).multi_scheduling()
        end = time.time()
        logging.info("all cars have arrived, total ticks: %d, total time %d s, best saturation %2f" %
                     (self._global_tick - 1, end-start, self._saturation))
