from queue import Queue


class LaneSlot(object):
    def __init__(self, car, position, next=None):
        self.car = car
        self.position = position
        self.next = next


class Lane(object):
    """
    车道 抽象为链表结构
    """
    def __init__(self, id, speed, length, road, global_exit_queue):
        self._id = id
        self._speed = speed
        self._length = length
        self._current_tick = 0
        self.road = road
        self.global_exit_queue = global_exit_queue

        # head指向本车道的第一辆车，tail指向本车道的最后一辆车
        self._head = None
        self._tail = None

    def is_full(self):
        return self._tail is not None and self._tail.position == 1

    def get_current_tick(self):
        return self._current_tick

    def go_by_tick(self, global_tick):
        """
        Lane上的所有车辆运行1个时间单位,驶出本Lane的车辆进入global_exit_queue中，
        等待本tick所有正常行驶的车辆全部更新完毕后，统一进入目标Road

        @param global_tick: int，当前全局时间tick
        @return
        """
        lane_slot_point = self._head
        while lane_slot_point:
            current_v = min(self._speed, lane_slot_point.car.get_speed())
            # 肯定未驶出本车道
            if current_v <= self._length - lane_slot_point.position:
                lane_slot_point.position += current_v
                lane_slot_point.car.set_current_position(lane_slot_point.position)
                lane_slot_point.car.set_current_tick(global_tick)
            # 可能驶出本车道
            else:
                current_dist = self._length - lane_slot_point.position
                next_road, next_road_direction = lane_slot_point.car.get_next_road()
                # 车辆到达终点
                if next_road is None and next_road_direction is None:
                    lane_slot_point.car.set_current_tick(global_tick)
                    car = self.exit()
                    car.set_is_arrived()
                    lane_slot_point = lane_slot_point.next
                    continue
                next_v = min(next_road.get_speed(), lane_slot_point.car.get_speed())
                # 下一时刻驶出本车道
                if next_v - current_dist <= 0:
                    lane_slot_point.position = self._length
                    lane_slot_point.car.set_current_position(lane_slot_point.position)
                    lane_slot_point.car.set_current_tick(global_tick)
                # 当前时刻驶出本车道，进入global_exit_queue
                else:
                    next_dist = next_v - current_dist
                    car = self.exit()
                    if (next_road, next_road_direction) not in self.global_exit_queue:
                        self.global_exit_queue[(next_road, next_road_direction)] = {}
                    target_dict = self.global_exit_queue[(next_road, next_road_direction)]
                    if self.road not in target_dict:
                        channel_number = self.road.get_channel_number()
                        target_dict[self.road] = [Queue() for _ in range(channel_number)]
                    target_queue = target_dict[self.road][self._id]
                    target_queue.put((car, next_dist))
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
            self._tail.next = slot
            self._tail = slot

    def exit(self):
        car = self._head.car
        self._head = self._head.next
        return car

    def get_head(self):
        return self._head
