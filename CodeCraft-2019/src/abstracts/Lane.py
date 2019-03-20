from queue import Queue
import logging


class LaneSlot(object):
    def __init__(self, car, position, next=None, pre=None):
        self.car = car
        self.position = position
        self.next = next
        self.pre = pre
        self.state = None


class Lane(object):
    """
    车道 抽象为链表结构
    """
    def __init__(self, id, speed, length, road):
        self._id = id
        self._speed = speed
        self._length = length
        self._current_tick = 0
        self.road = road

        # head指向本车道的第一辆车，tail指向本车道的最后一辆车
        self._head = None
        self._tail = None
        self._car_num = 0

    def is_full(self):
        return self._tail is not None and self._tail.position == 1

    def is_empty(self):
        return self._head is None

    def is_waiting(self):
        return not self.is_empty() and self._head.state == 'waiting'

    def get_current_tick(self):
        return self._current_tick

    def go_by_tick(self, global_tick):
        """
        Lane上的所有车辆运行1个时间单位,
        未驶出本Lane的车辆状态记为finish
        驶出本Lane的车辆状态变成waiting，
        目标位置被waiting车辆阻挡而无法到达的车辆状态也记为waiting

        @param global_tick: int，当前全局时间tick
        @return
        """
        lane_slot_point = self._head
        while lane_slot_point and lane_slot_point.car.get_current_tick() < global_tick:
            current_v = min(self._speed, lane_slot_point.car.get_speed())
            # 如果第一辆车可能驶出道路的话需要单独处理
            if self._head == lane_slot_point and current_v > self._length - lane_slot_point.position:
                next_road, next_road_direction = lane_slot_point.car.get_next_road()
                # 车辆到达终点
                if next_road is None and next_road_direction is None:
                    lane_slot_point.car.set_current_tick(global_tick)
                    car = self.exit()
                    car.set_is_arrived()
                    lane_slot_point = lane_slot_point.next
                    continue
                current_dist = self._length - lane_slot_point.position
                next_v = min(next_road.get_speed(), lane_slot_point.car.get_speed())
                # 下一时刻驶出本车道
                if next_v - current_dist <= 0:
                    lane_slot_point.position = self._length
                    lane_slot_point.state = 'finish'
                    lane_slot_point.car.set_current_position(lane_slot_point.position)
                    lane_slot_point.car.set_current_tick(global_tick)
                # 当前时刻驶出本车道
                else:
                    lane_slot_point.state = 'waiting'
                lane_slot_point = lane_slot_point.next
                continue

            # 如果是车道上的第一辆车，pre_position为车道长度+1（不存在的位置）;否则，pre_position为前一辆车的位置
            pre_position = lane_slot_point.pre.position if lane_slot_point.pre is not None else self._length + 1

            # 肯定未驶出本车道
            if current_v < pre_position - lane_slot_point.position:
                if lane_slot_point.pre is None or lane_slot_point == self._head:
                    lane_slot_point.position += current_v
                else:
                    lane_slot_point.position = min(lane_slot_point.position + current_v, lane_slot_point.pre.position - 1)
                lane_slot_point.state = 'finish'
                lane_slot_point.car.set_current_position(lane_slot_point.position)
                lane_slot_point.car.set_current_tick(global_tick)
            # 可能驶出本车道
            else:
                if lane_slot_point.pre.state == 'finish':
                    lane_slot_point.position = pre_position - 1
                    lane_slot_point.state = 'finish'
                    lane_slot_point.car.set_current_position(lane_slot_point.position)
                    lane_slot_point.car.set_current_tick(global_tick)
                # 驶出车道
                else:
                    lane_slot_point.state = 'waiting'
            lane_slot_point = lane_slot_point.next
        self._current_tick = global_tick

    def enter(self, car, position, global_tick):
        """
        车进入车道

        @param car: Car
        @param global_tick: int
        @param position: int，该车进入车道后的这一时刻位于车道的哪个位置，取值[1,length]
        """
        assert 0 < position <= self._length
        # 保证车道还有slot容纳新进入的车辆
        if self._tail is not None:
            assert self._tail.position > 1
        position = min(position, self._tail.position - 1) if self._tail is not None else min(position, self._length)
        slot = LaneSlot(car, position)
        car.set_current_position(position)
        car.set_current_tick(global_tick)
        if self._head is None:
            self._head = self._tail = slot
        else:
            slot.next = None
            slot.pre = self._tail
            self._tail.next = slot
            self._tail = slot
        self._car_num += 1

    def exit(self):
        car = self._head.car
        self._head = self._head.next
        if self._head is not None:
            self._head.pre = None
        self._car_num -= 1
        return car

    def get_head(self):
        return self._head

    def get_car_num(self):
        return self._car_num
