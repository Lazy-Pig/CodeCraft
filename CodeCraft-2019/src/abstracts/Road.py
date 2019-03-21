# -*- coding: UTF-8 -*-
from abstracts.Lane import Lane
import logging
import math


class Road(object):
    def __init__(self, id, length, speed, channel, source_id, destination_id, is_duplex):
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
        self._scheduler = None
        self._lanes = {'positive': [Lane(i, self._speed, self._length, self)
                                    for i in range(self._channel)]}
        self._car_num = {'positive': 0}
        self._ready_exit_lane_index = {'positive': 0}
        if self._is_duplex:
            self._lanes['negative'] = [Lane(i, self._speed, self._length, self)
                                       for i in range(self._channel)]
            self._car_num['negative'] = 0
            self._ready_exit_lane_index['negative'] = 0

    def go_by_tick(self, global_tick):
        """
        本Road上的所有车辆行驶一个tick，驶出本Road的车辆进入global_exit_queue中，
        等待本tick所有正常行驶的车辆全部更新完毕后，统一进入目标Road

        @param global_tick: int
        """
        self._car_num['positive'] = 0
        for i in range(self._channel):
            self.lane_go_by_tick(global_tick, 'positive', i)
            self._car_num['positive'] += self._lanes['positive'][i].get_car_num()
        if self._is_duplex:
            self._car_num['negative'] = 0
            for i in range(self._channel):
                self.lane_go_by_tick(global_tick, 'negative', i)
                self._car_num['negative'] += self._lanes['negative'][i].get_car_num()

    def lane_go_by_tick(self, global_tick, direction, lane_index):
        self._lanes[direction][lane_index].go_by_tick(global_tick)

    def enter(self, car, position, direction, global_tick):
        """
        车进入Road

        @param car: Car
        @param position: int，该车进入车道后的这一时刻位于车道的哪个位置，取值[1,length]
        @param direction: str，进入的Road的方向, 'positive' or 'negative'
        @param global_tick: int
        """
        assert 0 < position <= self._length
        lanes = self._lanes[direction]
        cross = self._source if direction == 'positive' else self._destination
        if all([l.is_full() for l in lanes]):
            logging.warning("Cross(%d): Car(%d)不能进入Road（%d）" % (cross.get_id(), car.get_id(), self._id))
        for lane in lanes:
            if not lane.is_full():
                lane.enter(car, position, global_tick)
                break
        self._car_num[direction] = sum([l.get_car_num() for l in lanes])

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

    def get_lanes(self, direction):
        return self._lanes[direction]

    def is_duplex(self):
        return self._is_duplex == 1

    def get_car_num(self, direction):
        return self._car_num[direction]

    def is_full(self, direction):
        return all([lane.is_full() for lane in self._lanes[direction]])

    def get_ready_exit_slot(self, direction):
        if all([not l.is_waiting() for l in self._lanes[direction]]):
            return None, None, None, None, None

        exit_slot = self._lanes[direction][self._ready_exit_lane_index[direction]].get_head()
        while exit_slot is None or exit_slot.state != 'waiting':
            self._ready_exit_lane_index[direction] = (self._ready_exit_lane_index[direction] + 1) % self._channel
            exit_slot = self._lanes[direction][self._ready_exit_lane_index[direction]].get_head()

        current_dist = self._length - exit_slot.position
        next_road, next_road_direction = exit_slot.car.get_next_road()
        next_v = min(next_road.get_speed(), exit_slot.car.get_speed())
        next_dist = next_v - current_dist
        result = (exit_slot, self._ready_exit_lane_index[direction], next_road, next_road_direction, next_dist)
        self._ready_exit_lane_index[direction] = (self._ready_exit_lane_index[direction] + 1) % self._channel
        return result

    def exit(self, direction, lane_num):
        return self._lanes[direction][lane_num].exit()

    def get_weight(self, car):
        """
        车通过道路需要用的时间作为图的权重

        @param car: Car
        @return int
        """
        v = min(car.get_speed(), self.get_speed())
        return math.ceil(self.get_length() / v)

    def set_scheduler(self, scheduler):
        self._scheduler = scheduler

    def get_scheduler(self):
        return self._scheduler
