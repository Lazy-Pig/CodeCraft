import math


class GeneralScheduler(object):
    def __init__(self, id_2_cars, id_2_roads, id_2_cross, congestion_ratio=0.3):
        self._id_2_cars = id_2_cars
        self._id_2_roads = id_2_roads
        self._id_2_cross = id_2_cross
        self._not_start_cars = set(id_2_cars.values())
        self._congestion_ratio = congestion_ratio
        self._cars_just_run = []

    def is_all_arrived(self):
        return len(self._not_start_cars) == 0

    def get_cars_just_run(self):
        return self._cars_just_run

    def scheduling(self, global_tick):
        """
        1、为没有出发的车辆规划路径
        2、根据当前时刻的道路状况为已经在行驶的车辆调整路径
        """
        # 找出能够开始出发的车辆
        self._cars_just_run = []
        for car in self._not_start_cars:
            car_source = car.get_source()
            # 车辆出发点的四个道路中，有一个不那么拥塞就可以出发
            for road in car_source.get_road_list():
                if road is not None and not self._is_this_road_congestion(road, entrance=car_source):
                    self._cars_just_run.append(car)
                    self._plan_path(car)
                    car.start_running(global_tick)
                    break
        for car in self._cars_just_run:
            self._not_start_cars.remove(car)
        # 为新出发的车辆规划路径

    def _plan_path(self, car):
        # TODO
        pass

    def calculate_weight(self, car, road):
        """
        车通过道路需要用的时间作为图的权重

        @param car: Car
        @param road: Road
        @return int
        """
        v = min(car.get_speed(), road.get_speed())
        return math.ceil(road.get_length() / v)

    def _is_this_road_congestion(self, road, entrance):
        if road.get_source() == entrance:
            car_num = road.get_car_num('positive')
            is_full = road.is_full('positive')
        elif road.is_duplex():
            car_num = road.get_car_num('negative')
            is_full = road.is_full('negative')
        else:
            car_num = road.get_length()
            is_full = True
        return not is_full and (car_num > int(road.get_length() * self._congestion_ratio))
