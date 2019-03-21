# -*- coding: UTF-8 -*-


class Cross(object):
    def __init__(self, id, up_road_id, right_road_id, down_road_id, left_road_id):
        self._id = id
        self._road_id_list = [up_road_id, right_road_id, down_road_id, left_road_id]
        self._sorted_road_id_list = [self._road_id_list.index(i) for i in sorted(self._road_id_list)]
        self._road_list = None
        self.from_road = None
        self.to_road = None

    def get_id(self):
        return self._id

    def get_road_id_list(self):
        return self._road_id_list

    def get_road_list(self):
        return self._road_list

    def set_road_list(self, roads):
        self._road_list = roads
        self.from_road = []
        self.to_road = []
        for r in self._road_list:
            if r is None:
                continue
            if r.is_duplex():
                if r.get_destination() == self:
                    self.from_road.append((r, 'positive'))
                    self.to_road.append((r, 'negative'))
                else:
                    self.from_road.append((r, 'negative'))
                    self.to_road.append((r, 'positive'))
            else:
                if r.get_destination() == self:
                    self.from_road.append((r, 'positive'))
                else:
                    self.to_road.append((r, 'positive'))

    def go_by_tick(self, global_tick):
        ready_out_slot = {}
        while True:
            ready_in_slot = {}
            for road, direction in self.from_road:
                if (road, direction) not in ready_out_slot:
                    exit_slot, lane_index, next_road, next_road_direction, next_dist = \
                        road.get_ready_exit_slot(direction)
                    # 这条道路没有要驶出的车辆
                    if exit_slot is None and lane_index is None:
                        continue
                    ready_out_slot[(road, direction)] = (exit_slot, lane_index, next_road, next_road_direction, next_dist)
                exit_slot, lane_index, next_road, next_road_direction, next_dist = ready_out_slot[(road, direction)]
                # 如果下一条路已经满了则直接更新当前道路
                if next_road.is_full(next_road_direction):
                    ready_out_slot.pop((road, direction))
                    road.lane_go_by_tick(global_tick, direction, lane_index)
                    continue

                driving_direction = self._judge_driving_direction(road, next_road)
                if (next_road, next_road_direction) not in ready_in_slot:
                    ready_in_slot[(next_road, next_road_direction)] = (road, direction)
                else:
                    last_driving_direction = self._judge_driving_direction(ready_in_slot[(next_road, next_road_direction)][0],
                                                                           next_road)
                    if last_driving_direction > driving_direction:
                        ready_in_slot[(next_road, next_road_direction)] = (road, direction)

            # 路口调度完成
            if len(ready_out_slot) == 0:
                return

            # 按照road id升续进行调度
            for index in self._sorted_road_id_list:
                road = self._road_list[index]
                if road is None:
                    continue
                if road.get_destination() == self:
                    direction = 'positive'
                elif road.is_duplex():
                    direction = 'negative'
                else:
                    continue
                # 这条道路没有要驶出的车辆
                if (road, direction) not in ready_out_slot:
                    continue
                (exit_slot, lane_index, next_road, next_road_direction, next_dist) = ready_out_slot[(road, direction)]
                if (road, direction) == ready_in_slot[(next_road, next_road_direction)]:
                    ready_out_slot.pop((road, direction))
                    car = road.exit(direction, lane_index)
                    car.switch_next_road()
                    next_road.enter(car, next_dist, next_road_direction, global_tick)
                    road.lane_go_by_tick(global_tick, direction, lane_index)

    def _judge_driving_direction(self, road, next_road):
        road_index = self._road_list.index(road)
        next_road_index = self._road_list.index(next_road)
        if next_road_index == (road_index + 2) % 4:
            # 直行
            return 0

        if next_road_index == (road_index - 1) % 4:
            # 右转
            return 2

        if next_road_index == (road_index + 1) % 4:
            # 左传
            return 1
