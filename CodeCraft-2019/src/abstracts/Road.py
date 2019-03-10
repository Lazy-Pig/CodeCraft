from Lane import Lane


class Road(object):
    def __init__(self, id, length, speed, channel, source_id, destination_id, is_duplex, global_exit_queue):
        self._id = id
        self._length = length
        self._speed = speed
        self._channel = channel
        self._source_id = source_id
        self._destination_id = destination_id
        self._is_duplex = is_duplex
        self._source = None
        self._destination = None
        self._current_tick = 0
        self.global_exit_queue = global_exit_queue
        self._lanes = {'positive': [Lane(i, self._speed, self._length, self, global_exit_queue)
                                    for i in range(self._channel)]}
        if self._is_duplex:
            self._lanes['negative'] = [Lane(i, self._speed, self._length, self, global_exit_queue)
                                       for i in range(self._channel)]

    def go_by_tick(self, global_tick):
        """
        本Road上的所有车辆行驶一个tick，驶出本Road的车辆进入global_exit_queue中，
        等待本tick所有正常行驶的车辆全部更新完毕后，统一进入目标Road

        @param global_tick: int
        """
        for lane in self._lanes["positive"]:
            lane.go_by_tick(global_tick)
        if self._is_duplex:
            for lane in self._lanes["negative"]:
                lane.go_by_tick(global_tick)

    def enter_all(self, global_tick):
        """
        将当前tick所有准备进入本Road的车辆安置妥当

        """
        self.enter_one_side(True, global_tick)
        if self._is_duplex:
            self.enter_one_side(False, global_tick)

    def enter_one_side(self, direction, global_tick):
        """
        安置单边的车辆，遵循：直行 > 左转 > 右转 的优先级

        @param direction: bool
        @param global_tick: int
        """
        all_cars_will_enter = self.global_exit_queue[(self._id, direction)]
        entrance = self._source if direction else self._destination
        neighbors = entrance.get_road_list()
        index_of_entrance = neighbors.index(entrance)
        straight_road = neighbors[(index_of_entrance + 2) % 4]
        left_road = neighbors[(index_of_entrance - 1) % 4]
        right_road = neighbors[(index_of_entrance + 1) % 4]

        all_lanes_straight_cars = all_cars_will_enter[straight_road.get_id()]
        self.enter_from_same_road(all_lanes_straight_cars, direction, global_tick)
        all_lanes_left_cars = all_cars_will_enter[left_road.get_id()]
        self.enter_from_same_road(all_lanes_left_cars, direction, global_tick)
        all_lanes_right_cars = all_cars_will_enter[right_road.get_id()]
        self.enter_from_same_road(all_lanes_right_cars, direction, global_tick)

    def enter_from_same_road(self, all_lanes_cars, direction, global_tick):
        """
        从同一Road进入的本Road的车辆，遵循：从车道号小的到车道号大的蛇形循环 依次进入

        @param all_lanes_cars: list
        @param direction: bool
        @param global_tick: int
        """
        channel_num = len(all_lanes_cars)
        channel_index = 0
        while not all([lane.isEmpty() for lane in all_lanes_cars]):
            if not all_lanes_cars[channel_index % channel_num].isEmpty():
                car, next_dist = all_lanes_cars[channel_index % channel_num].get()
                self.enter(car, next_dist, direction, global_tick)
            channel_index += 1

    def enter(self, car, position, direction, global_tick):
        """
        车进入Road

        @param car: Car
        @param position: int，该车进入车道后的这一时刻位于车道的哪个位置，取值[1,length]
        @param direction: bool，进入的Road的方向
        @param global_tick: int
        """
        assert 0 < position <= self._length
        lanes = self._lanes["positive"] if direction else self._lanes["negative"]
        for lane in lanes:
            if not lane.is_full():
                lane.enter(car, position, global_tick)
        else:
            raise Exception("Car(%d)无法进入Road(%d)" % (car.get_id(), self._id))

    def get_id(self):
        return self._id

    def get_length(self):
        return self._length

    def get_speed(self):
        return self._speed

    def get_channel_number(self):
        return self._channel

    def get_source_id(self):
        return self._source_id

    def get_source(self):
        return self._source

    def set_source(self, obj):
        self._source = obj

    def get_destination_id(self):
        return self._destination_id

    def get_destination(self):
        return self._destination

    def set_destination(self, obj):
        self._destination = obj

    def get_current_tick(self):
        return self._current_tick
