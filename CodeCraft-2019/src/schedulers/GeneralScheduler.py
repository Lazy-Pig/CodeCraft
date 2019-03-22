# -*- coding: UTF-8 -*-
from algrithms.EdgeWeightedDigraph import EdgeWeightedDigraph
from algrithms.DijkstraSP import DijkstraSP


class GeneralScheduler(object):
    def __init__(self, id_2_cars, id_2_roads, id_2_cross, congestion_ratio=0.1):
        self._id_2_cars = id_2_cars
        self._id_2_roads = id_2_roads
        self._id_2_cross = id_2_cross
        self._not_start_cars_ids = sorted(id_2_cars.keys())
        self._running_cars = []
        self._arrived_cars = []
        self._congestion_ratio = congestion_ratio
        self._cars_just_run = []

    def is_all_arrived(self):
        return len(self._arrived_cars) == len(self._id_2_cars)

    def get_cars_just_run(self):
        return self._cars_just_run

    def scheduling(self, global_tick):
        """
        1、为没有出发的车辆规划路径
        2、根据当前时刻的道路状况为已经在行驶的车辆调整路径
        """
        # 找出能够开始出发的车辆
        self._cars_just_run = []
        for car_id in self._not_start_cars_ids:
            car = self._id_2_cars[car_id]
            if car.get_plan_time() > global_tick:
                continue
            car_source = car.get_source()
            # 车辆出发点的四个道路中，都不那么拥塞就可以出发
            if all([road is None or not self._is_this_road_congestion(road, entrance=car_source) for road in car_source.get_road_list()]):
                path = self._plan_path(car)
                start_road, state_road_direction = path[0]
                if not start_road.is_full(state_road_direction):
                    self._cars_just_run.append(car)
                    car.set_path(path)
                    car.start_running(global_tick)
                    self._running_cars.append(car.get_id())
        for car in self._cars_just_run:
            self._not_start_cars_ids.remove(car.get_id())

    def _plan_path(self, car):
        graph = EdgeWeightedDigraph(car, self._id_2_roads.values())
        shortest = DijkstraSP(graph, car.get_source_id())
        path = shortest.path_to(car.get_destination_id())
        return path

    def _is_this_road_congestion(self, road, entrance):
        if road.get_source() == entrance:
            car_num = road.get_car_num('positive')
            is_full = road.is_full('positive')
        elif road.is_duplex():
            car_num = road.get_car_num('negative')
            is_full = road.is_full('negative')
        else:
            return False
        return is_full or (car_num >= int(road.get_length() * road.get_channel_number() * self._congestion_ratio))
        # return is_full or (car_num >= road.get_channel_number())

    def arrived(self, car):
        self._arrived_cars.append(car.get_id())
        self._running_cars.remove(car.get_id())
        # print()
        # print(self._running_cars)
        # print(self._not_start_cars_ids)
