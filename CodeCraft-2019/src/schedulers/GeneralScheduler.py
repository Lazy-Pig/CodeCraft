# -*- coding: UTF-8 -*-
from schedulers.BaseScheduler import BaseScheduler
from algrithms.EdgeWeightedDigraph import EdgeWeightedDigraph


class GeneralScheduler(BaseScheduler):
    def __init__(self, id_2_cars, id_2_roads, id_2_cross, congestion_ratio=0.1):
        super(GeneralScheduler, self).__init__(id_2_cars, id_2_roads, id_2_cross)
        self._congestion_ratio = congestion_ratio
        self._cars_just_run = []

    def get_cars_just_run(self):
        return self._cars_just_run

    def scheduling(self, global_tick):
        """
        1、根据当前时刻的道路状况为已经在行驶的车辆调整路径
        2、为没有出发的车辆规划路径
        """
        # for car_id in self._running_cars:
        #     car = self._id_2_cars[car_id]
        #     next_road, next_direction = car.get_next_road()
        #     if next_road is not None and next_road.get_saturation(next_direction) >= 0.8:
        #         invalid_road_ids = car.get_pass_path()[:]
        #         invalid_road_ids.append(car.get_current_road()[0].get_id())
        #         graph = EdgeWeightedDigraph(car, self._id_2_roads.values(), invalid_road_ids)
        #         current_road, current_direction = car.get_current_road()
        #         next_cross_id = current_road.get_source_id() if current_direction == 'negative' else current_road.get_destination_id()
        #         if next_cross_id != car.get_destination_id():
        #             path = self._plan_path(graph, next_cross_id, car.get_destination_id())
        #             car.set_path(path)

        # 找出能够开始出发的车辆
        self._cars_just_run = []
        for car_id in self._not_start_cars_ids:
            car = self._id_2_cars[car_id]
            if car.get_plan_time() > global_tick:
                continue
            car_source = car.get_source()
            # 车辆出发点的四个道路中，都不那么拥塞就可以出发
            if all([road is None or not self._is_this_road_congestion(road, entrance=car_source) for road in car_source.get_road_list()]):
                graph = EdgeWeightedDigraph(car, self._id_2_roads.values())
                path = self._plan_path(graph, car.get_source_id(), car.get_destination_id())
                start_road, state_road_direction = path[0]
                if not start_road.is_full(state_road_direction):
                    self._cars_just_run.append(car)
                    car.set_path(path)
                    car.start_running(global_tick)
                    self._running_cars.append(car.get_id())
        for car in self._cars_just_run:
            self._not_start_cars_ids.remove(car.get_id())

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
