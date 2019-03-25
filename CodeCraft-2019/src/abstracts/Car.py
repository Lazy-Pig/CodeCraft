# -*- coding: UTF-8 -*-


class Car(object):
    def __init__(self, id, source_id, destination_id, speed, plan_time):
        self._id = id
        self._source_id = source_id
        self._destination_id = destination_id
        self._speed = speed
        self._plan_time = plan_time

        self._source = None
        self._destination = None
        self._current_road = None
        self.clear()

    def clear(self):
        self._current_road = None
        self._current_direction = None
        self._current_position = None
        self._next_road = None
        self._path = None
        self._pass_path = []
        self._current_tick = 0
        self._begin_tick = -1
        self._finish_tick = -1
        self._is_arrived = False
        self._total_time = 0

    def set_is_arrived(self):
        self._pass_path.append(self._current_road.get_id())
        self._is_arrived = True

    def is_arrived(self):
        return self._is_arrived

    def is_running(self):
        return self._current_road is not None

    def start_running(self, global_tick):
        """
        根据制定的path开始行走

        @param path: list of (Road, bool)，路线经过的Road;bool为true则为正向，为false则为反向
        @param global_tick: int，开始行走的时间
        """
        self._current_road, self._current_direction = self._path.pop(0)
        position = min(self._speed, self._current_road.get_speed())
        self._current_road.enter(self, position, self._current_direction, global_tick)
        self._begin_tick = global_tick

    def go_by_tick(self):
        # self._current_road
        pass

    def get_id(self):
        return self._id

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

    def get_speed(self):
        return self._speed

    def get_plan_time(self):
        return self._plan_time

    def set_current_position(self, pos):
        self._current_position = pos

    def set_current_tick(self, tick):
        self._current_tick = tick

    def set_path(self, path):
        self._path = path
        for r, d in path:
            self._total_time += r.get_weight(self)

    def get_path(self):
        return self._path

    def get_next_road(self):
        """
        获取下一个road

        @return (Road，bool)，Road对象和方向
        """
        if len(self._path) == 0:
            return None, None

        return self._path[0]

    def switch_next_road(self):
        self._pass_path.append(self._current_road.get_id())
        self._current_road, self._current_direction = self._path.pop(0)

    def get_current_tick(self):
        return self._current_tick

    def set_begin_tick(self, tick):
        self._begin_tick = tick

    def get_begin_tick(self):
        return self._begin_tick

    def get_pass_path(self):
        return self._pass_path

    def get_current_road(self):
        return self._current_road, self._current_direction
